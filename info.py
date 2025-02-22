from notion import ComandosNotion
def obtenerTodo():
    cn = ComandosNotion()
    todo = []
    # Obtener todos los nombres de los proyectos
    nombres_proyectos = cn.obtener_nombres("proyecto")
    for name in nombres_proyectos:
        
        item = {
            "tipo": "proyecto",
            "accion": "consultar",
            "nombre": name
        }
        id_proyecto = cn.obtener_id_por_nombre(name,"proyecto")
        
        datos_previos = cn.consultar_proyecto(item, False)
        datos_previos = datos_previos.get("results")[0]
        n = datos_previos.get("properties")
        
        a = cn.extraer_datos_proyecto(n)
        
        a["nombre_proyecto"] = name
        a["id_proyecto"] = id_proyecto
        a["tipo"] = "proyecto"
        todo.append(a)


    nombres_sprints = cn.obtener_nombres("sprint")
    for name in nombres_sprints:
        item = {
            "tipo": "sprint",
            "accion": "consultar",
            "nombre": name
        }
        id_sprint= cn.obtener_id_por_nombre(name,"sprint")
        datos_previos = cn.consultar_sprint(item, False)
        datos_previos = datos_previos.get("results")[0]
        n = datos_previos.get("properties")
        a = cn.extraer_datos_sprint(n)
        a["nombre_sprint"] = name
        a["id_sprint"] = id_sprint
        a["tipo"] = "sprint"
        todo.append(a)

    # Obtener todos los nombres de las tareas
    nombres_tareas = cn.obtener_nombres("tarea")
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
        a["nombre_tarea"] = name
        a["tipo"] = "tarea"
        todo.append(a)

# Obtener todos los nombres de las minutas
  #  nombres_minutas = cn.obtener_nombres("minuta")
  #  for name in nombres_minutas:
  #      item = {
  #          "tipo": "minuta",
  #          "accion": "consultar",
  ##          "nombre": name
   #     }
   ##     datos_previos = cn.consultar_minuta(item, False)
    #    datos_previos = datos_previos.get("results")[0]
    #    n = datos_previos.get("properties")
     #   a = cn.extraer_datos_minuta(n)
    ##todo.append(a)
    return todo