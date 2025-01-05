from fastapi import FastAPI, Form
from notion import ComandosNotion
from fastapi.responses import JSONResponse, Response, RedirectResponse
from fastapi.requests import Request
from llm import generarJsonComando, generarJsonMinuta, generarResumenMinuta, switch_comandos
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from schemas import projectEntity, projectsEntity, taskEntity, tasksEntity, resumenEntity, resumenesEntity, minutaEntity, minutasEntity, sprintEntity, sprintsEntity
from config.db import get_db
from bson import ObjectId
from info import obtenerTodo
import json
import re


app = FastAPI()
# Mount the static files directory
folder = os.path.join(os.path.dirname(__file__), "frontend/static")
app.mount("/static", StaticFiles(directory=folder), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="frontend")
cn = ComandosNotion()
todo_json = ""
cont =0

@app.get('/')
def home(request: Request):
    try: 
        
        global todo_json
        global cont
        if cont == 0:
            todo = obtenerTodo()
            todo_json = json.dumps(todo, ensure_ascii=False)
            cont = cont + 1
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"  
    
@app.get('/index/')
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/proyectos/')
def proyectos(request: Request):
    try:
        global todo_json
        return templates.TemplateResponse("proyectos.html", {"request": request, "todo": todo_json})
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"    
  
@app.get('/sprints/')
def sprints(request: Request):
    try:
        global todo_json
        return templates.TemplateResponse("sprint.html", {"request": request, "todo": todo_json})
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"    

def reemplazar_original(match):
    mapa_ordinal = {
        "1.er": "primer",
        "2.do": "segundo",
        "3.er": "tercero",
        "4.to": "cuarto",
        "5.to": "quinto",
        "6.to": "sexto",
        "7.mo": "séptimo",
        "8.vo": "octavo",
        "9.no": "noveno",
        "10.mo": "décimo",
    }

    ordinal = match.group(0)
    return mapa_ordinal.get(ordinal, ordinal)

def validar(texto):
    pattern = re.compile(r"\b(\d{1,2})(er|do|ro|to|mo|vo|no)\b")

    texto_remplazado =pattern.sub(reemplazar_original, texto)
    return texto_remplazado


@app.post('/comandos/')
def comandos(texto:str):

    #Aplicacion del reemplazo
    texto_reemplazado = validar(texto)
    content={"respuesta":texto}
    return JSONResponse(content=content, status_code=200)
    try:

        respuesta, n = generarJsonComando(texto_reemplazado)
        
        if respuesta.status_code == 200:
            content={"respuesta":texto}
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
        elif n == -2:
            content={"respuesta":"el texto no tenia nada que ver con una reunion"}
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

        if (num_pro == 1):
            task = projectEntity(db.minutas.find_one({"tipo":"proyecto"}))
            respuesta = templates.TemplateResponse("minuta.html",{"request": request, "combined": task, "res_min": resumen_minuta, "tipo":"proyecto"})
            
        elif (num_pro>1):
            
            tasks = projectsEntity(db.minutas.find({"tipo":"proyecto"}))
            respuesta = templates.TemplateResponse("minuta2.html",{"request": request, "combineds": tasks, "res_min": resumen_minuta, "tipo":"proyecto"})
        elif (num_pro==0):
            return RedirectResponse(url="/", status_code=303)
        return respuesta
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"

    
@app.get('/obtenerTareasIncompletos/')
def obtenerTareasIncompletos(request: Request):
    try:
        db = get_db()
        resumen_minuta = db.minutasResumen.find()
        num_task = db.minutas.count_documents({"tipo": "tarea"})

        if (num_task == 1):
            task = taskEntity(db.minutas.find_one({"tipo":"tarea"}))
            respuesta = templates.TemplateResponse("minuta.html",{"request": request, "combined": task, "res_min": resumen_minuta, "tipo":"tarea"})
            
        elif (num_task>1):
            
            tasks = tasksEntity(db.minutas.find({"tipo":"tarea"}))
            respuesta = templates.TemplateResponse("minuta2.html",{"request": request, "combineds": tasks, "res_min": resumen_minuta, "tipo":"tarea"}) 
        
        elif (num_task==0):
            return RedirectResponse(url="/", status_code=303)

        return respuesta
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"
    
@app.get('/obtenerSprintsIncompletos/')
def obtenerSprintsIncompletos(request: Request):
    try:
        db = get_db()
        resumen_minuta = db.minutasResumen.find()
        num_pro = db.minutas.count_documents({"tipo": "sprint"})

        if (num_pro == 1):
            task = sprintEntity(db.minutas.find_one({"tipo":"sprint"}))
            respuesta = templates.TemplateResponse("minuta.html",{"request": request, "combined": task, "res_min": resumen_minuta, "tipo":"sprint"})
        elif (num_pro>1):
            tasks = sprintsEntity(db.minutas.find({"tipo":"sprint"}))
            respuesta = templates.TemplateResponse("minuta2.html",{"request": request, "combineds": tasks, "res_min": resumen_minuta, "tipo":"sprint"})
        elif (num_pro==0):
            return RedirectResponse(url="/", status_code=303)
        return respuesta
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"


