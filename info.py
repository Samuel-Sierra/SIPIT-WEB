from notion import ComandosNotion
import json
def obtenerTodo():
    cn = ComandosNotion()
    todo = []
    # Obtener todos los nombres de los proyectos
    # Obtener todos los nombres de los proyectos
    nombres_proyectos = cn.obtener_nombres("proyecto")
    print("Proyectos:", nombres_proyectos)
    for name in nombres_proyectos:
        item = {
            "tipo": "proyecto",
            "accion": "consultar",
            "nombre": name
        }
        datos_previos = cn.consultar_proyecto(item, False)
        datos_previos = datos_previos.get("results")[0]
        n = datos_previos.get("properties")
        a = cn.extraer_datos_proyecto(n)
        todo.append(a)
           

    nombres_sprints = cn.obtener_nombres("sprint")
    print("Sprints:", nombres_sprints)
    for name in nombres_sprints:
        item = {
            "tipo": "sprint",
            "accion": "consultar",
            "nombre": name
        }
        datos_previos = cn.consultar_sprint(item, False)
        datos_previos = datos_previos.get("results")[0]
        n = datos_previos.get("properties")
        a = cn.extraer_datos_sprint(n)
        todo.append(a)
            
        # Obtener todos los nombres de las tareas
        nombres_tareas = cn.obtener_nombres("tarea")
        print("Tareas:", nombres_tareas)
    for name in nombres_tareas:
        item = {
            "tipo": "tarea",
            "accion": "consultar",
            "nombre": name
        }
        datos_previos = cn.consultar_tarea(item, False)
        datos_previos = datos_previos.get("results")[0]
        n = datos_previos.get("properties")
        a = cn.extraer_datos_tareas(n)
        todo.append(a)

# Obtener todos los nombres de las minutas
    #nombres_minutas = cn.obtener_nombres("minuta")
    #for name in nombres_minutas:
    #    item = {
    #        "tipo": "minuta",
    #        "accion": "consultar",
    #        "nombre": name
    #    }
    #    datos_previos = cn.consultar_minuta(item, False)
    #    datos_previos = datos_previos.get("results")[0]
    #    n = datos_previos.get("properties")
    #    a = cn.extraer_datos_minuta(n)
    #    a["nombre_minuta"] = name
    #   todo.append(a)
    return todo
