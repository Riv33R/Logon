from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField

from wtforms.validators import DataRequired

import csv


app = Flask(__name__)

app.secret_key = 'your_secret_key'


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'


class User(UserMixin):

    def __init__(self, id):

        self.id = id


@login_manager.user_loader

def load_user(user_id):

    return User(user_id)


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')


def read_csv_data(filepath, search_term):

    results = []

    try:

        with open(filepath, newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                if search_term.lower() in row.get('UserName', '').lower() or search_term.lower() in row.get('ComputerName', '').lower():

                    # Convert LogonTime string to datetime object

                    logon_time = datetime.strptime(row['LogonTime'], '%y-%m-%d %H:%M')

                    # Format the datetime object to the desired format

                    row['LogonTime'] = logon_time.strftime('%d.%m.%Y %H:%M')

                    results.append(row)

            # Sort results by datetime objects in LogonTime

            results.sort(key=lambda x: datetime.strptime(x['LogonTime'], '%d.%m.%Y %H:%M'), reverse=True)

    except FileNotFoundError:

        results = [{'Error': 'File not found or cannot be accessed'}]

    except ValueError as e:

        print(f"Error converting date and time: {e}")

    return results


@app.route('/login', methods=['GET', 'POST'])

def login():

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data

        password = form.password.data

        # Replace with actual user validation

        if username == 'admin' and password == 'School12023+':

            user = User(username)

            login_user(user)

            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])

@login_required

def logout():

    logout_user()

    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])

@login_required

def index():

    results = []

    if request.method == 'POST':

        username_or_pcname = request.form['search']

        # Replace the following path with the path to your file

        filepath = '/mnt/share/UserLogons.csv'

        results = read_csv_data(filepath, username_or_pcname)

    return render_template("index.html", results=results)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)

