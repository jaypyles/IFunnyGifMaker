import logging
import os
import textwrap
from typing import Optional

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from utils.image_utils import determine_dimensions

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger()


class Meme:
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
            LOG.info("Created meme.")
        else:
            image_response = requests.get(url)
            with open("found.gif", "wb+") as f:
                f.write(image_response.content)
            LOG.info("Created meme.")

    def __add_text_box_to_gif(
        self,
        input_gif_path,
        output_gif_path,
        text,
        font_size=36,
        text_color=(255, 255, 255),
        bg_color=(0, 0, 0),
    ):
        font_path = os.path.join(
            os.path.dirname(__file__), "fonts", "Futura Condensed Extra Bold.otf"
        )

        # Open the GIF image
        gif = Image.open(input_gif_path)

        # Get the width and height of the GIF image
        width, height = gif.size

        # Create a new blank image with the same dimensions as the GIF
        text_image = Image.new("RGBA", (width, font_size + 10), bg_color)

        # Create a drawing context for the text image
        draw = ImageDraw.Draw(text_image)

        # Load a font (you may need to adjust the path to the font file)
        font = ImageFont.truetype(font_path, font_size)

        # Calculate text size and position to center it at the top of the text image
        text_width, text_height = draw.textsize(text, font=font)
        text_x = (width - text_width) // 2
        text_y = (
            gap - text_height
        ) // 2  # Adjust the 'gap' parameter to control the space between the image and text

        # Draw the text on the text image
        draw.text((text_x, text_y), text, fill=text_color, font=font)

        # Iterate through each frame of the GIF
        frames_with_text = []
        for frame in ImageSequence.Iterator(gif):
            # Create a new image with the text above the frame
            frame_with_text = Image.new(
                "RGBA", (width, height + font_size + gap), bg_color
            )
            frame_with_text.paste(frame, (0, font_size + gap))
            frame_with_text.paste(text_image, (0, 0))

            # Append the modified frame to the list
            frames_with_text.append(frame_with_text)

        # Save the modified GIF image with the text on each frame
        frames_with_text[0].save(
            output_gif_path,
            format="GIF",
            save_all=True,
            append_images=frames_with_text[1:],
        )

        def __clean_up(self):
            os.remove("found.gif")

    def make_meme(self):
        self.__create_gif(query="woof")
        input_gif_path = "found.gif"
        output_gif_path = "modified.gif"
        text_to_add = "Your centered text here"

        self.__add_text_box_to_gif(input_gif_path, output_gif_path, text_to_add)

        self.__clean_up()


# Example usage:
load_dotenv()
token = os.getenv("TENOR_API_KEY")
meme_engine = Meme(token=token)
text = "Such meme, much wow!"
font_size = 40
text_color = (0, 0, 0)  # White text color

meme_engine.make_meme()
