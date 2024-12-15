from openai import OpenAI
from datetime import datetime
import json
from notion import ComandosNotion
from fastapi.responses import JSONResponse
from config.db import get_db

cn = ComandosNotion()

fecha_hora_actual = datetime.now()
client = OpenAI()

def switch_minuta(data):

    n=""
    for item in data:
        accion=item.get("accion")
        if accion =="crear":
            tipo = item.get("tipo")
            if tipo == "tarea":
                respuesta = cn.crear_tarea(item)
            elif tipo == "proyecto":
                respuesta = cn.crear_proyecto(item)
            elif tipo == "sprint":
                respuesta = cn.crear_sprint(item)
            elif tipo == "minuta":
                respuesta = cn.crear_minuta(item)
            else:
                print(f"Tipo desconocido: {tipo}")

        elif accion == "consultar":
            tipo = item.get("tipo")
            if tipo == "tarea":
                n=cn.consultar_tarea(item, True)
            elif tipo == "proyecto":
                n = cn.consultar_proyecto(item, True)
                print(n)
            elif tipo == "sprint":
                n = cn.consultar_sprint(item, True)
                print(n)
            elif tipo == "minuta":
                n = cn.consultar_minuta(item, True)
                print(n)
            else:
                print(f"Tipo desconocido: {tipo}")

        elif accion == "actualizar":
            tipo = item.get("tipo")
            if tipo == "tarea":
                respuesta = cn.modificar_tarea(item)
            elif tipo == "proyecto":
                respuesta = cn.modificar_proyecto(item)
            elif tipo == "sprint":
                respuesta = cn.modificar_sprint(item)
                print("si?")
            elif tipo == "minuta":
                respuesta = cn.modificar_minuta(item)
            else:
                print(f"Tipo desconocido: {tipo}")
                
        elif accion == "eliminar":
            tipo = item.get("tipo")
            if tipo == "tarea":
                cn.eliminar_tarea(item.get("nombre"))
            elif tipo == "proyecto":
                cn.eliminar_proyecto(item.get("nombre"))
            elif tipo == "sprint":
                cn.eliminar_sprint(item.get("nombre"))
            elif tipo == "minuta":
                cn.eliminar_minuta(item.get("nombre"))
            else:
                print(f"Tipo desconocido: {tipo}")
        n = "El comando "+accion +tipo 
    if (respuesta.status_code==200):
        n = n + " se concreto correctamente"
    else: 
        n = n + " no se concreto"
    return respuesta, n

def switch_comandos(item):

    respuesta=[]
    n=""
    accion=item.get("accion")
    if accion =="crear":
        tipo = item.get("tipo")
        if tipo == "tarea":
            respuesta = cn.crear_tarea(item)
        elif tipo == "proyecto":
            respuesta = cn.crear_proyecto(item)
        elif tipo == "sprint":
            respuesta = cn.crear_sprint(item)
        elif tipo == "minuta":
            respuesta = cn.crear_minuta(item)
        else:
            print(f"Tipo desconocido: {tipo}")

    elif accion == "consultar":
        tipo = item.get("tipo")
        if tipo == "tarea":
            pren = cn.consultar_tarea(item, True)
            
        elif tipo == "proyecto":
            pren = cn.consultar_proyecto(item, True)

        elif tipo == "sprint":
            pren = cn.consultar_sprint(item, True)

        elif tipo == "minuta":
            pren = cn.consultar_minuta(item, True)

        else:
            print(f"Tipo desconocido: {tipo}")
        if pren != 0:
            n = pren

    elif accion == "actualizar":
        tipo = item.get("tipo")
        if tipo == "tarea":
            respuesta = cn.modificar_tarea(item)
        elif tipo == "proyecto":
            respuesta = cn.modificar_proyecto(item)
        elif tipo == "sprint":
            respuesta = cn.modificar_sprint(item)
        elif tipo == "minuta":
            respuesta = cn.modificar_minuta(item)
        else:
            print(f"Tipo desconocido: {tipo}")
            
    elif accion == "eliminar":
        tipo = item.get("tipo")
        if tipo == "tarea":
            cn.eliminar_tarea(item.get("nombre"))
        elif tipo == "proyecto":
            cn.eliminar_proyecto(item.get("nombre"))
        elif tipo == "sprint":
            cn.eliminar_sprint(item.get("nombre"))
        elif tipo == "minuta":
            cn.eliminar_minuta(item.get("nombre"))
        else:
            print(f"Tipo desconocido: {tipo}")

    if accion != "consultar":
        n = "El comando "+accion +tipo 
        if (respuesta.status_code==200):
            n = n + " se concreto correctamente"
        else: 
            n = n + " no se concreto"

    return respuesta, n

