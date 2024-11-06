from PIL import Image

RGBA_LOW_TRANSPARENCY = 20
GRAYSCALE_LOW_TRANSPARENCY = 0

def mask_background_rgba(img:Image.Image,transparency_threshold=RGBA_LOW_TRANSPARENCY):
    mask = Image.new("L",img.size,color=255)
    pixels = img.load()

    for row in range(img.size[0]):
        for col in range(img.size[1]):
            if pixels[row,col][-1] < transparency_threshold:
                mask.putpixel((row,col),0)

    return mask

def mask_background_grayscale(img:Image.Image,transparency_threshold=GRAYSCALE_LOW_TRANSPARENCY):
    mask = Image.new("L",img.size,color=255)
    pixels = img.load()

    for row in range(img.size[0]):
        for col in range(img.size[1]):
            if pixels[row,col] == transparency_threshold:
                mask.putpixel((row,col),0)

    return mask


def mask_background_rgb(img:Image.Image):
    mask = Image.new("L",img.size,color=255)
    pixels = img.load()

    for row in range(img.size[0]):
        for col in range(img.size[1]):
            if pixels[row,col] == (0,0,0):
                mask.putpixel((row,col),0)

    return mask