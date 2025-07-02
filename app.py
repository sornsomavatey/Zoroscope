from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import DatabaseHandler
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from db import DatabaseHandler, get_zodiac_sign

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = DatabaseHandler()
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

    # Simulated saving/validation (no database for now)
    print(f"Signup: {name}, {password}, {birthday}")

    # Redirect back to welcome page with name
    return jsonify({'message': f'Welcome, {name}!', 'redirect': url_for('welcome', name=name)})

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No data received'}), 400
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password required'}), 400

        if db.authenticate_user(username, password):
            return jsonify({
                'message': f'Welcome back, {username}!',
                'redirect': url_for('greeting', username=username)
            }), 200
        else:
            return jsonify({'message': ' Invalid username or password'}), 401

    return render_template('login.html')

def get_user_zodiac(username):
    """
    Load user data and return (sign_name, sign_icon)
    """
    user = db.get_user_by_name(username)
    
    if not user:
        return None, None  # or raise an error
    
    birthday = datetime(user['year'], user['month'], user['date'])
    sign, icon = get_zodiac_sign(birthday.month, birthday.day)
    return sign, icon


@app.route('/greeting/<username>')
def greeting(username):
    user = db.get_user_by_name(username)
    if not user:
        return redirect(url_for('login_page'))

    sign, icon = get_user_zodiac(username)
    quote = "Believe in yourself and the stars will align ✨"

    return render_template(
        "greeting.html",
        username=username,
        zodiac=sign,
        zodiac_icon=icon,
        quote=quote
    )
@app.route('/explore')
def explore_page():
    return render_template('card.html')

# def horoscope(username, day="today"):
#     sign, icon = get_user_zodiac(username)
#     if not sign:
#         return "User not found."

#     # Map sign names to numbers (Horoscope.com expects numbers)
#     dic = {
#         'Aries': 1, 'Taurus': 2, 'Gemini': 3,
#         'Cancer': 4, 'Leo': 5, 'Virgo': 6,
#         'Libra': 7, 'Scorpio': 8, 'Sagittarius': 9,
#         'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
#     }
#     zodiac_number = dic[sign]

#     url = (
#         "https://www.horoscope.com/us/horoscopes/general/"
#         f"horoscope-general-daily-{day}.aspx?sign={zodiac_number}"
#     )

#     soup = BeautifulSoup(requests.get(url).content, "html.parser")
#     return soup.find("div", class_="main-horoscope").p.text


if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
