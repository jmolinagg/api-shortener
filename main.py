from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uuid
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

dic = [] 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Item(BaseModel):
  url: str
  short: Optional[str] = None # Elegir nuestra propio acortador será opcional, sino será random

@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
  return dic

@app.post("/")
async def create_url(item: Item, token: str = Depends(oauth2_scheme)):
  if item.short != None:
    for i in dic:
      if i.short == item.short:
        return {"Ese link acortado ya existe."}
  if item.short == None:
    item.short = str(uuid.uuid4())[-6:] # Generamos el acortador random, si no se ha elegido
  dic.append(item);
  return item;


@app.get("/{short}")
async def open_url(short: str):
  for i in dic:
    if i.short == short:
      return RedirectResponse(i.url)
  raise HTTPException(status_code=404, detail="No se ha encontrado ese link acortado")


# Usuarios por defecto: usuario1, contra1 y usuario2, contra2
fake_users_db = {
    "usuario1": {
        "username": "usuario1",
        "hashed_password": "fakehashedcontra1",
    },
    "usuario2": {
        "username": "usuario2",
        "hashed_password": "fakehashedcontra2",
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

