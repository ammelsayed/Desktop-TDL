from datetime import date
import sys,os
from textwrap import wrap


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
        pass

    elif sys.platform.startswith("win"):
        # Windows
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Control Panel\\Desktop", 0, winreg.KEY_READ)
        path, _ = winreg.QueryValueEx(key, "WallPaper")
        return path
    
    else:
        # Linux
        from subprocess import run, PIPE
        shell_command =  run(
                                """gsettings get org.gnome.desktop.background picture-uri | sed "s/file:\/\///" | xargs -I{} realpath {}""",
                                shell = True,
                                stdout=PIPE,
                                text=True
                                )
        return shell_command.stdout.strip("\n")


def set_wallpaper(path):

    if sys.platform == "darwin":
        pass

    elif sys.platform.startswith("win"):
        from ctypes import windll
        windll.user32.SystemParametersInfoW(20, 0, path, 3)

    elif sys.platform.startswith("linux"):
        from subprocess import run, PIPE
        uri = f"file://{path}"
        run(
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri],
            stdout=PIPE,
            text=True
        )
    
def text_handler(todo_items, max_character_length):

    title = f"To Do List ({date.today()})\n{'—'*11}\n"

    items = [line.strip() for line in todo_items.splitlines() if line.strip()]
    out = []
    for i, item in enumerate(items):
        p = f"({i+1}) "
        wrapped = wrap(item,
                                width=max_character_length,
                                break_long_words=False,
                                break_on_hyphens=False) or ['']
        out.append(p + wrapped[0])
        indent = ' ' * len(p)
        out.extend(indent + w for w in wrapped[1:])

    return title + "\n".join(out)
