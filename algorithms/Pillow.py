import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from functions import set_wallpaper

img_path = "E:/Gallary/wallpapers/milkyway.jpg"

text = "Hello World! 你好！"

pos = (200, 300)  

img = cv2.imread(img_path)

if img is None:
    print("Error: can't read", img_path); sys.exit(1)

img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 40)

draw = ImageDraw.Draw(img_pil)

text = "你好，世界"
pos = (50, 200)

# draw rectangle
bbox = draw.textbbox(pos, text, font=font)
draw.rectangle(bbox, fill=(255,255,255))  # background box

# draw text
draw.text(pos, text, font=font, fill=(0,0,0))


# # Font settings
# font_path = "C:/Windows/Fonts/simhei.ttf"
# ft2 = cv2.freetype.createFreeType2()
# ft2.loadFontData(fontFileName=font_path, id=0)


# font_scale = 10.0

# color = (0, 0, 0)    # B,G,R

# fontHeight = 50

# thickness=-1

# # (x,y) is the bottom-left corner of the text (OpenCV convention)
# ft2.putText(img, text, (x, y), fontHeight, color, thickness, cv2.LINE_AA)

# # Drawing the 
# (w, h), baseline = ft2.getTextSize(text, fontHeight, thickness)
# cv2.rectangle(img, (pos[0], pos[1]-h-baseline), (pos[0]+w, pos[1]+baseline), (255,255,255), thickness)


img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

cv2.imwrite("out.png", img)

print("Saved out.png")
