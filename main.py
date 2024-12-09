from fastapi import FastAPI
from notion import ComandosNotion
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
from llm import generarJsonComando, generarJsonMinuta
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
# Mount the static files directory
folder = os.path.join(os.path.dirname(__file__), "frontend/static")
app.mount("/static", StaticFiles(directory=folder), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="frontend")
cn = ComandosNotion()

class Comando(BaseModel):
    texto: str

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/comandos/')
def comandos(texto:str):
    respuesta, n = generarJsonComando(texto)

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
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)