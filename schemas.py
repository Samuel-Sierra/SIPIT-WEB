def projectEntity(item) -> dict:
    return{
        "tipo":item["tipo"],
        "accion":item["accion"],
        "nombre_proyecto":item["nombre_proyecto"],
        "estado":item["estado"],
        "fecha_inicio":item["fecha_inicio"],
        "fecha_fin":item["fecha_fin"],
        "prioridad":item["prioridad"],
        "resumen":item["resumen"]
    }

def projectsEntity(entity) -> list:
    [projectEntity(item) for item in entity]