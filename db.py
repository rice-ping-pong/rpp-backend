from pymongo import MongoClient
from pymongo.server_api import ServerApi
from constants import MONGO_URI, MONGO_CERT_PATH, DATABASE, USER_COLLECTION, GAME_COLLECTION


class Client:

    def __init__(self):
        self.client = MongoClient(MONGO_URI,
                        tls=True,
                        tlsCertificateKeyFile=MONGO_CERT_PATH,
                        server_api=ServerApi('1'))

    def get_database(self):
        return self.client[DATABASE]
    
    def get_user_collection(self):
        return self.get_database()[USER_COLLECTION]
    
    def get_game_collection(self):
        return self.get_database()[GAME_COLLECTION]
    
    def get_user(self, token):
        return self.get_user_collection().find_one({"token": token})
    
    def get_game(self, game_id):
        return self.get_game_collection().find_one({"_id": game_id})
    
    def put_user(self, user):
        return self.get_user_collection().insert_one(user)
    




