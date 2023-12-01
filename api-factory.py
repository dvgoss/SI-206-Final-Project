import apicredentials
import requests
#import os


#get movie data from OMDb API for all the movies in a list 
def get_omdbapi_movie_data(movie_list):
    
    api_key = apicredentials.omdb_apikey
    base_url = "http://www.omdbapi.com/"

    #put the parameters for the resquest in a dictionary
    params_dict = {"apikey": api_key, "t": ""}

    all_movies_useful_info = []
    movies_with_no_info_found = []
    
    for movie in movie_list: 

        #define the movie title in the dictionary to the given movie in the list
        params_dict["t"] = movie

        #get movie data
        response = requests.get(base_url, params=params_dict)
        movie_data = response.json()
        
        try:
            #gather useful information
            year = movie_data["Year"]
            rotten_rating = (movie_data["Ratings"][1]["Value"]).strip("%")
            metascore_rating = int(movie_data["Metascore"])
            imdb_rating = float(movie_data["imdbRating"])
            actors_list = (movie_data["Actors"]).split(", ")

            #create a tuple with the movie's useful information
            movie_details = (movie, int(year), int(rotten_rating), metascore_rating, imdb_rating, actors_list)

        except:
            #insert movie name into the list of movie with no information found on the API
            movies_with_no_info_found.append(movie)

        all_movies_useful_info.append(movie_details)
            
    return all_movies_useful_info







#get_omdbapi_movie_data(["The Godfather", 'Mean Girls'])