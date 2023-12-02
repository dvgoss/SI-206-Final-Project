from bs4 import BeautifulSoup
import requests

def get_movies_list():
    all_titles = []

    #Getting the titles on the first page and adding them to a list
    base_url = "https://www.listchallenges.com/top-100-movies-to-watch-before-you-die"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    titles = soup.find_all("div", class_="item-name")

    #Getting the titles on the other pages and appending those to the same list
    page = 2
    for x in range(2):
        url = f"{base_url}/list/{page}"
        r = requests.get(url)
        new_soup = BeautifulSoup(r.content, 'html.parser')
        new_titles = new_soup.find_all('div', class_="item-name")

        titles.extend(new_titles)
        page +=1


    #Going thru each title in the list and stripping them to just the title, then adding them to the final list
    for each_title in titles:
        string_title = str(each_title)
        split_title = string_title.split()
        list_title = split_title[2:-2]
        final_title = " ".join(list_title)
        all_titles.append(final_title)

    return all_titles