@app.post('/acompletarproyecto/')
def acompletarproyecto(id:str = Form(...), tipo: str = Form(...), accion: str = Form(...), nombre_proyecto: str = Form(...), estado: str = Form(...),
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

    return RedirectResponse(url="/obtenerProyectosIncompletos/", status_code=303)

@app.post('/acompletartarea/')
def acompletartarea(id:str = Form(...), tipo: str = Form(...), accion: str = Form(...), nombre_proyecto: str = Form(...), nombre_tarea: str = Form(...),
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

        db = get_db()

        db.minutas.find_one_and_delete({"_id": ObjectId(id)})
        return RedirectResponse(url="/obtenerTareasIncompletos/", status_code=303)
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"
    
@app.post('/acompletarsprint/')
def acompletartarea(id:str = Form(...), tipo: str = Form(...), accion: str = Form(...), nombre: str = Form(...), estado: str = Form(...),
    fecha_inicio: str = Form(...), fecha_fin: str = Form(...)):

    try:
        datos = {
            "tipo":tipo,
            "accion":accion,
            "nombre":nombre,
            "estado":estado,
            "fecha_inicio":fecha_inicio,
            "fecha_fin":fecha_fin,
        }
        respuesta, n = switch_comandos(datos)

        db = get_db()

        db.minutas.find_one_and_delete({"_id": ObjectId(id)})
        return RedirectResponse(url="/obtenerSprintsIncompletos/", status_code=303)
    except Exception as e:
        return f"Excepción al realizar la solicitud: {e}"
    

@app.post("/CrearTarea/")
def CrearTarea(nombre_tarea: str = Form(...), estado: str = Form(...), prioridad: str = Form(...), nombre_persona: str = Form(...),
                resumen: str = Form(...), fecha_fin: str = Form(...), fecha_inicio: str = Form(...), nombre_proyecto: str = Form(...), nombre_sprint: str = Form(...)):
    datos = {
        "nombre_tarea": nombre_tarea,
        "nombre_persona": nombre_persona,
        "estado": estado,
        "prioridad": prioridad,
        "resumen": resumen,
        "fecha_inicio":fecha_inicio,
        "fecha_fin": fecha_fin,
        "nombre_proyecto": nombre_proyecto,
        "nombre_sprint": nombre_sprint
    }

    respuesta = cn.crear_tarea(datos)
    if respuesta.status_code==200:
        return RedirectResponse(url="/", status_code=303)

@app.post("/EditarTarea/")
def EditarTarea(nombre_tarea: str = Form(...), estado: str = Form(...), prioridad: str = Form(...), nombre_persona: str = Form(...),
                resumen: str = Form(...), fecha_fin: str = Form(...), fecha_inicio: str = Form(...), nombre_proyecto: str = Form(...), nombre_sprint: str = Form(...)):
    datos = {
        "nombre_tarea": nombre_tarea,
        "nombre_persona": nombre_persona,
        "estado": estado,
        "prioridad": prioridad,
        "resumen": resumen,
        "fecha_inicio":fecha_inicio,
        "fecha_fin": fecha_fin,
        "nombre_proyecto": nombre_proyecto,
        "nombre_sprint": nombre_sprint
    }
    return datos
    respuesta = cn.modificar_tarea(datos)
    return RedirectResponse(url="/", status_code=303)

# --- Endpoint Eliminar Tarea ---
@app.get("/EliminarTarea/")
def EliminarTarea(nombre_tarea:str):
    datos = {"nombre_tarea": nombre_tarea}
    return datos
    respuesta = cn.eliminar_tarea(datos)
    return RedirectResponse(url="/", status_code=303)

# --- Endpoint Crear Proyecto ---
@app.post("/CrearProyecto/")
def CrearProyecto(request: Request, nombre_proyecto: str = Form(...), fecha_inicio: str = Form(...), estado: str = Form(...),
    fecha_fin: str = Form(...), prioridad: str = Form(...), nombre_persona: str = Form(...)):
    try:
        datos = {
            "nombre_proyecto": nombre_proyecto,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "prioridad": prioridad,
            "nombre_persona": nombre_persona,
            "estado": estado
        }

        respuesta = cn.crear_proyecto(datos)

        if respuesta.status_code==200:
            
            todo = obtenerTodo()
            todo_json = json.dumps(todo, ensure_ascii=False)
            return templates.TemplateResponse("proyectos.html", {"request": request, "todo": todo_json, "a":True})
        else:
            content={"respuesta":respuesta.status_code}
            return JSONResponse(content=content, status_code=respuesta.status_code)
            return templates.TemplateResponse("proyectos.html", {"request": request, "todo": todo_json, "a":False})
    except:
        datos = {"ab":"no le ande moviendo"}
        return datos
    respuesta = cn.crear_proyecto(datos)
    return RedirectResponse(url="/index.html/", status_code=303)

# --- Endpoint Editar Proyecto ---
@app.post("/EditarProyecto/")
def editarProyecto(id: str = Form(...), nombre_proyecto: str = Form(...), fecha_fin: str = Form(...),fecha_inicio: str = Form(...), nombre_persona:str = Form(...), 
                    prioridad: str = Form(...), estado: str = Form(...)):
    datos = {
        "nombre_proyecto": nombre_proyecto,
        "nombre_persona" : nombre_persona,
        "fecha_inicio" : fecha_inicio,
        "fecha_fin": fecha_fin,
        "prioridad": prioridad,
        "estado": estado
    }
    return datos
    respuesta = cn.modificar_proyecto(datos)
    return RedirectResponse(url="/index.html/", status_code=303)

# --- Endpoint Eliminar Proyecto ---
@app.get("/EliminarProyecto/")
def eliminarProyecto(nombre_proyecto:str):
    datos = {"nombre_proyecto": nombre_proyecto}
    return datos
    respuesta = cn.eliminar_proyecto(datos)
    return RedirectResponse(url="/index.html/", status_code=303)



# --- Endpoint Consultar Proyecto ---
@app.post("/ConsultarProyecto/")
def consultarProyecto(id: str = Form(...)):
    datos = {"id": id}
    respuesta = cn.consultar_proyecto(datos)
    return respuesta


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)