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
    cur.execute("CREATE TABLE IF NOT EXISTS Actors (actors_id INTEGER PRIMARY KEY, name TEXT UNIQUE, age INTEGER, gender TEXT, birthday TEXT, net_worth NUMERIC)")
    
    #create Movies_Actors table
    cur.execute("CREATE TABLE IF NOT EXISTS Movies_and_Actors (movie_actor_combination_id INTEGER PRIMARY KEY, movie_id INTEGER, actor_id INTEGER)")

    conn.commit()



#cur, conn = setup_database_structure("Movie & Actors Database")
#setup_all_tables(cur, conn)