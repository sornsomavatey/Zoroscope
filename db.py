from pymongo import MongoClient
import hashlib


class DatabaseHandler:
    def __init__(self, uri="mongodb+srv://Vatey:vatey2609@cluster0.disrk.mongodb.net/Zoroscope?retryWrites=true&w=majority"):
        self.client = MongoClient(uri)
        self.db = self.client["Zoroscope"]
        self.users = self.db["Sign_up"]
        

    def hash_password(self, password):
        # Simple hash for demonstration (you may use bcrypt for more security)
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
    
    def get_user_by_name(self, username):
        user = self.users.find_one({"name": username})
        if user:
            # Return relevant fields
            return {
                "name": user.get("name"),
                "year": user.get("year"),
                "month": user.get("month"),
                "date": user.get("date")
            }
        return None
    
    def get_user_by_email(self, email):
        user = self.users.find_one({"email": email})
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




