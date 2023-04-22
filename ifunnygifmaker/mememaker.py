import os
import textwrap
from typing import Optional

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


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

    def __calculate_fontsize(self, text, font_name, rect_len, rect_width, wrap):
        font_val = 0
        font = ImageFont.truetype(font_name, font_val)
        length_ratio = 0
        height_ratio = 0

        while length_ratio < 0.85 and height_ratio < 0.85:
            text_lines = textwrap.wrap(text, wrap)
            line_heights = []
            max_line_width = 0
            for line in text_lines:
                line_size = font.getsize(line)
                line_heights.append(line_size[1])
                if line_size[0] > max_line_width:
                    max_line_width = line_size[0]
            text_width = max_line_width
            text_height = sum(line_heights)
            length_ratio = text_width / rect_width
            height_ratio = text_height / rect_len
            font_val += 1
            font = ImageFont.truetype(font_name, font_val)

        return font_val

    def __edit_gif(self, text: str):
        font_path = os.path.join(
            os.path.dirname(__file__), "fonts", "Futura Condensed Extra Bold.otf"
        )

        # Open the GIF file
        with Image.open("found.gif") as im:
            # Loop over all the frames in the GIF
            frames = []
            for frame in range(im.n_frames):
                im.seek(frame)

                # Create a new image with the required dimensions for each frame
                padding_size = 85
                new_im = Image.new("RGB", (im.width, im.height + padding_size), "white")

                # Paste the original GIF image onto the new image
                new_im.paste(im, (0, 100))

                # Create a drawing object
                draw = ImageDraw.Draw(new_im)

                # Define the font for the text
                font = ImageFont.truetype(font_path, 15)

                # Get the size of the text
                text_size = draw.textsize(text, font=font)

                # Calculate the position for the text
                text_y = ((padding_size - 50) - text_size[1]) // 2
                wrap = new_im.width * 0.1
                size = self.__calculate_fontsize(
                    text=text,
                    rect_len=padding_size,
                    rect_width=new_im.width,
                    wrap=wrap,
                    font_name=font_path,
                )

                # Define the font for the text
                font = ImageFont.truetype(font_path, size)

                # Draw the text on the rectangle
                text_lines = textwrap.wrap(text, width=wrap)
                for line in text_lines:
                    line_size = draw.textsize(line, font=font)  # draw the text
                    line_x = (new_im.width - line_size[0]) // 2
                    draw.text((line_x, text_y), line, font=font, fill=0)
                    text_y += line_size[1]

                # Add the new frame to the list
                frames.append(new_im)

            # Save the new GIF with all its frames
            frames[0].save(
                "out.gif",
                save_all=True,
                append_images=frames[1:],
                duration=im.info["duration"],
                loop=0,
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
        self.__edit_gif(text)
        self.__clean_up()
