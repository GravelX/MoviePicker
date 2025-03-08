import os
import omdb
import secrets
import requests

# 1000 requests per day limit, so don't spam the API
DOWNLOAD_POSTERS = True

def create_movie_object(data, category, save_path):
    movie = {}
    # Basic info
    movie['title'], movie['year'] = [text.strip() for text in data.split('\t')]
    movie['category'] = category
    movie['poster_file'] = os.path.join(save_path, movie['title'].replace(" ","_") + '.jpg')
    # Get movie poster URL
    if DOWNLOAD_POSTERS:
        client = omdb.OMDBClient(apikey=secrets.API_KEY)
        res = client.get(title=movie['title'], year=movie['year'], fullplot=False, tomatoes=False)
        print(res)
        movie['poster_url'] = res['poster']

def get_movie_data(file_paths):
    at_least_one = False
    movie_data = []
    for category in file_paths:
        # check if a movie list exists
        if os.path.exists(os.path.join(category, 'movies.txt')):
            with open(os.path.join(category, 'movies.txt'), 'r') as f:
                movies = [movie.strip() for movie in f.readlines()]
            # If the movie list is empty or contains only the category name, skip the category
            if not movies or len(movies) == 1:
                continue
            at_least_one = True
            # remove the first line since it's the name of the category
            category_name = movies.pop(0)
            for movie in movies:
                movie_data.append(create_movie_object(movie, category_name, category))
        else:
            continue
    if not at_least_one:
        raise FileNotFoundError('None of the movie categories have a movie list, or the lists are all empty.')

def download_images(data):
    if DOWNLOAD_POSTERS:
        for movie in data:
            # Check if the poster already exists
            if os.path.exists(movie['poster_file']):
                continue
            # Download the poster
            img_data = requests.get(movie['poster_url']).content
            with open(movie['poster_file'], 'wb') as handler:
                handler.write(img_data)

# --- MAIN ---
def LOAD_DATA():
    # Dummy data for testing
    data = []
    data.append({'title': 'Starship Troopers', 'year': '1997', 'category': 'Sci-Fi', 'poster_file': 'C:\\Users\\Kami\\Desktop\\vscode-workspaces\\personnal\\MoviePicker\\exports\\sci-fi\\Starship_Troopers.jpg', 'poster_url': 'https://m.media-amazon.com/images/M/MV5BZTNiOGM1ZWUtZTZjZC00OWJmLWE2YzUtZjQ4ODZjZmVlMDU3XkEyXkFqcGc@._V1_SX300.jpg'})
    data.append({'title': 'Planet of the apes', 'year': '1968', 'category': 'Sci-Fi', 'poster_file': 'C:\\Users\\Kami\\Desktop\\vscode-workspaces\\personnal\\MoviePicker\\exports\\sci-fi\\Planet_of_the_apes.jpg', 'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjI2NzRkNmQtNTIwZi00ZWMxLThlOGQtMjQ1NjI3MzI5YmIzXkEyXkFqcGc@._V1_SX300.jpg'})
    data.append({'title': 'They Live', 'year': '1988', 'category': 'Sci-Fi', 'poster_file': 'C:\\Users\\Kami\\Desktop\\vscode-workspaces\\personnal\\MoviePicker\\exports\\sci-fi\\They_Live.jpg', 'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTQ3MjM3ODU1NV5BMl5BanBnXkFtZTgwMjU3NDU2MTE@._V1_SX300.jpg'})
    #data = get_movie_data(secrets.CATEGORY_PATHS)

    if DOWNLOAD_POSTERS:
        download_images(data)

LOAD_DATA()