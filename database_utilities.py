import sqlite3
import os
import api_factory
import get_movies_list


def setup_database_connection(database_name: str):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + database_name)
    cur = conn.cursor()
    return cur, conn

def setup_all_tables(cur, conn):

    # Create Movies table
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (movie_id INTEGER PRIMARY KEY, title TEXT UNIQUE, year INTEGER, rotten_tomatoes FLOAT, metascore FLOAT, imdb FLOAT)")
    
    # Create Actors table
    cur.execute("CREATE TABLE IF NOT EXISTS Actors (actor_id INTEGER PRIMARY KEY, name TEXT UNIQUE, age INTEGER, gender TEXT, birthday TEXT, net_worth NUMERIC, is_alive INTEGER)")
    
    # Create Movies_Actors table
    cur.execute("CREATE TABLE IF NOT EXISTS Movies_and_Actors (movie_actor_combination_id INTEGER PRIMARY KEY, movie_id INTEGER, actor_id INTEGER)")

    conn.commit()

# Expects a movie_data is a list with no duplicates, and that movie_data remains the same across multiple runs
def add_omdbapi_data_to_database(movie_data: list, cur, conn):

    # Check length of Movies table to gather new Movies from the given list
    cur.execute("SELECT COUNT(*) FROM Movies")
    start_index = (cur.fetchone())[0]
    end_index = start_index + 3

    # Loop 3 times to gather 3 new movies information since it will add a total of 21 new items in the database
    for x in range(start_index, end_index):

        # Check if we already iterated through the entire list of movies_data
        if start_index >= len(movie_data):

            print("We collected all movies already!")
            # Finish the program
            break
         
        else:
            # Insert movie information into the Movies table in the database
            movie_info = movie_data[x]
            title, year, rotten_tomatoes, metascore, imdb, actors = movie_info
            cur.execute("INSERT OR IGNORE INTO Movies (title, year, rotten_tomatoes, metascore, imdb) VALUES (?,?,?,?,?)", (title, year, rotten_tomatoes, metascore, imdb))

            # Get movie_id from Movies table
            cur.execute("SELECT movie_id FROM Movies WHERE title = (?)", (title,))
            movie_id = (cur.fetchone())[0]
                
            # Insert each actor to the actors table
            for actor in actors:
                cur.execute("INSERT OR IGNORE INTO Actors (name) VALUES (?)", (actor,))

                # Get actor_id from the Actors table
                cur.execute("SELECT actor_id FROM Actors WHERE name = (?)", (actor,))
                actor_id = (cur.fetchone())[0]

                # Insert data into the Movies_and_Actors table
                cur.execute("INSERT OR IGNORE INTO Movies_and_Actors (movie_id, actor_id) VALUES (?,?)", (movie_id, actor_id))
            
            conn.commit()
        conn.commit()


def get_last_actors_id(cur):

    # Collect the last actor_id from Actors table to litmit new data entry
    cur.execute("SELECT * FROM Actors WHERE actor_id=(SELECT max(actor_id) FROM Actors)")
    last_actor_info = (cur.fetchone())

    if last_actor_info != None:
        last_actor_id = last_actor_info[0]
    
    # If there's no data in the Actors table, set the index to zero
    else:
        last_actor_id = 0

    return last_actor_id


def add_celebrityapi_data_to_database(index: int, cur, conn):

    # Gather all actors that were added to the database in the current run
    cur.execute("SELECT name FROM Actors WHERE actor_id > (?)", (index,))
    all_actors_rows = cur.fetchall()

    # Create a list of actors to request data from the celebrity API
    list_of_actors = []
    for row in all_actors_rows:
        actor_name = row[0]

        list_of_actors.append(actor_name)

    
    # Get the data from the celebrity API
    actors_info, no_info_actors = (api_factory.get_celebrityapi_actors_data(list_of_actors))
    
    for actor in actors_info:
        name, age, gender, birthday, net_worth, is_alive = actor
        
        # Convert boolean to SQLite appropriate
        if is_alive == True:
            is_alive = 1
        else:
            is_alive = 0


        # Update columns in the Actors table for the given actor
        cur.execute("UPDATE Actors SET age=?, gender=?, birthday=?, net_worth=?, is_alive=? WHERE name=?",(age, gender, birthday, net_worth, is_alive, name))
        conn.commit()


# Fill in the database
def load_database(database_name: str):

    # Grab the list of movies
    movie_list = get_movies_list.get_movies_list()
    # Ensure there are no repeated movies in the given list 
    movie_list = sorted(list(set(movie_list)))

    # Create and set up the Movie & Actors database
    cur, conn = setup_database_connection(database_name)
    setup_all_tables(cur, conn)

    # Keep track of the last actor_id with api data added to it
    index = get_last_actors_id(cur)
    
    # Retrieve the Movies information from OMDb API
    movie_data = api_factory.get_omdbapi_movie_data(movie_list)

    # Add data from both APIs into the database
    add_omdbapi_data_to_database(movie_data, cur, conn)
    add_celebrityapi_data_to_database(index, cur, conn)


database_name = "Movie_And_Actors_Database"
load_database(database_name)