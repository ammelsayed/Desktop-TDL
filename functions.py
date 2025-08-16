from PIL import Image, ImageDraw, ImageFont
from datetime import date
import tempfile,sys,os
from ctypes import windll
import subprocess


# Importing Dictonaries
from directories import WindowsFonts


def FileSize(file_path):
    try:
        # Get file size in bytes
        size_bytes = os.path.getsize(file_path)

        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.21} TB"
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return "0.0 B"
    
    except OSError as e:
        print(f"Error: Unable to access file '{file_path}': {str(e)}")
        return "0.0 B"

def get_wallpaper_path():


    if sys.platform == "darwin":
        # MacOS
        import subprocess
        script = 'tell application "System Events" to get picture of current desktop'
        args = ["osascript", "-e", script]
        return subprocess.check_output(args).decode().strip()

    elif sys.platform.startswith("win"):
        # Windows
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Control Panel\\Desktop", 0, winreg.KEY_READ)
        path, _ = winreg.QueryValueEx(key, "WallPaper")
        return path
    
    else:
        # Linux
        import subprocess
        try:
            cmd = ['gsettings', 'get',
                   'org.gnome.desktop.background', 'picture-uri']
            output = subprocess.check_output(cmd).decode().strip()
            return output.strip("'\n").replace('file://', '')
        except Exception as e:
            print(e)
            sys.exit(1)
    
def reset_wallpaper(new_path):
    
    if sys.platform == "darwin":
        # MacOS
        pass

    elif sys.platform.startswith("win"):
        # Windows
        from ctypes import windll
        windll.user32.SystemParametersInfoW(20, 0, new_path, 3)

    else:
        # Linux
        pass
    

def set_wallpaper(input):

    # if the input is an image path, the wallpaper set is direct, nonethless if it is an image, we create a temptorary path for it.

    if type(input) == str:
        path = input

    # if it is an image Save to a temporary PNG (lossless, fast)
    else:  
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            path = tmp.name
            input.save(path, format="PNG")

        
    if sys.platform == "darwin":
        # MacOS
        pass

    elif sys.platform.startswith("win"):
        # Windows
        windll.user32.SystemParametersInfoW(20, 0, path, 3)

    elif sys.platform.startswith("linux"):
        try:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{path}"])
        except Exception:
            # Fallback: feh (lightweight)
            subprocess.run(["feh", "--bg-scale", path])
    else:
        raise RuntimeError("Unsupported OS")
    

def WriteOnDesktop(
                    todo_items,
                    wallpaper_path, 
                    corner, 
                    font_name,
                    font_size,
                    text_color,
                    box_color,
                    pad_tf,
                    padding
                    ):

    # Load current wallpaper
    wp = wallpaper_path

    # Load the image
    img = Image.open(wp)
    img_w, img_h = img.size

    # Prepare a drawing context
    draw = ImageDraw.Draw(img)

    # Title
    line_lenght = 11
    title = f"To Do List ({date.today()})\n{'—'*line_lenght}\n"

    # Compose text
    text = title + "\n".join(f"({i+1}) {item}" for i, item in enumerate(todo_items.split("\n")))

    # Load font
    font = ImageFont.truetype(WindowsFonts[font_name], size=font_size, encoding="utf-8")

    # Measure text at origin
    x0, y0, x1, y1 = draw.textbbox((0,0), text, font=font)
    text_width = x1 - x0
    text_height = y1 - y0
    box_width = text_width + 2 * padding
    box_height = text_height + 2 * padding

    # Determine box origin
    if corner == "Top Left":
        box_x, box_y = pad_tf, pad_tf
    elif corner == "Top Right":
        box_x, box_y = img_w - pad_tf - box_width, pad_tf
    elif corner == "Bottom Left":
        box_x, box_y = pad_tf, img_h - pad_tf - box_height
    elif corner == "Bottom Right":
        box_x, box_y = img_w - pad_tf - box_width, img_h - pad_tf - box_height
    elif corner == "Center":
        box_x = (img_w - box_width) / 2
        box_y = (img_h - box_height) / 2
    else:
        raise ValueError("Invalid corner specified.")

    # Draw box and text
    draw.rectangle(
        [(box_x, box_y), (box_x + box_width, box_y + box_height)],
        fill=box_color
    )
    draw.text((box_x + padding, box_y + padding), text,
              font=font, fill=text_color)

    # Save and apply
    set_wallpaper(img)


