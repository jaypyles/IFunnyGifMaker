import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_gif(query):
    response = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key=fmAqviQQ3vt1gGXZt4vrY37EYlV39gJ0&q={query}&limit=1&offset=0&rating=g&lang=en")
    image_url = response.json().get("data")[0].get("images").get("original").get("url")
    image_response = requests.get(image_url)

    with open("found.gif", "wb") as f:
        f.write(image_response.content)

def calculate_fontsize(draw, text, font_name, rect_len, rec_width, text_y, text_x):
    font_val = 0
    font =ImageFont.truetype(font_name, font_val)
    font_ratio = 0
    y = text_y
    rectangle_area = rect_len * rec_width

    while font_ratio < 0.50:
        text_lines = textwrap.wrap(text, 50)
        line_heights = []
        text_y = y
        max_line_width = 0
        for line in text_lines:
            line_size = font.getsize(line)  
            line_heights.append(line_size[1])
            text_y += line_size[1]
            if line_size[0] > max_line_width:
                max_line_width = line_size[0]
        text_width = max_line_width
        text_height = sum(line_heights)
        text_area = text_width * text_height
        font_ratio = text_area/rectangle_area
        font_val += 1
        font = ImageFont.truetype(font_name, font_val)

    return font_val

def edit_gif():
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

            # Define the text to be written on the rectangle
            text = "pizza moment"

            # Define the font for the text
            font = ImageFont.truetype("Futura Condensed Extra Bold.otf", 15)
            
            # Get the size of the text
            text_size = draw.textsize(text, font=font)

            # Calculate the position for the text
            text_x = (new_im.width - text_size[0] - 25) // 2
            text_y = ((padding_size - 50) - text_size[1]) // 2
            size = calculate_fontsize(draw=draw, text=text, rect_len=padding_size, rec_width=new_im.width, font_name="Futura Condensed Extra Bold.otf", text_x=text_x, text_y=text_y) 

            # Define the font for the text
            font = ImageFont.truetype("Futura Condensed Extra Bold.otf", size)

            # Draw the text on the rectangle
            text_lines = textwrap.wrap(text, width= 25)
            line_heights = []
            for line in text_lines:
                line_size = draw.textsize(line, font=font) #draw the text
                line_x = (new_im.width - line_size[0]) // 2
                draw.text((line_x, text_y), line, font=font, fill=0)
                line_heights.append(line_size[1])
                text_y += line_size[1]

            # Add the new frame to the list
            frames.append(new_im)

        # Save the new GIF with all its frames
        frames[0].save(
            "out.gif",
            save_all=True,
            append_images=frames[1:],
            duration=im.info['duration'],
            loop=0,
        )
def clean_up():
    os.remove("found.gif")
    
if __name__ == "__main__":
    create_gif("pizza")
    edit_gif()
    clean_up()
