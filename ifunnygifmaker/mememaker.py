import os
from typing import Optional

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageSequence

from ifunnygifmaker.utils.image_utils import get_wrapped_text

FONT_PATH = os.path.join(
    os.path.dirname(__file__), "fonts", "Futura Condensed Extra Bold.otf"
)
FONT_SIZE = 38
PADDING = 0.1


class MemeMaker:
    def __init__(self, token):
        """
        An engine for making memes
        :token: your tenor api token
        """
        self.token = token

    def __create_gif(self, query: Optional[str] = None, url: Optional[str] = None):
        if url is None:
            tenor_key = self.token
            response = requests.get(
                f"https://tenor.googleapis.com/v2/search?q={query}&key={tenor_key}"
            )
            image_url = (
                response.json()
                .get("results")[0]
                .get("media_formats")
                .get("gif")
                .get("url")
            )

            image_response = requests.get(image_url)

            with open("found.gif", "wb+") as f:
                f.write(image_response.content)
        else:
            image_response = requests.get(url)
            with open("found.gif", "wb+") as f:
                f.write(image_response.content)

    def __add_text(self, text, gif_path, font_path, font_size, output_path):
        gif = Image.open(gif_path)
        frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

        gif_width, gif_height = gif.size
        modified_frames = []

        # Define padding for the text box
        padding_width = PADDING * gif_width

        # generate temporary image to determine text size
        temp_img = Image.new("RGBA", gif.size)
        temp_draw = ImageDraw.Draw(temp_img)

        # generate font
        font = ImageFont.truetype(font_path, font_size)
        font_color = (0, 0, 0)  # Black text color (adjust if needed)

        # Generate text block (modify this logic based on your requirements)
        text = text
        wrapped_text = get_wrapped_text(text, font, temp_img.width - padding_width)
        _, text_height = temp_draw.textsize(wrapped_text, font)

        white_box_padding = PADDING + 0.1

        for frame in frames:
            # Create a new image with the required dimensions (adjusted for extra space on top)
            new_img = Image.new(
                "RGBA",
                (
                    gif_width,
                    gif_height + (text_height + int(text_height * white_box_padding)),
                ),
                (255, 255, 255, 255),
            )

            # Prepare text overlay on the transparent image
            trans_image = Image.new("RGBA", new_img.size, (0, 0, 0, 0))
            draw_text = ImageDraw.Draw(trans_image)

            # Calculate the size of the white box based on the text
            white_box_width, white_box_height = draw_text.textsize(
                wrapped_text, font=font
            )

            # Create white image that is the size of the text
            white_image = Image.new(
                "RGBA",
                (
                    int(white_box_width + int(white_box_width * white_box_padding)),
                    int(white_box_height + int(white_box_height * white_box_padding)),
                ),
                (255, 255, 255, 255),
            )
            white_draw = ImageDraw.Draw(
                white_image
            )  # Create a new ImageDraw object for the white image

            # Draw the text on the white image
            white_draw.multiline_text(
                (0, 0),
                wrapped_text,
                font=font,
                fill=font_color,
                align="center",
            )

            # Combine the transparent image with the current frame and the white box
            new_img.paste(white_image, (int((gif_width - white_box_width) / 2), 0))
            new_img.paste(
                frame, (0, text_height + int(text_height * white_box_padding))
            )  # Paste the original frame below the white box

            # Add the new frame to the list of modified frames
            modified_frames.append(new_img)

        # Save the modified frames as a new GIF
        modified_frames[0].save(
            output_path,
            format="GIF",
            save_all=True,
            append_images=modified_frames[1:],
            duration=gif.info["duration"],
            loop=gif.info.get("loop", 0),
        )

    def __clean_up(self):
        os.remove("found.gif")

    def make_meme(
        self, text: str, query: Optional[str] = None, url: Optional[str] = None
    ):
        load_dotenv()
        if query is None:
            query = text.replace(" ", "+")
        if query is not None and url is not None:
            query = None
        if query is not None:
            query = query.replace(" ", "+")
        self.__create_gif(query=query, url=url)
        self.__add_text(text, "found.gif", FONT_PATH, FONT_SIZE, "out.gif")
        self.__clean_up()


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TENOR_API_KEY")
    m = MemeMaker(token)
    m.make_meme(text="")
