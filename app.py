from flask import Flask, render_template, request, jsonify, redirect, url_for
from db import DatabaseHandler
from datetime import datetime
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
            return jsonify({'message': 'Invalid username or password'}), 401

    return render_template('login.html')

@app.route('/greeting/<username>')
def greeting(username):
    user = db.get_user_by_name(username)
    if not user:
        return redirect(url_for('login_page'))

    # Use year, month, date from user dict to create datetime
    birthday = datetime(user['year'], user['month'], user['date'])
    sign, icon = get_zodiac_sign(birthday.month, birthday.day)


    quote = "Believe in yourself and the stars will align ✨"

    return render_template("greeting.html", username=username, zodiac=sign, zodiac_icon=icon, quote=quote)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
