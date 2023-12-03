import database_utilities
import os


# Access the existing database
def access_database(database_name="Movie_And_Actors_Database"):
    cur, conn = database_utilities.setup_database_connection(database_name)
    return cur, conn

# Write a text file
def write_txt_file(filename, section_header: str, lines: list):
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filename)

    with open(full_path, 'a') as out_file:

        # Write the header of the section
        out_file.write("\n" + section_header + "\n" + "\n")

        for line in lines:
            out_file.write(line)
            out_file.write("\n")
        
        # Visually separate the different sections
        out_file.write("\n")
        out_file.write("-----------------------------------------------------------------------")



# Calculate the average rating for each movie in the database
def calculate_movie_rating_average(cur):

    # Retrieve every movie in the database along with all the ratings
    cur.execute("SELECT title, rotten_tomatoes, metascore, imdb FROM Movies")
    all_movies_rows = cur.fetchall()

    all_movies_average_ratings = []

    # Loop through all rows of the database to calculate the average rating for each movie.
    for row in all_movies_rows:
        # Extract the information from the row (tuple)
        title, rotten_tomatoes, metascore, imdb = row
        # Calculate the rating average, convert the imdb rating to the same type as the other ratings
        average_rating = (rotten_tomatoes + metascore + (imdb * 10)) / 3
        # Round the result so it only has 1 decimal place
        average_rating = round(average_rating, 1)

        # Create a string with movie title and average rating
        movie_and_average_rating = f"{title}, {average_rating}"

        all_movies_average_ratings.append(movie_and_average_rating)

    write_txt_file("calculations_results.txt", "Average Rating of Movies in The Database", all_movies_average_ratings)

    return all_movies_average_ratings


# Calculate the average net worth of actors in the database based on gender
def calculate_average_networth_based_on_gender(cur):

    # Gather the net worth data of all female actors that are still alive
    cur.execute("SELECT net_worth FROM Actors WHERE gender =(?) AND is_alive =(?)", ("female", 1))
    all_female_actors = cur.fetchall()

    # Combine the net worth of all female actors alive
    total_net_worth_females = 0
    for actress in all_female_actors:
        actress_net_worth = actress[0]

        total_net_worth_females += actress_net_worth

    # Calculate average net worth of female actors alive
    average_networth_females = int(total_net_worth_females / len(all_female_actors))


    # Gather the net worth data of all male actors that are still alive
    cur.execute("SELECT net_worth FROM Actors WHERE gender=(?) AND is_alive=(?)", ("male", 1))
    all_male_actors = cur.fetchall()

    # Combine the net worth of all male actors alive
    total_net_worth_males = 0
    for actor in all_male_actors:
        actor_net_worth = actor[0]

        total_net_worth_males += actor_net_worth
    
    # Calculate average net worth of female actors alive
    average_networth_males = int(total_net_worth_males / len(all_male_actors))


    #Write information to the calculations file
    females_networth_info = f"Average Net Worth of Female Actors Who are Still Alive: {average_networth_females}"
    males_networth_info = f"Average Net Worth of Male Actors Who are Still Alive: {average_networth_males}"
    information = [females_networth_info, males_networth_info]
    write_txt_file("calculations_results.txt", "Average Net Worth of Actors Based on Gender", information)

    return average_networth_females, average_networth_males
    
    




cur, conn = access_database()
calculate_movie_rating_average(cur)
calculate_average_networth_based_on_gender(cur)



