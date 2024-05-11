from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3
from datetime import datetime, timedelta


def print_time(data):
    for t in data:
        print(t)
def is_time_str_greater(time_str2):
    time_split = time_str2.split(":")
    time_extra = time_split[0]
    try:
        integer_number = int(time_extra)
        return 10 <= integer_number < 12

    except ValueError:
        print("Cannot convert the string to an integer.")
        return False

def process_data(data):
    prayer_schedule = []

    for t in data:
        time_str_adan = t[1]
        time_str_iqama = t[2]
        contains_digits = any(char.isdigit() for char in time_str_adan)
        if not contains_digits:
            time_str_adan = "12:52 PM"
            time_str_iqama = "12:52 PM"

        time_obj_adan = datetime.strptime(time_str_adan, "%I:%M %p").time()
        time_obj_iqama = datetime.strptime(time_str_iqama, "%I:%M %p").time()

        datetime_obj = datetime.combine(datetime.today(), time_obj_adan)

        # Subtract 10 minutes

        notify_at_time = (datetime_obj - timedelta(minutes=10)).time()

        prayer_schedule.append(
            (t[0], time_obj_adan.strftime('%H:%M'), time_obj_iqama.strftime('%H:%M'), notify_at_time.strftime('%H:%M'),t[3]))

    return prayer_schedule


def db_exec(data_to_insert):
    conn = sqlite3.connect('../database/db.sqlite')

    cursor = conn.cursor()

    # Define the name of the table to delete and recreate
    table_name = 'prayer'

    # Drop the table if it exists
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"

    cursor.execute(drop_table_query)

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS prayer (
                          prayer_id INTEGER PRIMARY KEY,
                          prayer_name TEXT NOT NULL,
                          prayer_name_arabic TEXT NOT NULL,
                          adan_time TEXT NOT NULL,
                          iqama_time TEXT NOT NULL,
                          notified_at TEXT NOT NULL
                    )''')

    for data in data_to_insert:
        cursor.execute("INSERT INTO prayer (prayer_name,prayer_name_arabic, adan_time, iqama_time,notified_at ) VALUES (?,?, ?, ?,?)", data)

    # Commit the transaction
    conn.commit()

    # Query the data
    cursor.execute("SELECT * FROM prayer")
    rows = cursor.fetchall()

    print_time(rows)

    # Close the connection
    conn.close()


def clean_data(s, ad, iq):
    duhr_adan = ad[2]
    duhr_iqama = iq[1]
    morning_adan = is_time_str_greater(duhr_adan)
    morning_iqama = is_time_str_greater(duhr_iqama)

    if morning_adan:
        duhr_adan += " AM"
    else:
        duhr_adan += " PM"

    if morning_iqama:
        duhr_iqama += " AM"
    else:
        duhr_iqama += " PM"

    data = [
        (s[0], ad[0] + " AM", iq[0] + " AM", "الفجر"),
        (s[2], duhr_adan, duhr_iqama, "الظهر"),
        (s[3], ad[3] + " PM", iq[2] + " PM", "العصر"),
        (s[4], ad[4] + " PM", iq[3] + " PM", "المغرب"),
        (s[5], ad[5] + " PM", iq[4] + " PM", "العشاء"),
        (s[6], ad[6] + " PM", ad[6] + " PM", "الجمعة")
    ]
    return data


def scrape_prayer():
    # URL of the webpage containing the table
    url = 'https://mosqueprayertimes.com/msaconcordia'

    # driver = webdriver.Chrome()

    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    # Launch Chrome WebDriver with headless mode
    # driver = webdriver.Chrome(options=chrome_options)

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    table = soup.find_all('table')[2]

    adan_time = []

    salat_ = []

    iqama_time = []

    rows = table.find_all('tr')

    for i in range(0, len(rows)):

        cols = rows[i].find_all('td')

        for j in range(1, len(cols)):

            span = cols[j].find('span')

            if span:

                txt = span.get_text().strip()

                if j < 8 and i == 0:
                    salat_.append(txt)

            divs = cols[j].find_all('div')

            if divs:

                time_ = divs[0].get_text().strip()

                if i == 1:
                    adan_time.append(time_)
                else:
                    iqama_time.append(time_)

                if time_ == "Khutbah":
                    khutbah_time = divs[2].get_text().strip()
                    adan_time[6] = khutbah_time

    cleaned_data = clean_data(salat_, adan_time, iqama_time)
    return cleaned_data


if __name__ == '__main__':
    db_data = scrape_prayer()
    prayer_time = process_data(db_data)
    db_exec(prayer_time)
