import apicredentials
import requests


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


def get_celebrityapi_actors_data(actors_list):

    apikey = apicredentials.celebrity_apikey
    #base_url = 'https://api.api-ninjas.com/v1/celebrity?name'

    actors_useful_information = []
    actors_not_found = []

    #Get the actors data from the API
    for actor in actors_list:
        url = 'https://api.api-ninjas.com/v1/celebrity?name={}'.format(actor)
        response = requests.get(url, headers={'X-Api-Key': apikey})
        actor_data = response.json()
        

        #Make sure the actor information was found
        try:
            actor_info = actor_data[0]
            #extract the useful data
            net_worth = actor_info["net_worth"]
            gender = actor_info["gender"]
            birthday = actor_info["birthday"]
            age = actor_info["age"]
            is_alive = actor_info["is_alive"]


            #create a tuple with all actor's useful details
            actor_details = (actor, age, gender, birthday, net_worth, is_alive)

            #Add all actors tuples to a list
            actors_useful_information.append(actor_details)

        #Keep track of the actors that were not found in the API
        except:
            actors_not_found.append(actor)   

        
    return actors_useful_information, actors_not_found

