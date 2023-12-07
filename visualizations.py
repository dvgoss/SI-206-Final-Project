import calculations
import numpy as np
import matplotlib.pyplot as plt



def plot_average_net_worth_based_on_gender(cur):
    """
    This function creates a bar graph with the the average net worth of females and males 
    showcased side by side.
    """
 
    # Calculate average net worth of female and male actors
    avg_net_worth_females, avg_net_worth_males = calculations.calculate_average_networth_based_on_gender(cur)

    # Create a bar graph that puts both averages side by side
    genders = ['Female', 'Male']
    averages = [avg_net_worth_females, avg_net_worth_males]
    colors = ['indianred', 'cadetblue']

    plt.bar(genders, averages, color=colors)
    plt.xlabel('Gender')
    plt.ylabel('Average Net Worth (in Millions)')
    plt.title('Average Net Worth of Actors in the Top 250 Movies Based on Gender')
    plt.show()




def plot_average_imdb_rating_based_on_gender_year(cur, gender, year):
    """
    This function plots the average IMDb rating of gender-led movies before and on/after given year
    """

    # Calculate average IMDb rating for gender-led movies before and on/after year
    avg_rating_before_year, avg_rating_on_after_year = calculations.calculate_average_imdb_rating_based_on_gender_year(cur, gender, year)
    
    # Create a bar graph
    scenarios = ['Before ' + str(year), 'On/After ' + str(year)]
    averages = [avg_rating_before_year, avg_rating_on_after_year]
    colors = ['indigo', 'darkolivegreen']

    plt.bar(scenarios, averages, color=colors)
    plt.xlabel('Time Period')
    plt.ylabel('Average IMDb Rating')
    plt.title(f'Average IMDb Rating for {gender.capitalize()}-Led Movies in the Top 250')
    
    for i, value in enumerate(averages):
        plt.text(i, value, str(round(value, 2)), ha='center', va='bottom')

    plt.show()



def plot_scatterplot_of_age_trend(cur):
    """
    This function creates a scatterplot with a best-fit line representing
    a potential actor's age trend over the years
    """

    # Calculate the data for the scatterplot (points, slope, and y-intercept)
    (x_values, y_values), slope, y_intercept = calculations.calculate_slope_of_age_trend_over_years(cur)

    # Create a scatterplot with best-fit line
    plt.scatter(x_values, y_values, label='Age', color='cadetblue')
    plt.plot(x_values, slope * np.array(x_values) + y_intercept, color='orangered', label='Best-fit Line')

    plt.xlabel('Year')
    plt.ylabel('Age of Main Actors')
    plt.title('Age Trend of Actors in the Top 250 Movies Over the Years')
    plt.legend()
    plt.show()

# This function was added AFTER presentation/grading session to create extra visualizations for more extra points
def plot_scatterplot_of_gender_age_trend(cur, gender:str):
    """
    This function takes a database cursor and a string representing a gender (female or male)
    The function creates a scatterplot with a best-fit line representing
    a potential actor's age trend over the years for actors of the given gender
    """

    # Calculate the data for the scatterplot (points, slope, and y-intercept)
    points, slope, y_intercept = calculations.calculate_slope_of_gender_age_trend_over_years(cur, gender)

    # Create a scatterplot with best-fit line
    plt.scatter(points[0], points[1], label='Age', color='mediumaquamarine')
    plt.plot(points[0], slope * np.array(points[0]) + y_intercept, color='orangered', label='Best-fit Line')

    plt.xlabel('Year')
    plt.ylabel(f"Age of {gender.capitalize()} Main Actors")
    plt.title(f'Age Trend of {gender.capitalize()} Actors in the Top 250 Movies Over the Years')
    plt.legend()
    plt.show()


def main():
    # Create visualizations
    cur, conn = calculations.access_database()
    plot_average_net_worth_based_on_gender(cur)
    plot_average_imdb_rating_based_on_gender_year(cur,'female', 2000)
    plot_average_imdb_rating_based_on_gender_year(cur, 'male', 2000)
    plot_scatterplot_of_age_trend(cur)
    plot_scatterplot_of_gender_age_trend(cur, 'female')
    plot_scatterplot_of_gender_age_trend(cur, 'male')


main()


