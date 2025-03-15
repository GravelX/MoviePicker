import os
import omdb
import secrets
import requests

# 1000 requests per day limit, so don't spam the API
DOWNLOAD_POSTERS = False
VERBOSE = False

def create_movie_object(data, category, save_path):
    movie = {}
    method = 0 # 0 = omdb.get, 1 = omdb.search, 2 = placeholder
    # Basic info
    movie['title'], movie['year'] = [text.strip() for text in data.split('\t')]
    movie['category'] = category
    valid_title = movie['title'].replace(" ","_")
    valid_title = valid_title.replace(":","")
    movie['poster_file'] = os.path.join(save_path, valid_title + '.jpg')
    # Get movie poster URL
    if DOWNLOAD_POSTERS:
        client = omdb.OMDBClient(apikey=secrets.API_KEY)
        res = client.get(title=movie['title'].replace(":",""), year=movie['year'], fullplot=False, tomatoes=False)
        if VERBOSE:
            print(f"Getting data for {movie['title']} ({movie['year']})")
            print("First attempt - Get()")
            print(res)
        # if the response is empty, try using a search query instead
        if res == {}:
            res = client.search(movie['title'].replace(":",""), timeout=5)
            method = 1
            if VERBOSE:
                print("Couldn't find movie data with Get() (inexact title). Trying Search()")
                print("First attempt - Search()")
                print(res)
        # if we tried using search
        if method == 1:
            # if the response is still empty, set the poster to a default image
            if res == []:
                method = 2
                if VERBOSE:
                    print("Couldn't find movie poster using Search() either.")
                    print("Falling back on placeholder image.")
            # if not, try the get method again but with the correct title
            else:
                real_title = res[0]['title']
                res2 = client.get(title=real_title, year=movie['year'], fullplot=False, tomatoes=False)
                if VERBOSE:
                    print("Second attempt - Get() but using exact title found via search:", real_title)
                    print(res2)
                # if it worked this time, use the new response
                if res2 != {}:
                    res = res2
                    method = 0
                    if VERBOSE:
                        print("Successfully found movie data with Get() using exact title.")
                        print(res)
                else:
                    # if the get() method still failed, check if the poster URL is in the search response
                    if 'poster' in res[0]:
                        method = 1
                        if VERBOSE:
                            print("Failed to find movie data with Get() using exact title, but poster URL was found in Search() response.")
                    else:
                        method = 2
                        if VERBOSE:
                            print("Failed to find movie data with Get() using exact title, and poster URL was not found in Search() response. Falling back on placeholder image.")

        # Grab data with correct method depending on the response
        if VERBOSE:
            print(f"Final method selection: {method}")
        if method == 0:
            movie['poster_url'] = res['poster']
            movie['plot'] = res['plot']
        elif method == 1:
            movie['poster_url'] = res[0]['poster']
            movie['plot'] = 'No plot available.'
        elif method == 2:
            movie['poster_url'] = 'https://placehold.co/300x450.jpg'
            movie['plot'] = 'No plot available.'
        else:
            raise ValueError('What the actual fuck.')

    return movie

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
    
    return movie_data

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

def LOAD_DATA():
    # Dummy data for testing
    #'''
    data = []
    data.append({'title': 'Starship Troopers', 'year': '1997', 'category': 'Sci-Fi', 'poster_file': 'C:\\Users\\Kami\\Desktop\\vscode-workspaces\\personnal\\MoviePicker\\data\\sci-fi\\Starship_Troopers.jpg', 'poster_url': 'https://m.media-amazon.com/images/M/MV5BZTNiOGM1ZWUtZTZjZC00OWJmLWE2YzUtZjQ4ODZjZmVlMDU3XkEyXkFqcGc@._V1_SX300.jpg', 'plot': 'Humans in a fascistic, militaristic future do battle with giant alien bugs in a fight for survival.'})
    data.append({'title': 'Planet of the apes', 'year': '1968', 'category': 'Sci-Fi', 'poster_file': 'C:\\Users\\Kami\\Desktop\\vscode-workspaces\\personnal\\MoviePicker\\data\\sci-fi\\Planet_of_the_apes.jpg', 'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjI2NzRkNmQtNTIwZi00ZWMxLThlOGQtMjQ1NjI3MzI5YmIzXkEyXkFqcGc@._V1_SX300.jpg', 'plot': 'An astronaut crew crash-lands on a planet in the distant future where intelligent talking apes are the dominant species, and humans are the oppressed and enslaved.'})
    data.append({'title': 'They Live', 'year': '1988', 'category': 'Sci-Fi', 'poster_file': 'C:\\Users\\Kami\\Desktop\\vscode-workspaces\\personnal\\MoviePicker\\data\\sci-fi\\They_Live.jpg', 'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTQ3MjM3ODU1NV5BMl5BanBnXkFtZTgwMjU3NDU2MTE@._V1_SX300.jpg', 'plot': 'A drifter discovers a pair of sunglasses that allow him to wake up to the fact that aliens have taken over the Earth.'})
    #'''
    #data = get_movie_data(secrets.CATEGORY_PATHS)

    if DOWNLOAD_POSTERS:
        download_images(data)

    return data