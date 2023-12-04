import apicredentials
import requests


def get_omdbapi_movie_data(movie_list: list):
    """
    This funcion takes a list of movie titles and retrieves information 
    for all movies in the list from the OMDb API. 

    It returns a list of tuples with the following structure:
    (movie title, movie year, rotten tomatoes rating, metascore rating, imdb rating, a list with 3 main actors of the movie)

    If the movie is not found in the API or has any of the desired information missing, 
    it is then added to a list of movies with no information. 
    """
    
    api_key = apicredentials.omdb_apikey
    base_url = "http://www.omdbapi.com/"

    # Put the parameters for the resquest in a dictionary
    params_dict = {"apikey": api_key, "t": ""}

    all_movies_useful_info = []
    movies_with_no_info_found = []
    
    for movie in movie_list: 

        # Define the movie title in the dictionary to the given movie in the list
        params_dict["t"] = movie

        # Get movie data
        response = requests.get(base_url, params=params_dict)
        movie_data = response.json()
        
        try:
            # Gather useful information
            year = movie_data["Year"]
            rotten_rating = (movie_data["Ratings"][1]["Value"]).strip("%")
            metascore_rating = int(movie_data["Metascore"])
            imdb_rating = float(movie_data["imdbRating"])
            actors_list = (movie_data["Actors"]).split(", ")

            # Create a tuple with the movie's useful information
            movie_details = (movie, int(year), int(rotten_rating), metascore_rating, imdb_rating, actors_list)

            all_movies_useful_info.append(movie_details)

        except:
            # Insert movie name into the list of movie with no information found on the API
            movies_with_no_info_found.append(movie)

            
    return all_movies_useful_info



def get_celebrityapi_actors_data(actors_list: list):
    """
    This function takes a list of actors and retrieve information about those actors
    from the celebrity API. 

    It returns a list of tuples, where each tutple has the following information: 
    (actor's name, age, gender, birthday, net worth, is it alive? True or False),
    Also returns a list with the name of all actors that were not found in the API.
    """

    apikey = apicredentials.celebrity_apikey

    actors_useful_information = []
    actors_not_found = []

    # Get the actors data from the API
    for actor in actors_list:
        url = 'https://api.api-ninjas.com/v1/celebrity?name={}'.format(actor)
        response = requests.get(url, headers={'X-Api-Key': apikey})
        actor_data = response.json()
        

        # Make sure the actor information was found
        try:
            actor_info = actor_data[0]
            # Extract the useful data
            net_worth = actor_info["net_worth"]
            gender = actor_info["gender"]
            birthday = actor_info["birthday"]
            age = actor_info["age"]
            is_alive = actor_info["is_alive"]


            # Create a tuple with all actor's useful details
            actor_details = (actor, age, gender, birthday, net_worth, is_alive)

            # Add all actors tuples to a list
            actors_useful_information.append(actor_details)

        # Keep track of the actors that were not found in the API
        except:
            actors_not_found.append(actor)   

        
    return actors_useful_information, actors_not_found

