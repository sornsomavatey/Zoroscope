from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import DatabaseHandler, get_zodiac_sign
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import re
import requests
import joblib


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = DatabaseHandler()

# Load datasets and model for zodiac sign compatibility prediction
# original_df = pd.read_csv("Zoroscope_dataset_preparation/zodiac_compatibility_dataset.csv")
# encoded_df = pd.read_csv("Zoroscope_dataset_preparation/encoded_zodiac_compatibility_dataset.csv")
# descriptions_df = pd.read_csv("Zoroscope_dataset_preparation/zodiac_pairs_description.csv")
# model = joblib.load("Zoroscope_dataset_preparation/xgb_zodiac_model.pkl")
# features = joblib.load("Zoroscope_dataset_preparation/xgb_features.pkl")

# Initialize Flask app
app = Flask(__name__)


# Root route = Welcome page
@app.route('/')
def welcome():
    name = request.args.get('name', 'Guest')
    return render_template('welcome_page.html', name=name)

# Sign-up page
@app.route('/signup-page')
def signup_page():
    return render_template('index.html')

# Handle form data from signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    birthday = data.get('birthday')

    # Check if email already exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        return jsonify({'message': 'Email already exists.'}), 400

    # Register new user
    db.register_user(name, email, password, birthday)

    return jsonify({
        'message': f'Welcome, {name}!',
        'redirect': url_for('welcome', name=name)
    })


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No data received'}), 400
        
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Username and password required'}), 400

        if db.authenticate_user(email, password):
            user = db.get_user_by_email(email)
            
            return jsonify({
                'message': f'Welcome back, {user["name"]}!',
                'username': user["name"],
                'redirect': url_for('greeting', username=user["name"])
            })
            200
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


@app.route('/explore/<username>')
def explore_page(username):
    return render_template('card.html', username=username)

@app.route('/daily-horoscope/<username>', methods=["GET", "POST"])
def daily_horoscope(username):

    Zodiac_option = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    dic = {
        'Aries': 1, 'Taurus': 2, 'Gemini': 3,
        'Cancer': 4, 'Leo': 5, 'Virgo': 6,
        'Libra': 7, 'Scorpio': 8, 'Sagittarius': 9,
        'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
    }

    if request.method == "POST":
        # User selected a sign manually
        sign = request.form['sign']

    elif request.method == "GET":
        # GET request, load user and get their zodiac sign
        user = db.get_user_by_name(username)
        if not user:
            return f"User '{username}' not found.", 404

        sign_name, _ = get_zodiac_sign(user['month'], user['date'])  # unpack tuple
        sign = sign_name    

    zodiac_number = dic.get(sign)

    if zodiac_number is None:
        horoscope_text = "Invalid zodiac sign selected."
        today_date = datetime.now().strftime("%B %d, %Y")
        return render_template(
            "daily-horoscope.html",
            selected_sign=sign,
            today=today_date,
            horoscope_text=horoscope_text,
            zodiacs=Zodiac_option,
            username=username
        )
    
    else: 
        # Fetch horoscope after we know the sign
        url = (
            "https://www.horoscope.com/us/horoscopes/general/"
            f"horoscope-general-daily-today.aspx?sign={zodiac_number}"
        )
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        main_div = soup.find("div", class_="main-horoscope")

        if main_div and main_div.p:
            raw_text = main_div.p.text.strip()
            if " - " in raw_text:
                horoscope_text = raw_text.split(" - ", 1)[1].strip() 
            else:
                horoscope_text = raw_text
        else:
            horoscope_text = "Horoscope information currently unavailable."

        today_date = datetime.now().strftime("%B %d, %Y")

        return render_template(
            "daily-horoscope.html",
            selected_sign=sign,
            today=today_date,
            horoscope_text=horoscope_text,
            zodiacs=Zodiac_option,
            username=username
        )

# @app.route("/predict", methods=["POST"])
# def signs_compatibility():
#     data = request.json
#     sign1 = data.get("sign1", "").strip().capitalize()
#     sign2 = data.get("sign2", "").strip().capitalize()

#     if not sign1 or not sign2:
#         return jsonify({"error": "Both 'sign1' and 'sign2' are required."}), 400

#     # Find matching row (either order)
#     match = original_df[
#         ((original_df["Sign1"] == sign1) & (original_df["Sign2"] == sign2)) |
#         ((original_df["Sign1"] == sign2) & (original_df["Sign2"] == sign1))
#     ]

#     if match.empty:
#         return jsonify({"error": "Combination not found in the dataset."}), 404

#     idx = match.index[0]

#     # Fetch encoded row
#     row_encoded = encoded_df.iloc[[idx]].copy()
#     row_encoded = row_encoded.drop(columns=["Compatibility_rate"], errors="ignore")
#     row_encoded = row_encoded.reindex(columns=features, fill_value=0)

#     # Predict compatibility
#     pred = model.predict(row_encoded)[0]
#     round_pred= float(round(pred, 2)) 
    

#     # Get descriptions
#     desc_rows = descriptions_df[
#         ((descriptions_df["Sign1"] == sign1) & (descriptions_df["Sign2"] == sign2)) |
#         ((descriptions_df["Sign1"] == sign2) & (descriptions_df["Sign2"] == sign1))
#     ]

#     descriptions = {}
#     if desc_rows.empty:
#         descriptions["Friends"] = "No description available."
#         descriptions["Couple"] = "No description available."
#     else:
#         # Friends descriptions
#         friends_texts = desc_rows[desc_rows["RelationshipType"] == "Friends"]["Description"].tolist()
#         couple_texts = desc_rows[desc_rows["RelationshipType"] == "Couple"]["Description"].tolist()

#         descriptions["Friends"] = " ".join(friends_texts) if friends_texts else "No description available."
#         descriptions["Couple"] = " ".join(couple_texts) if couple_texts else "No description available."


#     return jsonify({
#         "sign1": sign1,
#         "sign2": sign2,
#         "compatibility_score": round_pred,
#         "descriptions": descriptions
#     })


if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