def generarJsonComando(content):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": f"Eres un asistente muy util y perspicaz que toma notas en reuniones. Recuerda que la fecha de hoy es {fecha_hora_actual} en caso de no tener fecha de inicio asume que empieza en este momento, lee detalladamente la reunion y para cada tarea asignada en la reunión devuelve un diccionario JSON con el formato: {{'tipo': 'tarea','accion': 'valor','nombre_proyecto': 'valor', 'nombre_tarea':'valor', 'nombre_persona': 'valor', 'estado' : 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}, accion indica si se desea eliminar o crear, prioridad solo puede tomar valores baja media y alta, el nombre de la persona debe ser el nombre de la persona a la que se le asigno la tarea. Para cada proyecto debes devolver un json con el siguiente formato{{'tipo':'proyecto', 'accion':'valor', 'nombre_proyecto': 'valor','estado':'valor',  'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}  si se desea hacer un nuevo sprint devuelve un diccionario json con el formato: {{ tipo : sprint, nombre : valor, fecha_inicio : YYYY-MM-DD, fecha_fin : YYYY-MM-DD}} si alguno de los valores no viene en el texto, trata de inferirlo solo con la informacion del texto, si no se puede dejalo vacío. es importante que no inventes ningun dato. únicamente devuelve el JSON, con comillas dobles, sin comentarios ni explicación ni acentos. Los valores que puede tomar en estado son unicamente: En curso, Atraso, Planificación, En pausa, Hecho y Cancelado"
            },
            
            {
                "role": "user",
                "content": content
            }
        ]
    )
    response_dict = completion.to_dict()

    # Capturar el mensaje de salida
    output_message = response_dict['choices'][0]['message']['content']

    # Guardar el mensaje en una variable
    resultado = output_message

    # Texto inicial (puede ser una lista o texto que luego se convierte en JSON)
    texto = resultado

    print(texto)

    # Convertir el texto a una lista de diccionarios

    datos = json.loads(texto)

    # Listas para almacenar los datos completos y los incompletos
    completos = []

    if all(datos[key] != "" for key in datos):  # Verificar si no hay campos vacíos
        completos.append(datos)
        respuesta, n = switch_comandos(datos)
        return respuesta, n 
    else:
        return JSONResponse(content="", status_code=206), "datos incompletos"

def generarJsonMinuta(content):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": f"Eres un asistente muy util y perspicaz que toma notas en reuniones. Recuerda que la fecha de hoy es {fecha_hora_actual} en caso de no tener fecha de inicio asume que empieza en este momento, lee detalladamente la reunion y para cada tarea asignada en la reunión devuelve un diccionario JSON con el formato: {{'id': '{1}', 'tipo': 'tarea','accion': 'valor','nombre_proyecto': 'valor', 'nombre_tarea':'valor', 'nombre_persona': 'valor', 'estado' : 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}, accion indica si se desea eliminar o crear, prioridad solo puede tomar valores baja media y alta, el nombre de la persona debe ser el nombre de la persona a la que se le asigno la tarea. Para cada proyecto debes devolver un json con el siguiente formato{{'id': '{1}','tipo':'proyecto', 'accion':'valor', 'nombre_proyecto': 'valor','estado':'valor',  'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}} si se desea hacer un nuevo sprint devuelve un diccionario json con el formato: {{'id': '{1}', tipo : sprint, nombre : valor, fecha_inicio : YYYY-MM-DD, fecha_fin : YYYY-MM-DD}} si alguno de los valores no viene en el texto, trata de inferirlo solo con la informacion del texto, si no se puede dejalo vacío. es importante que no inventes ningun dato. únicamente devuelve el JSON, con comillas dobles, sin comentarios ni explicación ni acentos. Los valores que puede tomar en estado son unicamente: En curso, Atraso, Planificación, En pausa, Hecho y Cancelado"
            },
            
            {
                "role": "user",
                "content": content
            }
        ]
    )
    response_dict = completion.to_dict()

    # Capturar el mensaje de salida
    output_message = response_dict['choices'][0]['message']['content']

    # Guardar el mensaje en una variable
    resultado = output_message

    # Texto inicial (puede ser una lista o texto que luego se convierte en JSON)
    texto = resultado

    # Convertir el texto a una lista de diccionarios

    datos = json.loads(texto)

    # Listas para almacenar los datos completos y los incompletos
    completos = []
    incompletos = []
    incompletos.append(id)
    

    # Clasificar los datos
    for dato in datos:
        if all(dato[key] != "" for key in dato):  # Verificar si no hay campos vacíos
            completos.append(dato)
        else:
            incompletos.append(dato)

    respuesta=""
    n=""

    if completos !=[] :
        respuesta, n = switch_comandos(completos)
        
    if incompletos !=[] :
        for x in incompletos:
            db = get_db()
            db.minutas.insert_one(x)
        n = "hay datos incompletos, checar la pagina"

    return respuesta, n 