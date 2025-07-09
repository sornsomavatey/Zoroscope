from pymongo import MongoClient
import hashlib
import ephem  
from bson import ObjectId


class DatabaseHandler:
    def __init__(self, uri="mongodb+srv://Vatey:vatey2609@cluster0.disrk.mongodb.net/Zoroscope?retryWrites=true&w=majority"):
        self.client = MongoClient(uri)
        self.db = self.client["Zoroscope"]
        self.users = self.db["Sign_up"]
        

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, email, password):
        hashed_password = self.hash_password(password)
        user = self.users.find_one({
            "email": email,
            "password": hashed_password })
        return user is not None
    
    def register_user(self, username,email, password, birthday):
        
        hashed_password = self.hash_password(password)
        year, month, date = map(int, birthday.split('-'))  # 'YYYY-MM-DD'
        self.users.insert_one({
            "name": username,
            "email": email,
            "password": hashed_password,
            "date": date,
            "month": month,
            "year": year
        })  
    
    def get_user_by_email(self, email):
        user = self.users.find_one({"email": email})
        if user:
            return {
                "user_id": str(user.get("_id")),
                "name": user.get("name"),
                "email": user.get("email"),
                "year": user.get("year"),
                "month": user.get("month"),
                "date": user.get("date")
            }
        return None
    
    def get_user_by_id(self, user_id):
        user = self.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return {
                "name": user.get("name"),
                "email": user.get("email"),
                "year": user.get("year"),
                "month": user.get("month"),
                "date": user.get("date")
            }
        return None   

def get_zodiac_sign(month, day):
    zodiac_signs = [
        ("Capricorn",  (1,  19), "♑"),
        ("Aquarius",   (2,  18), "♒"),
        ("Pisces",     (3,  20), "♓"),
        ("Aries",      (4,  19), "♈"),
        ("Taurus",     (5,  20), "♉"),
        ("Gemini",     (6,  20), "♊"),
        ("Cancer",     (7,  22), "♋"),
        ("Leo",        (8,  22), "♌"),
        ("Virgo",      (9,  22), "♍"),
        ("Libra",     (10,  22), "♎"),
        ("Scorpio",   (11,  21), "♏"),
        ("Sagittarius",(12, 21), "♐"),
        ("Capricorn", (12, 31), "♑")
    ]

    for sign, (m, d), icon in zodiac_signs:
        if (month < m) or (month == m and day <= d):
            return sign, icon
    return "Capricorn", "♑"

def get_moon_phase(date):
    moon = ephem.Moon(date)
    phase = moon.phase

    if phase < 1.5:
        return "New Moon"
    elif 1.5 <= phase < 25:
        return "Waxing Crescent"
    elif 25 <= phase < 35:
        return "First Quarter"
    elif 35 <= phase < 49:
        return "Waxing Gibbous"
    elif 49 <= phase < 51:
        return "Full Moon"
    elif 51 <= phase < 65:
        return "Waning Gibbous"
    elif 65 <= phase < 75:
        return "Last Quarter"
    elif 75 <= phase < 99:
        return "Waning Crescent"
    else:
        return "New Moon"

# Zodiac Sign Color Associations
ZODIAC_COLORS = {
    "Aries": ["Red", "Orange", "Yellow"],
    "Taurus": ["Green", "Brown", "Muted Yellow"],
    "Gemini": ["Yellow", "Light Blue", "Orange"],
    "Cancer": ["Blue", "Green", "White"],
    "Leo": ["Bright Yellow", "Orange", "Gold"],
    "Virgo": ["Subtle Green", "Brown", "Light Blue"],
    "Libra": ["Blue", "Pink", "Violet"],
    "Scorpio": ["Red", "Black", "Violet"],
    "Sagittarius": ["Yellow", "Blue", "Orange"],
    "Capricorn": ["Brown", "Gray", "Dark Blue"],
    "Aquarius": ["Blue", "Green", "White"],
    "Pisces": ["Light Blue", "Violet", "Green"]
}

# 8 Moon Phase Color Associations
MOON_PHASE_COLORS = {
    "New Moon": ["Black", "Dark Blue", "Deep Purple"],
    "Waxing Crescent": ["Light Green", "Pale Yellow"],
    "First Quarter": ["Red", "Orange"],
    "Waxing Gibbous": ["Gold", "Bright Yellow", "Light Blue"],
    "Full Moon": ["White", "Silver", "Light Blue"],
    "Waning Gibbous": ["Violet", "Indigo", "Soft Blue"],
    "Last Quarter": ["Gray", "Brown"],
    "Waning Crescent": ["Dark Green", "Black", "Deep Blue"]
}

# Planetary Color Associations
PLANET_COLORS = {
    "Sun": ["Gold", "Orange"],
    "Moon": ["Silver", "White"],
    "Mars": ["Red"],
    "Venus": ["Pink", "Green"],
    "Jupiter": ["Royal Blue", "Purple"],
    "Saturn": ["Dark Blue", "Black"],
    "Mercury": ["Yellow", "Light Blue"],
    "Uranus": ["Electric Blue"],
    "Neptune": ["Sea Green"],
    "Pluto": ["Black", "Deep Red"]
}

RULING_PLANETS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Pluto",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Uranus",
    "Pisces": "Neptune"
}

COLOR_HEX_MAP = {
    "Red": "#FF0000",
    "Orange": "#FFA500",
    "Yellow": "#FFFF00",
    "Green": "#008000",
    "Brown": "#A52A2A",
    "Muted Yellow": "#D8B500",
    "Light Blue": "#ADD8E6",
    "Blue": "#0000FF",
    "White": "#FFFFFF",
    "Bright Yellow": "#FFEA00",
    "Gold": "#FFD700",
    "Subtle Green": "#90EE90",
    "Pink": "#FFC0CB",
    "Violet": "#8F00FF",
    "Black": "#000000",
    "Gray": "#808080",
    "Dark Blue": "#00008B",
    "Deep Purple": "#673AB7",
    "Light Green": "#90EE90",
    "Pale Yellow": "#FFFFE0",
    "Silver": "#C0C0C0",
    "Indigo": "#4B0082",
    "Soft Blue": "#87CEFA",
    "Dark Green": "#006400",
    "Deep Blue": "#001F3F",
    "Royal Blue": "#4169E1",
    "Purple": "#800080",
    "Electric Blue": "#7DF9FF",
    "Sea Green": "#2E8B57",
    "Deep Red": "#8B0000"
}


