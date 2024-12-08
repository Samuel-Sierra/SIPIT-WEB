from fastapi import FastAPI
from notion import ComandosNotion
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from llm import generarJson

cn = ComandosNotion()
app = FastAPI()

class Comando(BaseModel):
    texto: str

@app.get('/')
def home():
    return "Hola mundo!"

@app.post('/comandos/')
def comandos(texto:str):

    respuesta, n = generarJson(texto)
    
    if respuesta.status_code == 200:
        content={"respuesta":n}
        return JSONResponse(content=content, status_code=200)
    else:
        content={"respuesta":n}
        return JSONResponse(content=content, status_code=respuesta.status_code)

@app.post('/minutatxt/')
def minuta(texto_minuta:str):
    content={"respuesta":"Se recibió la minuta con éxito"+texto_minuta}
    return JSONResponse(content=content, status_code=200)
    


    
    
