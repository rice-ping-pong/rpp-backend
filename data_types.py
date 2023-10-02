from pydantic import BaseModel
import jwt

class User:
    def __init__(self, token):
        self.token = token
        print(token)
        user_data = jwt.decode(token, options={"verify_signature": False})
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.picture = user_data["picture"]
        self.elo = 1000
        self.games = []
        self.wins = 0
        self.losses = 0

class UserRequest(BaseModel):
    token: str