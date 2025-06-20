from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

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

    # Simulated saving/validation (no database for now)
    print(f"Signup: {name}, {password}, {birthday}")

    # Redirect back to welcome page with name
    return jsonify({'message': f'Welcome, {name}!', 'redirect': url_for('welcome', name=name)})

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))
