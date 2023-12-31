import database_utilities
import os
import numpy
import config


def access_database(database_name="Movie_And_Actors_Database"):
    """ 
    This function takes a string, the database name, and accesses the database with given name. 
    The default database name is set to be the name of the database created for this project. 
    
    The function returns cur, conn - the cursor and connection for the database
    """

    cur, conn = database_utilities.setup_database_connection(database_name)
    return cur, conn

def write_txt_file(filename: str, section_header: str, lines: list):
    """
    This function takes a file name, a string representing the header for the file section, 
    and a list containing the information to be written, and writes a text file.

    The function does not overwrite the file content if file already exists. Instead, it appends
    the new content to the end of the file. 

    The function does not return anything.
    To enable the function, access the config.py file and set WRITE_TO_CALCULATIONS_RESULTS to TRUE. 
    """
    # Ensure text file is not re-written without enabling 
    if config.WRITE_TO_CALCULATIONS_RESULTS == False:
        return 
    
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


def calculate_average_networth_based_on_gender(cur):
    """
    This function takes a database cursor (cur). 
    It calculates the average net worth of actors in the database based on their gender, females and males, respectively,
    and writes the results of those calculations to a text file. 
    
    The function returns the average net worth of female actors, and the average net worth of male actors, respectively. 
    """

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


    # Write information to the calculation file
    females_networth_info = f"Average Net Worth of Female Actors Who are Still Alive: {average_networth_females}"
    males_networth_info = f"Average Net Worth of Male Actors Who are Still Alive: {average_networth_males}"
    information = [females_networth_info, males_networth_info]
    write_txt_file("calculations_results.txt", "Average Net Worth of Actors Based on Gender", information)

    return average_networth_females, average_networth_males
    
    

def calculate_average_imdb_rating_based_on_gender_year(cur, gender: str, year: int):
    """
    This function takes a database cursor (cur), a string representing a gender, and an integer representing a year.
    It calculates the average imdb rating of the movies in the database with more actors of the given gender 
    BEFORE and ON/AFTER the given year.

    This function returns the average IMDb rating before the given year, and the average rating on/after that given year
    as float numbers, respectively. 
    """

    # Join all three tables to gather the IMDb ratings for the movies released ON or AFTER a given year 
    # where there are more actors of a given gender 
    cur.execute("""SELECT imdb FROM Movies 
                JOIN Movies_and_Actors ON Movies.movie_id = Movies_and_Actors.movie_id 
                JOIN Actors ON Movies_and_Actors.actor_id = Actors.actor_id 
                WHERE Actors.gender =(?) AND Movies.year >= (?)
                GROUP BY Movies.movie_id HAVING COUNT(DISTINCT Actors.actor_id) >= (?)""", (gender, year, 2))
    
    all_ratings_on_and_after_year = cur.fetchall()

    # Calculate the average IMDb rating of the movies follow the given criteria
    all_imdb_ratings = 0

    for movie in all_ratings_on_and_after_year:
        movie_rating = movie[0]

        # Combine all the IMDb rating values
        all_imdb_ratings += movie_rating
    average_imdb_rating_on_and_after_year = all_imdb_ratings / len(all_ratings_on_and_after_year)
    # Round the average calculation result to have only 1 decimal
    average_imdb_rating_on_and_after_year = round(average_imdb_rating_on_and_after_year, 1)

    
    # Join all three tables to gather the IMDb ratings for the movies released BEFORE a given year 
    # where there are more actors of a given gender 
    cur.execute("""SELECT imdb FROM Movies 
                JOIN Movies_and_Actors ON Movies.movie_id = Movies_and_Actors.movie_id 
                JOIN Actors ON Movies_and_Actors.actor_id = Actors.actor_id 
                WHERE Actors.gender =(?) AND Movies.year < (?)
                GROUP BY Movies.movie_id HAVING COUNT(DISTINCT Actors.actor_id) >= (?)""", (gender, year, 2))
    
    all_ratings_before_year = cur.fetchall()
    # Calculate the average IMDb rating of the movies follow the given criteria
    all_imdb_ratings = 0

    for movie in all_ratings_before_year:
        movie_rating = movie[0]

        # Combine all the IMDb rating values
        all_imdb_ratings += movie_rating
    average_imdb_rating_before_year = all_imdb_ratings / len(all_ratings_before_year)
    # Round the average calculation result to have only 1 decimal
    average_imdb_rating_before_year = round(average_imdb_rating_before_year, 1)
    

    # Write information to the calculation file 
    before_year_info = f"Average IMDb rating BEFORE {year}: {average_imdb_rating_before_year}"
    on_after_year_info = f"Average IMDb rating ON and AFTER {year}: {average_imdb_rating_on_and_after_year}"
    
    information = [before_year_info, on_after_year_info]
    write_txt_file("calculations_results.txt", f"Popularity of {gender.capitalize()}-Led Movies Before and After {year}", information)

    return average_imdb_rating_before_year, average_imdb_rating_on_and_after_year
    

