from fastapi import FastAPI, status, Response
from db import Client
from data_types import Game, GameRequest, User, UserRequest, VerifyRequest
from elo import adjust_elo_record
from fastapi.middleware.cors import CORSMiddleware
import jwt

app = FastAPI()
# TODO: Change this
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_client = Client()

@app.get("/health", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Alive"}

@app.post("/auth", status_code=status.HTTP_200_OK)
async def auth(userRequest: UserRequest, response: Response):
    token = userRequest.token
    user = db_client.get_user(token)
    if user is None:
        try:
            new_user = User(token)
        except jwt.DecodeError as e:
            print(e)
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": "Invalid Token"}
        if not new_user.email.endswith("rice.edu"):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": "User is not a Rice student"}
        db_client.put_user(new_user.__dict__)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "User Created"}
        
    return {"message": "User Authorized"}

@app.get("/user", status_code=status.HTTP_200_OK)
async def user(userRequest: UserRequest, response: Response):
    token = userRequest.token
    user = db_client.get_user(token)
    if user is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid Token"}
    return user

@app.post("/game", status_code=status.HTTP_200_OK)
async def game(gameRequest: GameRequest, response: Response):
    player1_token = gameRequest.player1_token
    player2_token = gameRequest.player2_token
    player1 = db_client.get_user(player1_token)
    player2 = db_client.get_user(player2_token)
    if player1 is None or player2 is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid Player Token"}
    game_id = db_client.get_game_collection().count_documents({})
    game = Game(game_id, player1.name, player2.name, gameRequest.score)
    db_client.get_game_collection().insert_one(game.__dict__)
    return {"message": "Game Created"}

@app.post("/game/verify", status_code=status.HTTP_200_OK)
async def verify(verifyRequest: VerifyRequest, response: Response):
    game_id = verifyRequest.game_id
    verifying_player = verifyRequest.verifying_player
    game = db_client.get_game(game_id)
    if game is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Game not found"}
    if game.verify(verifying_player):
        db_client.get_game_collection().replace_one({"_id": game_id}, game.__dict__)
        player1 = db_client.get_user(game.player1)
        player2 = db_client.get_user(game.player2)
        adjust_elo_record(player1, player2, 1 if game.winner == player1.name else 0)
        db_client.get_user_collection().replace_one({"token": player1.token}, player1.__dict__)
        db_client.get_user_collection().replace_one({"token": player2.token}, player2.__dict__)
        return {"message": "Game Verified"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid Player Token"}
