from PIL import Image, ImageDraw 

DRAWWIDTH = 800
DRAWHEIGHT = 800
LINE_WIDTH = 4
NB_FRUITS = 5
MAP_SIZE = 20
RANDOM_FORCE = 1
NB_TURNS = 5
img = Image.new("RGB", (DRAWWIDTH, DRAWHEIGHT), "white")
ctx = ImageDraw.Draw(img)

for line in range(MAP_SIZE + 1):
    # drawing the line
    ctx.line([
            (5, line * (DRAWHEIGHT // MAP_SIZE)),
            (DRAWWIDTH - 5, line * (DRAWHEIGHT // MAP_SIZE))
            ], fill="black", width=LINE_WIDTH)
    # drawing the columns
    ctx.line([
            (line * (DRAWWIDTH // MAP_SIZE), 5),
            (line * (DRAWWIDTH // MAP_SIZE), DRAWHEIGHT - 5)
            ], fill="black", width=LINE_WIDTH)

img.show()