from fastapi import FastAPI, Form
from notion import ComandosNotion
from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request
from llm import generarJsonComando, generarJsonMinuta, generarResumenMinuta
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from schemas import projectEntity, projectsEntity
from config.db import get_db


app = FastAPI()
# Mount the static files directory
folder = os.path.join(os.path.dirname(__file__), "frontend/static")
app.mount("/static", StaticFiles(directory=folder), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="frontend")
cn = ComandosNotion()

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
def minutatxt(texto_minuta:str):

    respuesta, n = generarJsonMinuta (texto_minuta)
    resumen_minuta = generarResumenMinuta (texto_minuta)
    db = get_db()
    db.minutasResumen.insert_one(resumen_minuta)
    if respuesta.status_code == 200:
        content={"respuesta":"Se recibió la minuta con éxito"+n}
        return JSONResponse(content=content, status_code=200)
    else:
        content={"respuesta":"Se recibió la minuta con éxito"+n}
        return JSONResponse(content=content, status_code=respuesta.status_code)
    
@app.get('/obtenerIncompletos/')
def obtenerIncompletos(request: Request):
    try:
        db = get_db()
        #resumen_minuta = db.minutasResumen.find()
        resumen_minuta = "cuak"
        tasks = projectsEntity(db.minutas.find_one({"tipo":"proyecto"}))
        names = []
        data = []
        combineds = []
        
        
        for i in tasks: 
            names.append(i)
            data.append(tasks[i])
        combined = zip(names,data)
        
        respuesta = templates.TemplateResponse("minuta.html",{"request": request, "combined": combined, "res_min": resumen_minuta})
        return respuesta
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"
    
@app.post('/acompletar/')
def acompletar(nombre_proyecto: str = Form(...), msg: str = Form(...)):
    return nombre_proyecto


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)