def calculate_slope_of_age_trend_over_years(cur):
    """
    This function takes a database cursor (cur). 
    It calculates the slope of the actors' age trend over the years. 

    It returns the information necessary to build a scatterplot:
    a tuple with format (list A, list B) where list A = movie years, and list B = actors' ages;
    the slope of the best-fit line as a float number with 4 decimal places; and the y-intercept.
    """

    # Gather all movies years and the valid actors birthdays
    cur.execute("""SELECT year, birthday FROM Movies 
                JOIN Movies_and_Actors ON Movies.movie_id = Movies_And_Actors.movie_id
                JOIN Actors ON Movies_And_Actors.actor_id = Actors.actor_id
                WHERE birthday IS NOT NULL
                """)
    list_of_data_points = cur.fetchall()

    x_values = []
    y_values = []
    

    for point in list_of_data_points:
        # Extract data from the tuple
        movie_year, birthday = point

        # Select actor's birth year and convert to an integer
        birth_year = int(birthday.split("-")[0])
        
        # Calculate the age of the actor when the movie was released
        actor_age = movie_year - birth_year

        # If the actor is not a child actor, consider that data point
        if actor_age > 17:
            y_values.append(actor_age)
            x_values.append(movie_year)

    # Check if there is a trend over the years by calculting the slope   
    slope, y_intercept = numpy.polyfit(x_values, y_values, 1)
    slope = round(slope, 4)

    # Write information to the calculation file
    information = [f"Slope: {slope}"]
    write_txt_file("calculations_results.txt", "Actors Age Trend Over Nearly 100 Years", information)

    # Return data to build scatterplot and best-fit line
    return (x_values, y_values), slope, y_intercept


# This calculation was added after the presentation/grading session so we could add new visualizations   
def calculate_slope_of_gender_age_trend_over_years(cur, gender: str):
    """
    This function takes a database cursor and a string representing a gender (female or male). 
    It calculates the slope of the given gender actors' age trend over the years. 

    It returns the information necessary to build a scatterplot:
    a tuple with format (list A, list B) where list A = movie years, and list B = actors' ages;
    the slope of the best-fit line as a float number with 4 decimal places; and the y-intercept.
    """

    # Gather all movies years and the valid actors birthdays
    cur.execute("""SELECT year, birthday FROM Movies 
                JOIN Movies_and_Actors ON Movies.movie_id = Movies_And_Actors.movie_id
                JOIN Actors ON Movies_And_Actors.actor_id = Actors.actor_id
                WHERE gender = (?) AND birthday IS NOT NULL
                """, (gender,))
    list_of_data_points = cur.fetchall()

    x_values = []
    y_values = []
    

    for point in list_of_data_points:
        # Extract data from the tuple
        movie_year, birthday = point

        # Select actor's birth year and convert to an integer
        birth_year = int(birthday.split("-")[0])
        
        # Calculate the age of the actor when the movie was released
        actor_age = movie_year - birth_year

        # If the actor is not a child actor, consider that data point
        if actor_age > 17:
            y_values.append(actor_age)
            x_values.append(movie_year)

    # Check if there is a trend over the years by calculting the slope   
    slope, y_intercept = numpy.polyfit(x_values, y_values, 1)
    slope = round(slope, 4)

    # Write information to the calculation file
    information = [f"Slope: {slope}"]
    write_txt_file("calculations_results.txt", f"{gender.capitalize()} Actors Age Trend Over Nearly 100 Years", information)

    # Return data to build scatterplot and best-fit line
    return (x_values, y_values), slope, y_intercept
    


def main():
    # Run calculations 
    cur, conn = access_database()
    calculate_average_networth_based_on_gender(cur)
    calculate_average_imdb_rating_based_on_gender_year(cur, 'female', 2000)
    calculate_average_imdb_rating_based_on_gender_year(cur, 'male', 2000)
    calculate_slope_of_age_trend_over_years(cur)
    calculate_slope_of_gender_age_trend_over_years(cur, 'female')
    calculate_slope_of_gender_age_trend_over_years(cur, 'male')


main()


