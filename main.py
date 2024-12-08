from fastapi import FastAPI
from notion import comandosNotion
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from llm import generarJson

cn = comandosNotion()
app = FastAPI()

class Comando(BaseModel):
    texto: str

@app.get('/')
def home():
    return "Hola mundo!"

@app.post('/comandos/')
def comandos(texto:str):

    generarJson(texto)
    #respuesta = (texto)
    
    
    #if respuesta.status_code == 200:
    #    content={"respuesta":"Concretado"}
    #    return JSONResponse(content=content, status_code=200)
    #else:
    #    content={"respuesta":"No se proporcionó respuesta en el servidor."}
    #    return JSONResponse(content=content, status_code=respuesta.status_code)
    return JSONResponse(content="CUAK", status_code=200)

@app.post('/minutatxt/')
def minuta(texto_minuta:str):
    
    return texto_minuta
    


    
    
