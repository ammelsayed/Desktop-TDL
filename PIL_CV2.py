from cv2 import imread, imwrite, cvtColor, rectangle, COLOR_RGB2BGR, COLOR_BGR2RGB
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from functions import set_wallpaper

WindowsFonts = {
    'Arial'   :   'C:\Windows\Fonts\\arial.ttf',
    "Calibri" : "C:\\Windows\\Fonts\\Calibri.ttf",
    'Comic'   :   'C:\Windows\Fonts\comic.ttf',
    'Impact'   :   'C:\Windows\Fonts\impact.ttf',
    'Monbaiti'   :   'C:\Windows\Fonts\monbaiti.ttf',
    'Segoesc'   :   'C:\Windows\Fonts\segoesc.ttf',
    'Simfang' :  'C:\Windows\Fonts\simfang.ttf',
    'Simhei' : 'C:\Windows\Fonts\simhei.ttf',
    'Simkai' : 'C:\Windows\Fonts\simkai.ttf',
    'Tahoma'   :   'C:\Windows\Fonts\\tahoma.ttf',
    'Taile'   :   'C:\Windows\Fonts\\taile.ttf',
    'Times'   :   'C:\Windows\Fonts\\times.ttf',
}


DebianUbuntuFonts = {
    'Arial': '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # Closest to Arial
    'Comic': '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # No direct Comic Sans equivalent, using Sans as fallback
    'Impact': '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',  # No direct Impact equivalent, using bold Sans
    'Monbaiti': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',  # Monospace fallback
    'Segoesc': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Fallback to Sans
    'Simfang': '/usr/share/fonts/truetype/arphic/ukai.ttf',  # Chinese fallback (AR PL UKai)
    'Simhei': '/usr/share/fonts/truetype/arphic/uming.ttf',  # Chinese fallback (AR PL UMing)
    'Simkai': '/usr/share/fonts/truetype/arphic/ukai.ttf',  # Chinese fallback (AR PL UKai)
    'Tahoma': '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # Closest to Tahoma
    'Taile': '/usr/share/fonts/truetype/arphic/uming.ttf',  # Chinese/Thai fallback
    'Times': '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',  # Closest to Times New Roman
}


def hex_to_bgr(hex_color):
    """Convert hex color to BGR tuple"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (b, g, r)

def MixedMethod(
    todo_items,
    wallpaper_path, 
    corner, 
    font_name,
    font_size,
    text_color,
    box_color,
    frame_padding,
    text_box_padding,
    line_spacing,
    font_weight,
    data_folder
):
    # Load image
    img = imread(wallpaper_path)
    img_h, img_w = img.shape[:2]


    # Split into lines
    lines = todo_items.split("\n")

    # Convert to PIL
    pil_img = Image.fromarray(cvtColor(img, COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype(font_name, font_size)

    # Measure text sizes (width, height, baseline) like OpenCV
    sizes = []
    ascent, descent = font.getmetrics() 
    for line in lines:
        l, t, r, b = draw.textbbox((0, 0), line, font=font)
        w = r - l
        h = ascent  # height above baseline
        baseline = descent  # part below baseline
        sizes.append((w, h, baseline))

    max_w = max([s[0] for s in sizes])

    # Compute total text height including line spacing (mimics OpenCV behavior)
    total_text_height = 0
    for i, (w, h, baseline) in enumerate(sizes):
        if i < 2 or i == len(lines) - 1:
            total_text_height += h + baseline
        else:
            total_text_height += int(h * line_spacing + baseline)

    # Box coordinates (same as OpenCV-only version)
    if corner == 'Top Left':
        rect_left = frame_padding
        rect_top = frame_padding
    elif corner == 'Top Right':
        rect_left = img_w - (max_w + 2*text_box_padding) - frame_padding
        rect_top = frame_padding
    elif corner == 'Buttom Left':
        rect_left = frame_padding
        rect_top = img_h - (total_text_height + 2*text_box_padding) - frame_padding
    elif corner == 'Bottom Right':
        rect_left = img_w - (max_w + 2*text_box_padding) - frame_padding
        rect_top = img_h - (total_text_height + 2*text_box_padding) - frame_padding
    elif corner == 'Center':
        rect_left = (img_w - (max_w + 2*text_box_padding)) // 2
        rect_top = (img_h - (total_text_height + 2*text_box_padding)) // 2
    else:
        raise ValueError("Invalid alignment option")

    rect_right = rect_left + max_w + 2*text_box_padding
    rect_bottom = rect_top + total_text_height + 2*text_box_padding

    # Draw background rectangle with OpenCV
    img = cvtColor(np.array(pil_img), COLOR_RGB2BGR)

    # draw rectangle
    rectangle(img,
                  (rect_left, rect_top),
                  (rect_right, rect_bottom),
                  hex_to_bgr(box_color),
                  -1)



    y = rect_top + text_box_padding + ascent  # top + padding + ascent of first line

    # Back to Pillow for text
    pil_img = Image.fromarray(cvtColor(img, COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    for i, line in enumerate(lines):
        w, h, baseline = sizes[i]  
        draw.text((rect_left + text_box_padding, y - h), line,
                  font=font, fill=tuple(reversed(hex_to_bgr(text_color))),
                  stroke_width=font_weight, stroke_fill=tuple(reversed(hex_to_bgr(text_color))),)

        # Move y for next line
        if i < 2 or i == len(lines) - 1:
            y += h + baseline  # ascent + descent
        else:
            y += int(h * line_spacing + baseline) 

    # Convert back to OpenCV
    img = cvtColor(np.array(pil_img), COLOR_RGB2BGR)
    new_img_path = f"{data_folder}output.png"
    imwrite(new_img_path, img)

    # Apply to desktop
    set_wallpaper(new_img_path)
