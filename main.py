from fastapi import FastAPI, status, Response
from db import Client
from data_types import User, UserRequest
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