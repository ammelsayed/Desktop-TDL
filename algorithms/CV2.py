import cv2
import os
from functions import set_wallpaper


OpenCVFonts = {
    "Simplex":  cv2.FONT_HERSHEY_SIMPLEX,
    "Duplex":  cv2.FONT_HERSHEY_DUPLEX,
    "Complex":  cv2.FONT_HERSHEY_COMPLEX,
    "Triplex":  cv2.FONT_HERSHEY_TRIPLEX,
    "Script Simples":  cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    "Script Complex":  cv2.FONT_HERSHEY_SCRIPT_COMPLEX
}


def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (b, g, r)

def OpenCVMethod(
    todo_items,
    wallpaper_path, 
    corner, 
    font_name,
    font_size,
    text_color,
    box_color,
    text_box_padding,
    frame_padding,

    ## Newley added:
    thickness,
    line_spacing,

    # System data
    data_folder
    ):

    img = cv2.imread(wallpaper_path)
    img_h, img_w = img.shape[:2]

    # split into lines
    lines = todo_items.split("\n")

    # compute sizes
    sizes = []
    for line in lines:
        (w, h), baseline = cv2.getTextSize(line, font_name, font_size, thickness)
        sizes.append((w, h, baseline))
        
    max_w = max([s[0] for s in sizes])

    # compute total height of all lines including line spacing
    total_text_height = 0
    for i, (w, h, baseline) in enumerate(sizes):
        if i < 2 or i == len(lines)-1:
            total_text_height += h + baseline
        else:
            total_text_height += int(h * line_spacing + baseline)

    # compute rectangle coordinates based on alignment
    if corner == 'Top Left':
        rect_left = frame_padding
        rect_top = frame_padding
    elif corner == 'Top Right':
        rect_left = img_w - (max_w + 2 * text_box_padding) - frame_padding
        rect_top = frame_padding
    elif corner == 'Buttom Left':
        rect_left = frame_padding
        rect_top = img_h - (total_text_height + 2 * text_box_padding) - frame_padding
    elif corner == 'Bottom Right':
        rect_left = img_w - (max_w + 2 * text_box_padding) - frame_padding
        rect_top = img_h - (total_text_height + 2 * text_box_padding) - frame_padding
    elif corner == 'Center':
        rect_left = (img_w - (max_w + 2 * text_box_padding)) // 2
        rect_top = (img_h - (total_text_height + 2 * text_box_padding)) // 2
    else:
        raise ValueError("Invalid alignment option")

    rect_right = rect_left + max_w + 2 * text_box_padding
    rect_bottom = rect_top + total_text_height + 2 * text_box_padding

    # draw rectangle
    cv2.rectangle(img,
                  (rect_left, rect_top),
                  (rect_right, rect_bottom),
                  hex_to_bgr(box_color),
                  -1)

    # compute starting baseline for first line
    y = rect_top + text_box_padding + sizes[0][1]  # top + padding + first line height

    # draw text
    for i, line in enumerate(lines):
        cv2.putText(img, line, (rect_left + text_box_padding, y),
                    font_name, font_size, hex_to_bgr(text_color), thickness, cv2.LINE_AA)
        if i < 2 or i == len(lines)-1:
            y += sizes[i][1] + sizes[i][2]  # normal spacing
        else:
            y += int(sizes[i][1] * line_spacing + sizes[i][2])  # extra spacing for middle lines


    new_img_path = f"{data_folder}output_cv2.png"
    cv2.imwrite(new_img_path, img)

    # # show image (for testing)
    # cv2.namedWindow('text', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('text', 800, 600)
    # cv2.imshow('text', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Apply to desktop
    set_wallpaper(new_img_path)


## Test timing 

# def TestTiming ():

#     import time
#     start = time.time()  # record start time

#     OpenCVMethod(
#         text,
#         img_path, 
#         corner, 
#         font_name,
#         font_size,
#         text_color,
#         box_color,
#         text_box_padding,
#         frame_padding,

#         ## Newley added:
#         thickness,
#         line_spacing,

#         # System data
#         data_folder
#         )

#     end = time.time()  # record end time
#     print(f"Execution time: {end - start:.6f} seconds")
