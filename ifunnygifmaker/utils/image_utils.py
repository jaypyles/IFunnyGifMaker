from typing import Union

from PIL import Image, ImageFont


def determine_dimensions():
    with Image.open("found.gif") as im:
        return (im.width, im.height)


def get_wrapped_text(
    text: str, font: ImageFont.FreeTypeFont, line_length: Union[int, float]
):
    # https://stackoverflow.com/questions/8257147/wrap-text-in-pil
    lines = [""]
    for word in text.split():
        line = f"{lines[-1]} {word}".strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return "\n".join(lines)
