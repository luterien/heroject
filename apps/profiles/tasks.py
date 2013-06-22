from PIL import Image


def make_square(path=None, size=(200, 200)):
    img = Image.open(path)
    width, height = img.size

    if width > height:
        delta = width - height
        left = int(delta/2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width + upper

    img = img.crop((left, upper, right, lower))
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(path, quality=80)