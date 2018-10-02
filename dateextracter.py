import io
import re
import sys

from bs4 import BeautifulSoup, NavigableString


def remove_unnecessary_sections(soup):
    UNNECESSARY_LIST_CLASS = [
    "reflist",                  # contains the reference list
    "ambox-Unreferenced",
    "toc",                      # table of contents
    "citation",                 # contains citations
    "suggestions",
    "sisterproject",            # links to other website
    "external",                 # links to other website
    "vertical-navbox",          # only remove in parsing phase, we need this in crawling phage to get links
    "noprint",                  # "From Wikipedia, the free encyclopedia"
    "mw-jump",                  # links to navigation, search
    # "navigation-not-searchable",# just as it says, no need
    "hatnote",                  # "For more information..." text
    "metadata",
    "thumb",                    # for thumbnails
    ]

    UNNECESSARY_LIST_ID = [
    "mw-navigation",        # navigation
    "mw-hidden-catlinks",   # sister-projects
    "Sources_and_footnotes"
    "footer",
    ]

    UNNECESSARY_LIST_ROLE = [
    # "note",                 # notes in text
    "navigation",           # navigation bar
    ]

    unnecessary_sections_class = soup.find_all(class_=UNNECESSARY_LIST_CLASS)
    for section in unnecessary_sections_class:
        section.decompose()

    unnecessary_sections_id = soup.find_all(id=UNNECESSARY_LIST_ID)
    for section in unnecessary_sections_id:
        section.decompose()

    navigation_sections = soup.find_all(role=UNNECESSARY_LIST_ROLE)
    for section in navigation_sections:
        section.decompose()

    # remove every sibling after reference section
    reference = soup.find(id="References")
    if reference:
        next_tags = reference.parent.next_siblings

        # next_siblings returns generator object so,
        # first we need to get all siblings before decomposing them
        tags = []
        for tag in next_tags:
            tags.append(tag)

        # remove every sibling after navigation section
        # navigation = soup.find(id="mw-navigation")
        # nav_siblings = navigation.parent.next_siblings

        # for tag in nav_siblings:
        #     tags.append(tag)
        # navigation.parent.decompose()

        for tag in tags:
            if not isinstance(tag, NavigableString):
                tag.decompose()

        reference.parent.decompose()

# remove unnecessary spaces, inline references and other characters
def clean_text(text):
    # remove inline references with space, e.g> [1], [12], [123], [1234]
    text = re.sub(r"(\[\d+\])", "", text)
    # remove inline reference of form [a]
    text = re.sub(r"(\[\w\])", "", text)
    # replace more than one white space character with only one space
    text = re.sub(r"[\s]+", " ", text)
    return text


YEARS_SELECTION = "on|in|of"    # these appear before the date
YEAR_PATTERN = r"[\d]{4}"        # only select year of 4 digits
MONTHS_PATTERN = "january|febuary|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"

DATE_PATTERN = r"""
(
    ({year_selection}) [ ]
    (?P<year>
        # e.g> "In 1926"
        ({year})
        |
        # e.g> "On March 21, 1926", "December 2016"
        (({month}) ([ ] [\d]{{1,2}} [,]?)? [ ] {year})
    )
)
"""

DATE_PATTERN = DATE_PATTERN.format(
    year_selection = YEARS_SELECTION,
    year           = YEAR_PATTERN,
    month          = MONTHS_PATTERN
)

# TODO: add support for range of date; e.g> 1920-2020 BCE
AGE_PATTERN = r"""
# e.g> 12,000 BCE, 580 AD
(?P<era>([\d]{1,2},)?[\d]{1,5} [ ] (BC[E]?|AD|CE))
|
# e.g> In the 21st Century, mid-7th century, 21st-century, 6th century BCE
(?P<century>
    ((mid|early|late)[ -]?)? [ ] [\d]{1,2}.{2} [ -]? centur(y|ies) ([ ] BC[E]?)?
)
|
# first part is for number before decimal if exists
# e.g> 1.8 million years ago
(?P<years_ago>([\d]+[\.,])? [\d]+ ([ ] (million|billion))? [ ] years [ ] ago)
"""

SEARCH_PATTERN = AGE_PATTERN + "|" + DATE_PATTERN

SEARCH_REGEX = re.compile(SEARCH_PATTERN, re.VERBOSE | re.IGNORECASE)


# extract the date and line where date was found  form the BeautifulSoup object
def extract_date(soup):

    soup = soup.body
    remove_unnecessary_sections(soup)

    text = soup.get_text()
    text = clean_text(text)

    # split the soup at every fullstop and new line
    # only match '.' and not 'c.'
    split = re.compile(r"""
        (
            \n
            |
            # handle dates such as (d. 117 CE) as well
            (?<!(\([c|d] | [ ] [c|d]) ) \. [ ]
            # (?<!(\(c | [ ] c)) \. [ ]
        )
    """, re.VERBOSE)

    lines = re.split(split, text)

    for line in lines:
        # only use line when it is not empty and
        # when it has no whiltespace surrounding it
        if line and line.strip() and line != '\n' and line.strip() != '.':
            # line = clean_text(line)
            for match in SEARCH_REGEX.finditer(line):
                captures  = match.groupdict()

                century   = captures.get("century")
                era       = captures.get("era")
                years_ago = captures.get("years_ago")
                year      = captures.get("year")

                date_str  = ""  # store the actual date value
                date_type = ""  # store the date value type; e.g> Era

                if century:
                    date_str, date_type  = century, "Century"

                if era:
                    date_str, date_type  = era, "Era"

                if years_ago:
                    date_str, date_type  = years_ago, "Years Ago"

                if year:
                    date_str, date_type  = year, "Year"

                yield {'date_str': date_str, 'date_type': date_type,  'content': line}
