import data_generator
import utils
from PIL import Image, ImageDraw

# --- GENERAL PARAMS ---
SIZE = 800
INNER_BORDERS_COLOR = (237, 193, 62)
OUTER_BORDERS_COLOR = (82, 34, 13)
TEXT_COLOR = (33, 32, 31)
INNER_BORDER_SIZE = 5
OUTER_BORDER_SIZE = 15
BACKGROUND_COLOR = 'WhiteSmoke'

def generate_wheel(movies):
    for m in movies:
        print(m)

def GENERATE_WHEELS():
    movies = data_generator.LOAD_DATA()
    if movies is None:
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