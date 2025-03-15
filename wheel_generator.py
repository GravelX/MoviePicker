import math
import os
import data_generator
import utils
from PIL import Image, ImageDraw, ImageFont
from random import sample
import json

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
POSTER_WIDTH = 100
MAX_TITLE_LENGTH = 50
TEXT_SPACING_FROM_CENTER = 90
POSTER_SPACING_FROM_CENTER = int((SIZE-PADDING)/2 - TEXT_SPACING_FROM_CENTER)
FONT_SIZE = 15

def draw_rotated_text(image, font, text, angle, x, y):
    txt = Image.new(image.mode, font.getbbox(text)[-2:])
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, font=font, fill=(10, 10, 10), anchor='lt')
    txt = txt.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    image.paste(txt, (int(x - txt.width/2), int(y - txt.height/2)), txt)

def generate_wheel(movies):
    nb_sectors = len(movies)
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
    # Draw the sectors on the wheel
    for i, m in enumerate(movies):
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
        x = int((SIZE / 2) + (TEXT_SPACING_FROM_CENTER + (len(title_text)/MAX_TITLE_LENGTH*150)) * math.cos(math.radians(i * pieslice_offset)))
        y = int((SIZE / 2) + (TEXT_SPACING_FROM_CENTER + (len(title_text)/MAX_TITLE_LENGTH*150)) * math.sin(math.radians(i * pieslice_offset)))
        draw_rotated_text(wheel, f, title_text, 360-(i * pieslice_offset), x, y)
    # Save the wheel once
    save_path = os.path.dirname(movies[0].get('poster_file'))
    wheel.save(os.path.join(save_path, 'wheel.png'), "PNG")
    # Draw the movie posters in the sectors
    poster_width = POSTER_WIDTH
    # If there are too many movies, reduce the poster width to fit the pie slice
    slice_width = 2 * POSTER_SPACING_FROM_CENTER * math.tan(math.radians(pieslice_offset / 2))
    if poster_width > slice_width:
        poster_width = int(pieslice_offset / 0.3)

    for i, m in enumerate(movies):
        # Load poster
        poster = Image.open(m['poster_file']).convert("RGBA")
        # Transform the poster to fit the sector
        angle = 360-(i * pieslice_offset)
        w, h = poster.size
        poster = poster.resize((poster_width, int(poster_width * h / w)))
        # Rotate the poster around its center
        poster = poster.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC, fillcolor=BACKGROUND_COLOR)
        # Calculate the position to paster the poster so that it is centered
        # Calculate the position to paste the poster so that it is centered
        x = int((SIZE / 2) + POSTER_SPACING_FROM_CENTER * math.cos(math.radians(i * pieslice_offset)) - poster.width / 2)
        y = int((SIZE / 2) + POSTER_SPACING_FROM_CENTER * math.sin(math.radians(i * pieslice_offset)) - poster.height / 2)
        # Paste the poster
        wheel.paste(poster, (x, y), poster)
    # Save the wheel again but with posters
    wheel.save(os.path.join(save_path, 'wheel_posters.png'), "PNG")

def export_wheel_data(movies):
    # Export all the movie data into JSON, adding their corresponding angle on the wheel into the data.
    wheel_data = []
    nb_sectors = len(movies)#
    pieslice_offset = 360 / nb_sectors

    for i, m in enumerate(movies):
        angle = (i * pieslice_offset) - (pieslice_offset / 2) if i != 0 else 360 - (pieslice_offset / 2)
        movie_data = m.copy()
        movie_data['angle'] = angle
        wheel_data.append(movie_data)

    save_path = os.path.dirname(movies[0].get('poster_file'))
    with open(os.path.join(save_path, 'wheel_data.json'), 'w') as f:
        json.dump(wheel_data, f, indent=4)

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
    
    # For every category of movies
    for category in category_movies:
        # Generate and save the wheels
        generate_wheel(category_movies[category])
        # Export the wheel data to JSON
        export_wheel_data(category_movies[category])

GENERATE_WHEELS()