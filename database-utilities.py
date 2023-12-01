import sqlite3
import os


def setup_database_structure(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + database_name)
    cur = conn.cursor()
    return cur, conn

def setup_all_tables(cur, conn):

    #create Movies table
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (movie_id INTEGER PRIMARY KEY, title TEXT UNIQUE, year INTEGER, rotten_tomatoes FLOAT, metascore FLOAT, imdb FLOAT)")
    
    #create Actors table
    cur.execute("CREATE TABLE IF NOT EXISTS Actors (actor_id INTEGER PRIMARY KEY, name TEXT UNIQUE, age INTEGER, gender TEXT, birthday TEXT, net_worth NUMERIC)")
    
    #create Movies_Actors table
    cur.execute("CREATE TABLE IF NOT EXISTS Movies_and_Actors (movie_actor_combination_id INTEGER PRIMARY KEY, movie_id INTEGER, actor_id INTEGER)")

    conn.commit()


def add_omdbapi_data_to_database(movie_data, cur, conn):

    #insert each movie information into the Movies table in the database
    for movie in movie_data:
        title, year, rotten_tomatoes, metascore, imdb, actors = movie
        cur.execute("INSERT OR IGNORE INTO Movies (title, year, rotten_tomatoes, metascore, imdb) VALUES (?,?,?,?,?)", (title, year, rotten_tomatoes, metascore, imdb))

        #get movie_id from Movies table
        cur.execute("SELECT movie_id FROM Movies WHERE title = (?)", (title,))
        movie_id = (cur.fetchone())[0]
        

        #insert each actor to the actors table
        for actor in actors:
           cur.execute("INSERT OR IGNORE INTO Actors (name) VALUES (?)", (actor,))

           #get actor_id from the Actors table
           cur.execute("SELECT actor_id FROM Actors WHERE name = (?)", (actor,))
           actor_id = (cur.fetchone())[0]

           #insert data into the Movies_and_Actors table
           cur.execute("INSERT OR IGNORE INTO Movies_and_Actors (movie_id, actor_id) VALUES (?,?)", (movie_id, actor_id))
    
    conn.commit()



#cur, conn = setup_database_structure("Movie & Actors Database")
#setup_all_tables(cur, conn)
#movie_data = [("movie 1", 2012, 70, 69, 4.5, ["Actor 1", "Actor 2", "Actor 3"]), ("movie 2", 2022, 89, 75, 8.9, ["Actor 1", "Actor 4", "Actor 5"])]
#add_omdbapi_data_to_database(movie_data, cur, conn)