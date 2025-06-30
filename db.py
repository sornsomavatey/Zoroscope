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

    def authenticate_user(self, username, password):
        hashed_password = self.hash_password(password)
        user = self.users.find_one({"username": username, "password": hashed_password})
        return user is not None

    def register_user(self, username, password, birthday):
        
        hashed_password = self.hash_password(password)
        year, month, date = map(int, birthday.split('-'))  # 'YYYY-MM-DD'
        self.users.insert_one({
            "name": username,
            "password": hashed_password,
            "date": date,
            "month": month,
            "year": year
        })  
    
class get_zodiac:

    def get_zodiac_sign(self, date, month):
        if (month == 1 and date >= 20) or (month == 2 and date <= 18):
            return "Aquarius"
        elif (month == 2 and date >= 19) or (month == 3 and date <= 20):
            return "Pisces"
        elif (month == 3 and date >= 21) or (month == 4 and date <= 19):
            return "Aries"
        elif (month == 4 and date >= 20) or (month == 5 and date <= 20):
            return "Taurus"
        elif (month == 5 and date >= 21) or (month == 6 and date <= 20):
            return "Gemini"
        elif (month == 6 and date >= 21) or (month == 7 and date <= 22):
            return "Cancer"
        elif (month == 7 and date >= 23) or (month == 8 and date <= 22):
            return "Leo"
        elif (month == 8 and date >= 23) or (month == 9 and date <= 22):
            return "Virgo"
        elif (month == 9 and date >= 23) or (month == 10 and date <= 22):
            return "Libra"
        elif (month == 10 and date >= 23) or (month == 11 and date <= 21):
            return "Scorpio"
        elif (month == 11 and date >= 22) or (month == 12 and date <= 21):
            return "Sagittarius"
        else:
            return "Capricorn"



