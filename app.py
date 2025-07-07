from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import *
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from bson import ObjectId
import requests
import joblib


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = DatabaseHandler()

#Load datasets and model for zodiac sign compatibility prediction
original_df = pd.read_csv("Zoroscope_dataset/zodiac_compatibility_dataset.csv")
encoded_df = pd.read_csv("Zoroscope_dataset/encoded_zodiac_compatibility_dataset.csv")
descriptions_df = pd.read_csv("Zoroscope_dataset/zodiac_pairs_description.csv")
model = joblib.load("Zoroscope_dataset/xgb_zodiac_model.pkl")
features = joblib.load("Zoroscope_dataset/xgb_features.pkl")

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
            return jsonify({'message': 'email and password required'}), 400

        if db.authenticate_user(email, password):
            user = db.get_user_by_email(email)
            
            return jsonify({
                'message': f'Welcome back, {user["name"]}!',
                'user_id': str(user["user_id"]),
                'username': user["name"],
                'redirect': url_for('greeting', user_id=str(user["user_id"]))
            }), 200
        else:
            return jsonify({'message': ' Invalid email or password'}), 401

    return render_template('login.html')

def get_user_zodiac(user_id):
    """
    Load user data and return (sign_name, sign_icon)
    """
    user = db.get_user_by_id(user_id)

    birthday = datetime(user['year'], user['month'], user['date'])
    sign, icon = get_zodiac_sign(birthday.month, birthday.day)
    return sign, icon


@app.route('/greeting/<user_id>')
def greeting(user_id):
    
    user = db.get_user_by_id(user_id)
    if not user:
        return redirect(url_for('login_page'))

    sign, icon = get_user_zodiac(user_id)
    quote = "Believe in yourself and the stars will align ✨"

    return render_template(
        "greeting.html",
        username=user["name"],
        user_id=user_id,
        zodiac=sign,
        zodiac_icon=icon,
        quote=quote
    )


@app.route('/explore/<user_id>')
def explore_page(user_id):
    return render_template('card.html', user_id=user_id)

@app.route('/daily-horoscope/<user_id>', methods=["GET", "POST"])
def daily_horoscope(user_id):

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
        user = db.get_user_by_id(user_id)
        if not user:
            return f"User ID {user_id} not found.", 404

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
            user_id=user_id
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
            user_id=user_id
        )
    

def lucky_color_from_birthdate(birthdate):
    month = birthdate.month
    day = birthdate.day

    sign_name, _ = get_zodiac_sign(month, day)  # unpack tuple
    sign = sign_name    

    moon_phase = get_moon_phase(birthdate)
    planet = RULING_PLANETS.get(sign)

    sign_colors = ZODIAC_COLORS.get(sign, [])
    moon_colors = MOON_PHASE_COLORS.get(moon_phase, [])
    planet_colors = PLANET_COLORS.get(planet, [])

    all_colors = sign_colors * 3 + planet_colors * 2 + moon_colors
    unique_colors = list(dict.fromkeys(all_colors))

    return {
        "birthdate": birthdate.strftime("%Y-%m-%d"),
        "sign": sign,
        "ruling_planet": planet,
        "moon_phase": moon_phase,
        "lucky_colors": unique_colors
    }

@app.route("/lucky_colors", methods=["POST"])
def lucky_colors():
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "Missing user_id in request body."}), 400

    user_id = data["user_id"]
    user = db.get_user_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found or invalid user ID."}), 404

    if not all(u in user for u in ["year", "month", "date"]):
        return jsonify({"error": "Date fields missing in user data."}), 400

    birthdate = datetime(user["year"], user["month"], user["date"])
    result = lucky_color_from_birthdate(birthdate)

    return jsonify(result), 200

    
@app.route("/predict/<user_id>")
def compatibility_page(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        return redirect(url_for('login_page'))

    user_sign, _ = get_zodiac_sign(user["month"], user["date"])

    Zodiac_option = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    return render_template(
        "predict.html",
        username=user["name"],
        user_id=user_id,
        user_sign=user_sign,
        zodiacs=Zodiac_option
    )

@app.route("/predict", methods=["POST"])
def signs_compatibility():
    data = request.json
    sign1 = data.get("sign1", "").strip().capitalize()
    sign2 = data.get("sign2", "").strip().capitalize()

    if not sign1 or not sign2:
        return jsonify({"error": "Both 'sign1' and 'sign2' are required."}), 400

    # Find matching row (either order)
    match = original_df[
        ((original_df["Sign1"] == sign1) & (original_df["Sign2"] == sign2)) |
        ((original_df["Sign1"] == sign2) & (original_df["Sign2"] == sign1))
    ]

    if match.empty:
        return jsonify({"error": "Combination not found in the dataset."}), 404

    idx = match.index[0]

    # Fetch encoded row
    row_encoded = encoded_df.iloc[[idx]].copy()
    row_encoded = row_encoded.drop(columns=["Compatibility_rate"], errors="ignore")
    row_encoded = row_encoded.reindex(columns=features, fill_value=0) 

    # Predict compatibility
    pred = model.predict(row_encoded)[0]
    round_pred = round(float(pred) * 100, 2)
    

    # Get descriptions
    desc_rows = descriptions_df[
        ((descriptions_df["Sign1"] == sign1) & (descriptions_df["Sign2"] == sign2)) |
        ((descriptions_df["Sign1"] == sign2) & (descriptions_df["Sign2"] == sign1))
    ]

    descriptions = {}
    if desc_rows.empty:
        descriptions["Friends"] = "No description available."
        descriptions["Couple"] = "No description available."
    else:
        # Friends descriptions
        friends_texts = desc_rows[desc_rows["RelationshipType"] == "Friends"]["Description"].tolist()
        couple_texts = desc_rows[desc_rows["RelationshipType"] == "Couple"]["Description"].tolist()

        descriptions["Friends"] = " ".join(friends_texts) if friends_texts else "No description available."
        descriptions["Couple"] = " ".join(couple_texts) if couple_texts else "No description available."

    return jsonify({
        "sign1": sign1,
        "sign2": sign2,
        "compatibility_score": round_pred,
        "descriptions": descriptions
    })

@app.route('/lucky-color/<username>')
def lucky_color_page(username):
    user = db.get_user_by_name(username)
    if not user:
        return redirect(url_for('login_page'))

    sign, _ = get_zodiac_sign(user['month'], user['date'])

    color_data = {
        "Aries": {"image": "aries.jpg", "color": "Red", "desc": "Red energizes Aries and boosts confidence."},
        "Taurus": {"image": "taurus.jpg", "color": "Green", "desc": "Green brings Taurus calm and prosperity."},
        "Gemini": {"image": "gemini.jpg", "color": "Yellow", "desc": "Yellow stimulates Gemini’s curiosity and joy."},
        # Add more...
    }

    info = color_data.get(sign, {
        "image": "default.jpg",
        "color": "Unknown",
        "desc": "No lucky color available."
    })

    return render_template("color.html", username=username, sign=sign, color=info["color"], description=info["desc"], image=info["image"])

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
