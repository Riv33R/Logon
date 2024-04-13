from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def read_csv_data(filepath, search_term):
    results = []
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Используйте .get() для получения значений без риска KeyError
                user_name = row.get('UserName', '').lower()
                computer_name = row.get('ComputerName', '').lower()
                if search_term.lower() in user_name or search_term.lower() in computer_name:
                    results.append(row)
    except FileNotFoundError:
        results = [{'Error': 'File not found or cannot be accessed'}]
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username_or_pcname = request.form['search']
        # Замените следующий путь на путь к вашему файлу
        filepath = '\\\\srv-ad.dnestrschool1.online\\share\\Logonlogs\\UserLogons.csv'
        results = read_csv_data(filepath, username_or_pcname)
        return render_template("index.html", results=results)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
