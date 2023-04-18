import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
ALLIGNMENT_LEFT = 0
ALLIGNMENT_CENTER = 1 
ALLIGNMENT_RIGHT = 2
ALLIGNMENT_TOP = 3
ALLIGNMENT_BOTTOM = 4
def text_box(text, image_draw, font, box, horizontal_allignment = ALLIGNMENT_LEFT, vertical_allignment = ALLIGNMENT_TOP, **kwargs):
    x = box[0]
    y = box[1]
    width = box[2]
    height = box[3]
    lines = text.split('\n')
    true_lines = []
    for line in lines:
        if font.getsize(line)[0] <= width:
            true_lines.append(line) 
        else:
            current_line = ''
            for word in line.split(' '):
                if font.getsize(current_line + word)[0] <= width:
                    current_line += ' ' + word 
                else:
                    true_lines.append(current_line)
                    current_line = word 
            true_lines.append(current_line)
    
    x_offset = y_offset = 0
    lineheight = font.getsize(true_lines[0])[1] * 1.2 # Give a margin of 0.2x the font height
    if vertical_allignment == ALLIGNMENT_CENTER:
        y = int(y + height / 2)
        y_offset = - (len(true_lines) * lineheight) / 2
    elif vertical_allignment == ALLIGNMENT_BOTTOM:
        y = int(y + height)
        y_offset = - (len(true_lines) * lineheight)
    
    for line in true_lines:
        linewidth = font.getsize(line)[0]
        if horizontal_allignment == ALLIGNMENT_CENTER:
            x_offset = (width - linewidth) / 2
        elif horizontal_allignment == ALLIGNMENT_RIGHT:
            x_offset = width - linewidth
        image_draw.text(
            (int(x + x_offset), int(y + y_offset)),
            line,
            font=font,
            **kwargs
        )
        y_offset += lineheight

# helper function for fonts
def font(font_path, size=12):
    return ImageFont.truetype(font_path, size=size, encoding="unic")
# response = requests.get("https://api.giphy.com/v1/gifs/search?api_key=fmAqviQQ3vt1gGXZt4vrY37EYlV39gJ0&q=gary&limit=25&offset=0&rating=g&lang=en")
# image_url = response.json().get("data")[0].get("images").get("original").get("url")
# image_response = requests.get(image_url)
#
# with open("test_gif.gif", "wb") as f:
#     f.write(image_response.content)

# Open the GIF file
with Image.open("test_gif.gif") as im:
    # Loop over all the frames in the GIF
    frames = []
    for frame in range(im.n_frames):
        im.seek(frame)

        # Create a new image with the required dimensions for each frame
        new_im = Image.new("RGB", (im.width, im.height + 100), (255, 255, 255))
        # Paste the original GIF image onto the new image
        new_im.paste(im, (0, 100))

        # Create a drawing object
        draw = ImageDraw.Draw(new_im)

        # Define the text to be written on the rectangle
        text = "woah this is crazy i think this text shpould be wrappoing now"

        # Define the font for the text
        font = ImageFont.truetype("Futura Condensed Extra Bold.otf", 24)
        
        # Get the size of the text
        text_size = draw.textsize(text, font=font)
        
        # Calculate the position for the text
        text_x = (im.width - text_size[0]) // 2
        text_y = (100 - text_size[1]) // 2
        
        # Draw the text on the rectangle
        text_lines = textwrap.wrap(text, width=40)
        line_heights = []
        for line in text_lines:
            line_size = draw.textsize(line, font=font)
            line_x = (im.width - line_size[0]) // 2
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
