from bs4 import BeautifulSoup
import requests

def get_movies_list():
    """
    This function scrappes the website that contains movie titles, 
    and returns a list with all the movie titles.
    """
    all_titles = []

    # Get the titles on the first page and add them to a list
    base_url = "https://www.listchallenges.com/imdb-top-250-movies-of-all-time-2019-update"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = soup.find_all("div", class_="item-name")

    # Get the titles on the other pages and append those to the same list
    page = 2
    for x in range(6):
        url = f"{base_url}/list/{page}"
        r = requests.get(url)
        new_soup = BeautifulSoup(r.content, 'html.parser')
        new_titles = new_soup.find_all('div', class_="item-name")

        titles.extend(new_titles)
        page +=1


    # Go through each title in the list and strip them to just the title, then add them to the final list
    for each_title in titles:
        string_title = str(each_title)
        split_title = string_title.split()
        list_title = split_title[2:-2]
        final_title = " ".join(list_title)
        all_titles.append(final_title)

    return all_titles