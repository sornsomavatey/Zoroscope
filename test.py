from datetime import datetime
from db import DatabaseHandler, get_zodiac_sign
import requests
from bs4 import BeautifulSoup


'''
This file is for testing the logic and condition before input in app.py

'''

# Initialize DB handler
db = DatabaseHandler()

# Helper function to get zodiac sign
def get_user_zodiac(username):
    user = db.get_user_by_name(username)
    if not user:
        return None, None
    birthday = datetime(user['year'], user['month'], user['date'])
    sign, icon = get_zodiac_sign(birthday.month, birthday.day)
    return sign, icon

# Function to get horoscope
def horoscope(username, day="today"):
    sign, icon = get_user_zodiac(username)
    if not sign:
        return "User not found."

    dic = {
        'Aries': 1, 'Taurus': 2, 'Gemini': 3,
        'Cancer': 4, 'Leo': 5, 'Virgo': 6,
        'Libra': 7, 'Scorpio': 8, 'Sagittarius': 9,
        'Capricorn': 10, 'Aquarius': 11, 'Pisces': 12
    }
    zodiac_number = dic[sign]

    url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-{day}.aspx?sign={zodiac_number}"
    )

    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find("div", class_="main-horoscope").p.text

# ----------------------------
# TEST SCRIPT STARTS HERE
# ----------------------------

if __name__ == "__main__":
    # Example user info
    username = "testuser"
    password = "testpass"
    birthday = "2000-03-15"

    # Register the user
    print("Registering user...")
    db.register_user(username, password, birthday)
    print(f"Registered {username}")

    # Authenticate user
    print("Authenticating user...")
    if db.authenticate_user(username, password):
        print(f"Authentication successful for {username}")
    else:
        print("Authentication failed.")
        exit()

    # Get zodiac sign
    sign, icon = get_user_zodiac(username)
    if not sign:
        print("Failed to get zodiac sign.")
        exit()
    print(f"Zodiac Sign: {sign} {icon}")

    # Get horoscope
    print("Fetching horoscope...")
    horoscope_text = horoscope(username, day="today")
    print("\nToday's Horoscope:")
    print(horoscope_text)
