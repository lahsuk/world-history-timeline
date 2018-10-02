from flask import Flask, jsonify, request, render_template
from date_utils import convert_date_to_number, convert_number_to_year
from historydb import db_get_pages_in_range

app = Flask(__name__)

@app.route('/history_data', methods=['GET', 'POST'])
def history_data():
    # Don't use POST; doesn't work for some reason
    if request.method == "POST":
        start = request.data.get('start', '')
        end   = request.data.get('end', '')
    elif request.method == "GET":
        start = request.args.get('start', '')
        end   = request.args.get('end', '')
        randomize = True if request.args.get('random', '') == "true" else False
        load_count = request.args.get('load_count', '')
        print(request.args.get('randomize', ''))
        print('start:', start)
        print('end:', end)
        print('randomize:', randomize)        
        print('load count:', load_count)

    if start and end:
        start = convert_date_to_number('Year', start)
        end   = convert_date_to_number('Year', end)

        values_dict = []
        if load_count.isdecimal():
            pages = db_get_pages_in_range(start, end, load_count, randomize)
        else:
            pages = db_get_pages_in_range(start, end, randomize=randomize)
        for title, content, _, date, number in pages:
            year = convert_number_to_year(number)
            values_dict.append(
                {
                    'title': title,
                    'content': content,
                    'date': date,
                    'year': year,
                    'link': 'https://en.wikipedia.org/wiki/' + title,
                }
            )

        send_values = {'values': values_dict}
        return jsonify(send_values)

@app.route('/')
def index():
    return render_template('index.html')
