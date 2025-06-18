from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb+srv://Vatey:vatey2609@cluster0.disrk.mongodb.net/Zoroscope?retryWrites=true&w=majority")
# <- Compass uses this too
db = client["Zoroscope"]
users_collection = db["sign_up"]
