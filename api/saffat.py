from flask import Flask, jsonify
import sqlite3
from datetime import datetime, time

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Welcome Home"


# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('../database/db.sqlite')


# Route to fetch all data from the database
@app.route('/data/all', methods=['GET'])
def get_all_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prayer')  # Replace 'your_table' with your table name
    data = cursor.fetchall()
    coming_prayer = define_next_prayer(data)

    output_array = [{"name": pair[1], "adan": pair[2], "iqama": pair[3], "wudu": pair[4], "ar_name": pair[5]} for pair
                    in data]

    output_array.append({"name": coming_prayer[1], "adan": coming_prayer[2], "iqama": coming_prayer[3],
                         "wudu": coming_prayer[4], "ar_name": coming_prayer[5]})
    conn.close()
    return jsonify(output_array)


def define_next_prayer(data):
    coming_prayer = None
    start_time = get_time(data[0])
    for i in range(1, len(data)):
        current = data[i]
        end_time = get_time(current)
        if is_within_interval(start_time,end_time):
            coming_prayer = current
        start_time = end_time

    coming_prayer = coming_prayer if coming_prayer else data[0]
    return coming_prayer

def is_within_interval(start_time, end_time):
    now = datetime.now().time()
    return start_time <= now <= end_time

def get_time(p):
    time_str = p[3].split(":")

    t1 = convert_to_int(time_str[0])

    t2 = convert_to_int(time_str[1])

    time_ = time(t1,t2)

    return time_

def convert_to_int(s):
    try:
        return int(s)
    except ValueError:
        print("Error: Cannot convert '{}' to an integer.".format(s))
        return None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Different port for each API

