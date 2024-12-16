from fastapi import FastAPI, Form
from notion import ComandosNotion
from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request
from llm import generarJsonComando, generarJsonMinuta, generarResumenMinuta, switch_comandos
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from schemas import projectEntity, projectsEntity, taskEntity, tasksEntity, resumenEntity, resumenesEntity
from config.db import get_db
from bson import ObjectId
from info import obtenerTodo
import json


app = FastAPI()
# Mount the static files directory
folder = os.path.join(os.path.dirname(__file__), "frontend/static")
app.mount("/static", StaticFiles(directory=folder), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="frontend")
cn = ComandosNotion()

@app.get('/')
def home(request: Request):
    try:
        todo = obtenerTodo()
        todo_json = json.dumps(todo, ensure_ascii=False)
        return templates.TemplateResponse("index.html", {"request": request, "todo": todo_json})
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"
    

@app.post('/comandos/')
def comandos(texto:str):
    try:
        #respuesta, n = generarJsonComando(texto)
        content={"respuesta":texto}
        return JSONResponse(content=content, status_code=200)
        if respuesta.status_code == 200:
            content={"respuesta":n}
            return JSONResponse(content=content, status_code=200)
        else:
            content={"respuesta":n}
            return JSONResponse(content=content, status_code=respuesta.status_code)
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"

@app.post('/minutatxt/')
def minutatxt(texto_minuta:str):

    try:
        n = generarJsonMinuta (texto_minuta)
        #resumen_minuta = generarResumenMinuta (texto_minuta)
        #db = get_db()
        #db.minutasResumen.insert_one(resumen_minuta)
        if n == 2:
            content={"respuesta":"Se recibió la minuta con éxito"+", hay comandos incompletos, checar pagina"}
            return JSONResponse(content=content, status_code=200)
        else:
            content={"respuesta":"Se recibió la minuta con éxito"+" no hay comandos"}
            return JSONResponse(content=content, status_code=200)
    
    except Exception as e:
        return f"Error en minutatxt {e}"
    
@app.post('/minuta_resumen/')
def minuta_resumen(texto_minuta:str):

    try:
        #n = generarJsonMinuta (texto_minuta)
        resumen_minuta = generarResumenMinuta (texto_minuta)
        collection = {"resumen":resumen_minuta}
        db = get_db()
        db.minutasResumen.insert_one(collection)
        
        content={"respuesta":"Se recibió la minuta con éxito"+", se generó el resumen"}
        return JSONResponse(content=content, status_code=200)

    
    except Exception as e:
        return f"Error en minutatxt {e}"
    
    
@app.get('/obtenerProyectosIncompletos/')
def obtenerProyectosIncompletos(request: Request):
    try:
        db = get_db()
        resumen_minuta = db.minutasResumen.find()
        num_pro = db.minutas.count_documents({"tipo": "proyecto"})
        combined= []
        combineds= []

        if (num_pro == 1):
            tasks = projectEntity(db.minutas.find_one({"tipo":"proyecto"}))
            names = []
            data = []
            for i in tasks: 
                names.append(i)
                data.append(tasks[i])
            combined = zip(names,data)
            respuesta = templates.TemplateResponse("minuta.html",{"request": request, "combined": combined, "res_min": resumen_minuta, "tipo":"proyecto"})
            

        elif (num_pro>1):
            
            tasks = projectsEntity(db.minutas.find({"tipo":"proyecto"}))
            names = []
            data = []
            for task in tasks:
                for i in task:
                    names.append(i)
                    data.append(tasks[i])
                combined = zip(names,data)
            combineds.append(combined)
            respuesta = templates.TemplateResponse("minuta2.html",{"request": request, "combineds": combineds, "res_min": resumen_minuta, "tipo":"proyecto"})
        
        return respuesta
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"

    
@app.get('/obtenerTareasIncompletos/')
def obtenerTareasIncompletos(request: Request):
    try:
        db = get_db()
        resumen_minuta = db.minutasResumen.find()
        num_task = db.minutas.count_documents({"tipo": "tarea"})
        combined= []
        combineds= []

        if (num_task == 1):
            tasks = taskEntity(db.minutas.find_one({"tipo":"tarea"}))
            names = []
            data = []
            for i in tasks: 
                names.append(i)
                data.append(tasks[i])
            combined = zip(names,data)
            respuesta = templates.TemplateResponse("minuta.html",{"request": request, "combined": combined, "res_min": resumen_minuta, "tipo":"tarea"})
            

        elif (num_task>1):
            
            tasks = tasksEntity(db.minutas.find({"tipo":"tarea"}))
            names = []
            data = []
            for task in tasks:
                for i in task:
                    names.append(i)
                    data.append(tasks[i])
                combined = zip(names,data)
            combineds.append(combined)
            respuesta = templates.TemplateResponse("minuta2.html",{"request": request, "combineds": combineds, "res_min": resumen_minuta, "tipo":"tarea"})
        
        
        
        return respuesta
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"


@app.post('/acompletarproyecto/')
def acompletar(id:str = Form(...), tipo: str = Form(...), accion: str = Form(...), nombre_proyecto: str = Form(...), estado: str = Form(...),
               fecha_inicio: str = Form(...), fecha_fin: str = Form(...), prioridad: str = Form(...)):
    datos = {
        "tipo": tipo,
        "accion": accion,
        "nombre_proyecto": nombre_proyecto,
        "estado": estado,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "prioridad": prioridad,
    }
    respuesta, n = switch_comandos(datos)

    db = get_db()

    db.minutas.find_one_and_delete({"_id": ObjectId(id)})

    if respuesta.status_code == 200:
        content={"respuesta":n}
        return JSONResponse(content=content, status_code=200)
    else:
        content={"respuesta":n}
        return JSONResponse(content=content, status_code=respuesta.status_code)

@app.post('/acompletartarea/')
def acompletar(id:str = Form(...), tipo: str = Form(...), accion: str = Form(...), nombre_proyecto: str = Form(...), nombre_tarea: str = Form(...),
            nombre_persona: str = Form(...), nombre_sprint:str = Form(...), estado: str = Form(...), fecha_inicio: str = Form(...), fecha_fin: str = Form(...), prioridad: str = Form(...), 
            resumen: str = Form(...)):
    try:
        datos = {
            "tipo": tipo,
            "accion": accion,
            "nombre_proyecto": nombre_proyecto,
            "nombre_tarea": nombre_tarea,
            "nombre_persona": nombre_persona,
            "nombre_sprint": nombre_sprint,
            "estado": estado,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "prioridad": prioridad,
            "resumen": resumen,
        }
        respuesta, n = switch_comandos(datos)
        return datos

        db = get_db()

        db.minutas.find_one_and_delete({"_id": ObjectId(id)})
        if respuesta.status_code == 200:
            content={"respuesta":n}
            return JSONResponse(content=content, status_code=200)
        else:
            content={"respuesta":n}
            return JSONResponse(content=content, status_code=respuesta.status_code)
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)