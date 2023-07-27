from PIL import Image


def determine_dimensions():
    with Image.open("found.gif") as im:
        return (im.width, im.height)
