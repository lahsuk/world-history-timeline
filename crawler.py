# standard library imports
import io
import urllib
import time
import re
import atexit

# external library import
import requests
from bs4 import BeautifulSoup

# project import
from historydb import db_get_next_visit_urls, db_get_pages, db_insert_data, db_insert_data, db_visited_already, db_insert_not_visited_urls, db_delete_all_not_visite_urls
from dateextracter import extract_date
from date_utils import convert_date_to_number

# need to access during program termination so set it as global
global links
# links is a tuple if (title, url)
links = []

# this will be called during program termination to save unvisited links
# to the database
@atexit.register
def save_unvisited_links_to_db():
    urls = []
    for _, url in links:
        urls.append(url)
    # print("urls:", len(urls), urls)
    db_delete_all_not_visite_urls()
    db_insert_not_visited_urls(urls)


# returns the url with unnecessary components removed
def get_clean_name_url(url):
    if '#' in url:                 # remove redirection
        url = url.rpartition('#')
        url = url[0]
    title = url.partition('wiki/') # get the web page title only
    title = title[2]

    title_url = (title, urllib.parse.urljoin('https://en.wikipedia.org/', url))
    return title_url

def is_unneeded_link(url):
    if ":" in url:
        return True
    return False

def get_random_article():
    while True:
        RANDOM = "https://en.wikipedia.org/wiki/Special:Random"
        r = requests.get(RANDOM)

        if not db_visited_already(r.url):
            break

        time.sleep(10)

    return get_clean_name_url(r.url)


# asks the crawler to crawl for CRAWL_COUNT number of times
def crawl(CRAWL_COUNT = float('inf')):
    global links

    last_urls = db_get_next_visit_urls()
    # set to start link if not resuming from before
    if not last_urls:
        START_LINK = 'https://en.wikipedia.org/wiki/History_of_the_world'
        links.append(("History_of_the_world", START_LINK))
    else:
        # print("last links:", len(last_urls), last_urls)
        for url, in last_urls:
            links.append(get_clean_name_url(url))

    # format of the form of all wikipedia links
    WIKI_LINK = re.compile("/wiki/.*")

    # keeps track of the number of pages crawled
    count = 0
    while count < CRAWL_COUNT:
        print("start:", links[0])

        # get the first page
        r = requests.get(links[0][1])
        soup = BeautifulSoup(r.text, 'html.parser')

        for date_data in extract_date(soup):
            date_type = date_data['date_type']
            date_str  = date_data['date_str']
            content   = date_data['content']
            title = links[0][0]
            days_since_beginning = convert_date_to_number(date_type, date_str)

            # print("date type:", date_type)
            # print("date_str:", date_str)
            # print("content:", content)
            # print("title:", title)
            # print("time:", days_since_beginning)
            db_insert_data(title, content, date_type, date_str, days_since_beginning)


        ls = soup.find(id='mw-content-text').find(class_='mw-parser-output').find_all('a') # find all links

        for l in ls:
            href = l.get('href')
            if href and re.search(WIKI_LINK, href):
                if is_unneeded_link(href):
                    continue

                title_url  = get_clean_name_url(href)

                if not db_visited_already(title_url[0]) and title_url not in links:
                    links.append(title_url)

        links.pop(0)    # pop first element
        # print(links[0])

        # if links is empty, select a random article
        if len(links) == 0:
            links.append(get_random_article())

        # 10 seconds was too fast, so go even slower
        time.sleep(30)
        count += 1

        # take a break for 30min every 300 pages crawled
        if count % 300 == 0:
            time.sleep(1800)