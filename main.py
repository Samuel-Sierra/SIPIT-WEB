from fastapi import FastAPI
from notion import comandosNotion
from fastapi.responses import JSONResponse
from pydantic import BaseModel

cn = comandosNotion()
app = FastAPI()

class Comando(BaseModel):
    texto: str

@app.get('/')
def home():
    return "Hola mundo!"

@app.post('/comandos')
def comandos(data: Comando):
    texto = data.texto
    try:
        respuesta = cn.CrearTarea(texto)
        
        content=""
        if respuesta.status_code == 200:
            content = "Concretado"
            return JSONResponse(content=content, status_code=200)
        else:
            content = "No concretado"
            return JSONResponse(content=content, status_code=respuesta.status_code)
    except Exception as e:

        ab = f"Error al crear tarea: {str(e)}"
        content = ab+"Hubo un error al crear la tarea. Por favor, inténtalo de nuevo."
        return JSONResponse(content=content, status_code=respuesta.status_code)

    
    
