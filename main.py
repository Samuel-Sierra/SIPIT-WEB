from fastapi import FastAPI
from notion import comandosNotion
from fastapi.responses import JSONResponse

cn = comandosNotion()
app = FastAPI()

@app.get('/')
def home():
    return "Hola mundo!"

@app.get('/comandos/{texto}')
def comandos(texto : str):
    respuesta = cn.CrearTarea(texto)
    content=""
    if respuesta.status_code == 200:
        content = "Concretado"
        return JSONResponse(content=content, status_code=200)
    else:
        content = "No concretado"
        return JSONResponse(content=content, status_code=respuesta.status_code)
    
    
