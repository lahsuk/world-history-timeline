# age of earth is 4.543 billion years old
AGE_OF_EARTH = 4.543e9
DAYS_IN_YEAR = 365
DAYS_IN_MONTH = 30
HUMAN_ERA_YEARS = 10000
MONTH_COUNT = {
    'january':   1,      'jan': 1,
    'febuary':   2,      'feb': 2,
    'march':     3,      'mar': 3,
    'april':     4,      'apr': 4,
    'may':       5,
    'june':      6,      'jun': 6,
    'july':      7,      'jul': 7,
    'august':    8,      'aug': 8,
    'september': 9,      'sep': 9,
    'october':  10,     'oct': 10,
    'november': 11,     'nov': 11,
    'december': 12,     'dec': 12,
}
EARTH_AGE_OFFSET = (AGE_OF_EARTH + HUMAN_ERA_YEARS) * DAYS_IN_YEAR
CENTURY_DAYS_COUNT = 100 * DAYS_IN_YEAR
CENTURY_OFFSET = {
    'mid':   50,
    'early': 15,
    'late' : 85,
}

# return only number part of string: e.g> For 20th returns float(20)
def clean_number(s):
    s_num = ""
    for c in s:
        if c.isdigit() or c == '.':
            s_num += c
    return float(s_num)


def handle_year_type(date_str):
    number = 0
    date_parts = date_str.split()

    # when only the year date is present; e.g> 1970
    if len(date_parts) == 1:
        year = float(date_parts[0])
        number = EARTH_AGE_OFFSET + year * DAYS_IN_YEAR
    # when only month and year is present; e.g> December 1941
    if len(date_parts) == 2:
        month = date_parts[0].lower()
        month = MONTH_COUNT[month]
        year = float(date_parts[1])
        number = EARTH_AGE_OFFSET + year * DAYS_IN_YEAR + month * DAYS_IN_MONTH
    # when day, month and year is present; e.g> December 20th 1941
    if len(date_parts) == 3:
        month = date_parts[0].lower()
        month = MONTH_COUNT[month]
        day  = date_parts[1]
        day = clean_number(day)
        year = float(date_parts[2])
        number = EARTH_AGE_OFFSET + year * DAYS_IN_YEAR + month * DAYS_IN_MONTH + day

    return number


def handle_century_type(date_str):
    number = 0
    # replace all '-' with space; e.g> mid-15th-century -> mid 15th century
    date_str = date_str.replace('-', ' ')
    date_str = date_str.lower()

    date_parts = date_str.split()

    if date_str.endswith("bc") or date_str.endswith("bce"):
        # e.g> 14th Century BC
        # since century is offset by 1, subtract 1;
        # 14th Century is 1300-1399 so we need to multiply by 13 not 14
        if len(date_parts) == 3:
            century = date_parts[0]
            century = clean_number(century)
            century -= 1
            number = EARTH_AGE_OFFSET - century * CENTURY_DAYS_COUNT
        if len(date_parts) == 4:
            century_offset = date_parts[0]
            century_offset = CENTURY_OFFSET[century_offset]
            century = date_parts[1]
            century = clean_number(century)
            century -= 1
            number = EARTH_AGE_OFFSET - century * CENTURY_DAYS_COUNT - century_offset * DAYS_IN_YEAR
    else:
        # when only century is present; e.g> 20th century
        if len(date_parts) == 2:
            century = date_parts[0]
            century = clean_number(century)
            century -= 1
            number = EARTH_AGE_OFFSET + century * CENTURY_DAYS_COUNT
        # when century along with vague time is present; e.g> mid 15th century
        if len(date_parts) == 3:
            century_offset = date_parts[0]
            century_offset = CENTURY_OFFSET[century_offset]
            century = date_parts[1]
            century = clean_number(century)
            century -= 1
            number = EARTH_AGE_OFFSET + century * CENTURY_DAYS_COUNT + century_offset * DAYS_IN_YEAR

    return number

def handle_era_type(date_str):
    number = 0
    # since era is always in the form 'year era'; e.g> 1300 CE, 780 BCE
    year, era = date_str.split()
    year = clean_number(year)
    era = era.upper()

    if (era == "BCE") or (era == "BC"):
        # since we've already added 10,000 years in earth_age_offset already
        # and BCE happens before it
        number = EARTH_AGE_OFFSET - float(year) * DAYS_IN_YEAR
    if (era == "CE") or (era == "AD"):
        number = EARTH_AGE_OFFSET + float(year) * DAYS_IN_YEAR

    return number

def handle_years_ago_type(date_str):
    number = 0
    # remove the 'years ago' part; e.g> 3.2 million years ago -> 3.2 million
    date_str = date_str.replace(' years ago', '')
    date_split = date_str.split()
    # only years is present after removing ' years ago'; e.g> 200,000
    if len(date_split) == 1:
        years = clean_number(date_split[0])
        number = EARTH_AGE_OFFSET - years * DAYS_IN_YEAR
    # offset is present along with years; e.g> 3.2 million years ago
    if len(date_split) == 2:
        years = clean_number(date_split[0])
        offset = date_split[1].lower()
        if offset == "million":
            number = EARTH_AGE_OFFSET - years * 1e6 * DAYS_IN_YEAR
        elif offset == "billion":
            number = EARTH_AGE_OFFSET - years * 1e9 * DAYS_IN_YEAR

    return number

def convert_number_to_year(number):
    number -= EARTH_AGE_OFFSET
    return int(number/DAYS_IN_YEAR)


def convert_date_to_number(date_type, date_str):
    if date_type == "Year":
        return handle_year_type(date_str)
    if date_type == "Era":
        return handle_era_type(date_str)
    if date_type == "Century":
        return handle_century_type(date_str)
    if date_type == "Years Ago":
        return handle_years_ago_type(date_str)

    print("Error during conversion from date to string.\ndate_type:", date_type, "date_str:", date_str)
