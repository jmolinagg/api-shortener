from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from starlette.responses import RedirectResponse

app = FastAPI()

dic = []

class Item(BaseModel):
  url: str
  short: Optional[str] = None # Elegir nuestra propio acortador será opcional, sino será random

@app.get("/")
async def root():
  return dic

@app.post("/")
async def create_url(item: Item):
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


