from pydantic import BaseModel
import jwt

class User:
    def __init__(self, token):
        self.token = token
        user_data = jwt.decode(token, options={"verify_signature": False})
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.picture = user_data["picture"]
        self.elo = 1000
        self.games = []
        self.wins = 0
        self.losses = 0

class Game:
    def __init__(self, game_id, player1, player2, score):
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.verified = False 
        self.score = score
        self.winner = player1 if score[0] > score[1] else player2
        self.loser = player2 if score[0] > score[1] else player1
    
    def verify(self, verifying_player):
        if verifying_player == self.player2:
            self.verified = True
            return True
        
        return False

class UserRequest(BaseModel):
    token: str

class GameRequest(BaseModel):
    player1_token: str
    player2_token: str
    score: list

class VerifyRequest(BaseModel):
    game_id: int
    verifying_player: str