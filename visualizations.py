import calculations
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

cur, conn = calculations.access_database()

def calculate_average_net_worth_based_on_gender(cur, conn):
#This function returns the average net worth of females and males in this order. 
# Create a bar graph that puts both averages side by side


    avg_net_worth_females, avg_net_worth_males = calculations.calculate_average_networth_based_on_gender(cur)

    # Create a bar graph
    genders = ['Female', 'Male']
    averages = [avg_net_worth_females, avg_net_worth_males]

    plt.bar(genders, averages)
    plt.xlabel('Gender')
    plt.ylabel('Average Net Worth')
    plt.title('Average Net Worth Based on Gender')
    plt.show()

# cur, conn = calculations.access_database()
calculate_average_net_worth_based_on_gender(cur, conn)


def calculate_average_imdb_rating_based_on_gender_year(gender, year):
#This function returns the average IMDb rating of movies led by the gender before a given year, and on/after that given year in this order. 

#You will need to pass the gender and year (2000) so the function works 

#Create a bar graph that puts both gender averages side by side, for both scenarios (before and on/after the 2000s)


#Is there a difference in the popularity of female-led or male-led movies released before 2000 in comparison to movies released after that? 

#Are older female-led movies more popular than more recent newer female-led movies?

#Are older male-led movies more popular than more recent newer male-led movies?



#[IMPORTANT] What do I mean by female or male-led: If a movie have 2 or 3 female leading actors, then that movie is female-led. The OMDb API stores 3 actors for each movie, and those are the leading actors. 
    avg_rating_before_year, avg_rating_on_after_year = calculations.calculate_average_imdb_rating_based_on_gender_year(cur, gender, year)

    # Create a bar graph
    scenarios = ['Before ' + str(year), 'On/After ' + str(year)]
    averages = [avg_rating_before_year, avg_rating_on_after_year]

    plt.bar(scenarios, averages)
    plt.xlabel('Scenario')
    plt.ylabel('Average IMDb Rating')
    plt.title(f'Average IMDb Rating Based on {gender.capitalize()}-Led Movies and Year')
    plt.show()

# cur, conn = calculations.access_database()
calculate_average_imdb_rating_based_on_gender_year('female', 2000, cur, conn)
calculate_average_imdb_rating_based_on_gender_year('male', 2000, cur, conn)

def calculate_slope_of_age_trend_over_years():


#Create a scatterplot with a best-fit line. The function returns everything you need: a tuple of x-y values (list of x values, list of y values), slope, and y-intercept

#Here we’re checking if the age of the main actors starting movies changed over the years. 
    (x_values, y_values), slope, y_intercept = calculations.calculate_slope_of_age_trend_over_years(cur)

    # Create a scatterplot with best-fit line
    plt.scatter(x_values, y_values, label='Data Points')
    plt.plot(x_values, slope * np.array(x_values) + y_intercept, color='red', label='Best-fit Line')

    plt.xlabel('Year')
    plt.ylabel('Main Actors Age')
    plt.title('Age Trends Over the Years')
    plt.legend()
    plt.show()

# Assuming you have cur and conn from somewhere
# cur, conn = calculations.access_database()
calculate_slope_of_age_trend_over_years(cur, conn)


