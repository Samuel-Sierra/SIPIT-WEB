def projectEntity(item) -> dict:
    return{
        "id": str(item["_id"]),
        "tipo":item["tipo"],
        "accion":item["accion"],
        "nombre_proyecto":item["nombre_proyecto"],
        "estado":item["estado"],
        "fecha_inicio":item["fecha_inicio"],
        "fecha_fin":item["fecha_fin"],
        "prioridad":item["prioridad"]
    }

def projectsEntity(entity) -> list:
    [projectEntity(item) for item in entity]

def taskEntity(item) -> dict:
    return{
        "id": str(item["_id"]),
        "tipo":item["tipo"],
        "accion":item["accion"],
        "nombre_proyecto":item["nombre_proyecto"],
        "nombre_tarea":item["nombre_tarea"],
        "nombre_sprint":item["nombre_sprint"],
        "nombre_persona":item["nombre_persona"],
        "estado":item["estado"],
        "fecha_inicio":item["fecha_inicio"],
        "fecha_fin":item["fecha_fin"],
        "prioridad":item["prioridad"],
        "resumen":item["resumen"]
    }

def tasksEntity(entity) -> list:
    return [taskEntity(item) for item in entity]

def resumenEntity(item) ->dict:
    return{
        "id": str(item["_id"]),
        "resumen": item["resumen"]
    }

def resumenesEntity(entity) -> list:
    [resumenEntity(item for item in entity)]