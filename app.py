from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import DatabaseHandler, get_zodiac

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = DatabaseHandler()
z_sign=get_zodiac()
# Root route = Welcome page
@app.route('/')
def welcome():
    name = request.args.get('name', 'Guest')
    return render_template('Welcome-page.html', name=name)

# Sign-up page
@app.route('/signup-page')
def signup_page():
    return render_template('index.html')

# Handle form data from signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    birthday = data.get('birthday')

    db.register_user(name, password, birthday)


    # Extract month and day
    parts = birthday.split('-')
    month = int(parts[1])
    day = int(parts[2])

    zodiac_sign = z_sign.get_zodiac_sign(month, day)

    print(f"Signup: {name}, {password}, {birthday}, Zodiac: {zodiac_sign}")

    return jsonify({
        'message': f'Signed up successfully! Welcome, {name}!',
        'redirect': url_for('show_zodiac', name=name, zodiac=zodiac_sign)})










@app.route("/login")
def login_page():
    return render_template("login.html")  # or whatever your login template is


if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
