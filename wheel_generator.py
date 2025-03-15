import math
import os
import data_generator
import utils
from PIL import Image, ImageDraw, ImageFont
from random import sample

# --- GENERAL PARAMS ---
SIZE = 800
INNER_BORDERS_COLOR = (237, 193, 62)
OUTER_BORDER_COLOR = (82, 34, 13)
TEXT_COLOR = (33, 32, 31)
WHEEL_BG_COLOR = (0, 0, 0)
INNER_BORDER_W = 1
OUTER_BORDER_W = 15
BACKGROUND_COLOR = (0,0,0,0) # transparent
PADDING = 2
MAX_TITLE_LENGTH = 50
SPACING_FROM_CENTER = 90
FONT_SIZE = 15

def draw_rotated_text(image, font, text, angle, x, y):
    txt = Image.new(image.mode, font.getbbox(text)[-2:])
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, font=font, fill=(10, 10, 10), anchor='lt')
    txt = txt.rotate(angle, expand=1)
    image.paste(txt, (int(x - txt.width/2), int(y - txt.height/2)), txt)

def generate_wheel(movies):
    nb_sectors = len(movies)
    poster_width = (int(SIZE / nb_sectors)) - 10
    xy_main = (0+PADDING, 0+PADDING, SIZE-PADDING, SIZE-PADDING)
    xy_pie = (0+PADDING+OUTER_BORDER_W, 0+PADDING+OUTER_BORDER_W, SIZE-PADDING-OUTER_BORDER_W, SIZE-PADDING-OUTER_BORDER_W)
    pieslice_offset = 360 / nb_sectors
    # Load color palette
    colors = sample(utils.COLORS, nb_sectors)
    # font for movie titles
    f = ImageFont.load_default(size=FONT_SIZE)

    wheel = Image.new('RGBA', (SIZE, SIZE), color = BACKGROUND_COLOR)
    draw = ImageDraw.Draw(wheel)
    # Draw the wheel
    # xy: top-left and bottom-right coordinates of the bounding box for creating the circle
    draw.ellipse(xy = xy_main,
                fill = WHEEL_BG_COLOR,
                outline = OUTER_BORDER_COLOR,
                width = OUTER_BORDER_W)
    # Draw the sectors
    for i, m in enumerate(movies):
        #print(f"Drawing sector {i+1}/{nb_sectors}")
        #print("Drawing pieslice from", (i * pieslice_offset) - (pieslice_offset //  2) if i != 0 else 360 - (pieslice_offset //  2), "degrees to", (i * pieslice_offset) + (pieslice_offset //  2), "degrees")
        draw.pieslice(xy = xy_pie,
                      start = (i * pieslice_offset) - (pieslice_offset /  2) if i != 0 else 360 - (pieslice_offset /  2),
                      end = (i * pieslice_offset) + (pieslice_offset /  2),
                      fill = colors[i],
                      outline = INNER_BORDERS_COLOR,
                      width = INNER_BORDER_W)
        # Draw the titles
        title_text = m['title'] + " (" + m['year'] + ")"
        title_text = title_text if len(title_text) < MAX_TITLE_LENGTH else title_text[:MAX_TITLE_LENGTH] + '...'
        # Here, for the last 2 params, give a point further from the center along the sector's axis
        x = int(SIZE / 2) + (SPACING_FROM_CENTER + int(len(title_text)/MAX_TITLE_LENGTH*150)) * math.cos(math.radians(i * pieslice_offset))
        y = int(SIZE / 2) + (SPACING_FROM_CENTER + int(len(title_text)/MAX_TITLE_LENGTH*150)) * math.sin(math.radians(i * pieslice_offset))
        draw_rotated_text(wheel, f, title_text, 360-(i * pieslice_offset), x, y)
    # Save the wheel once
    save_path = os.path.dirname(movies[0].get('poster_file'))
    wheel.save(os.path.join(save_path, 'wheel.png'), "PNG")
    # Draw the movie posters in the sectors
    # Save the wheel again
    wheel.show()

def GENERATE_WHEELS():
    movies = data_generator.LOAD_DATA()
    if len(movies) == 0: 
        raise ValueError("No data found to generate wheels.")

    # Collect all the categories
    categories = []
    for movie in movies:
        if movie['category'] not in categories:
            categories.append(movie['category'])

    # Split the movies into different lists based on their category
    category_movies = {}
    for category in categories:
        category_movies[category] = [movie for movie in movies if movie['category'] == category]
    
    # Generate the wheels
    for category in category_movies:
        generate_wheel(category_movies[category])    

GENERATE_WHEELS()