from datetime import datetime
from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def read_csv_data(filepath, search_term):
    results = []
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if search_term.lower() in row.get('UserName', '').lower() or search_term.lower() in row.get('ComputerName', '').lower():
                    # Преобразование строки LogonTime в объект datetime
                    row['LogonTime'] = datetime.strptime(row['LogonTime'], '%y-%m-%d %H:%M')
                    results.append(row)
            # Сортировка результатов по объектам datetime в LogonTime
            results.sort(key=lambda x: x['LogonTime'], reverse=True)
    except FileNotFoundError:
        results = [{'Error': 'File not found or cannot be accessed'}]
    except ValueError as e:
        print(f"Ошибка при преобразовании даты и времени: {e}")
        # Вы можете решить, что делать в случае ошибки преобразования
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
