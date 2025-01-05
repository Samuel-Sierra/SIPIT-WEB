from openai import OpenAI
from datetime import datetime
import json
from notion import ComandosNotion
from fastapi.responses import JSONResponse
from config.db import get_db
import os

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

    return respuesta, n

def switch_comandos(data):

    respuesta=[]
    n=""
    item=data
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
        n = "El comando "+accion +tipo 
        if (respuesta.status_code==200):
            n = n + " se concreto correctamente"
        else: 
            n = n + " no se concreto"

    elif accion == "consultar":
        tipo = item.get("tipo")
        if tipo == "tarea":
            nombre = item.get("nombre_tarea")
            data = {"nombre": nombre, "tipo": "tarea"}
            respuesta=JSONResponse(content="", status_code=200)
            n=cn.consultar_tarea(data, True)
            
        elif tipo == "proyecto":
            nombre = item.get("nombre_proyecto")
            data = {"nombre": nombre, "tipo": "proyecto"}
            respuesta=JSONResponse(content="", status_code=200)
            n = cn.consultar_proyecto(data, True)

        elif tipo == "sprint":
            nombre = item.get("nombre")
            data = {"nombre": nombre, "tipo": "sprint"}
            respuesta=JSONResponse(content="", status_code=200)
            n = cn.consultar_sprint(data, True)

        elif tipo == "minuta":
            n = cn.consultar_minuta(item, True)

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
        elif tipo == "minuta":
            respuesta = cn.modificar_minuta(item)
        else:
            print(f"Tipo desconocido: {tipo}")

        n = "El comando "+accion +tipo 
        if (respuesta.status_code==200):
            n = n + " se concreto correctamente"
        else: 
            n = n + " no se concreto"
            
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
    
    return respuesta, n

def generarJsonComando(content):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": f"Eres un asistente muy util y perspicaz que analiza comandos. Recuerda que la fecha de hoy es {fecha_hora_actual} en caso de no tener fecha de inicio asume que empieza en este momento, lee detalladamente el comando, si menciona alguna tarea devuelve un diccionario JSON con el formato: {{'tipo': 'tarea','accion': 'valor','nombre_proyecto': 'valor', 'nombre_tarea':'valor', 'nombre_persona': 'valor','nombre_sprint':'valor' , 'estado' : 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}, si se menciona un proyecto debes devolver un json con el siguiente formato {{'tipo':'proyecto', 'accion':'valor', 'nombre_persona':'valor', 'nombre_proyecto': 'valor','estado':'valor', 'fecha_inicio':'YYYY-MM-DD', 'fecha_fin':'YYYY-MM-DD', 'prioridad':'valor'}} si se menciona un sprint devuelve un diccionario json con el formato: {{ 'tipo':'sprint', 'accion':'valor', 'nombre' : 'valor', 'fecha_inicio' : 'YYYY-MM-DD', 'fecha_fin' : 'YYYY-MM-DD', 'estado':'valor'}}  accion indica si se desea crear, consultar o modificar; prioridad solo puede tomar los siguientes valores: baja, media y alta, el nombre de la persona en caso de tipo tarea debe ser el nombre de la persona a la que se le asigno la tarea; los valores que puede tomar en estado de tarea: en curso, sin empezar y hecho. Para el caso de estado en proyecto los valores que puede tomar son: atraso, planificación, pausa, en curso, hecho y cancelado. Para el caso de estado en sprints los valores que puede tomar son: Past, Last, Next, Future y Current. Si alguno de los valores no viene en el texto, trata de inferirlo solo con la informacion del texto, si no se puede dejalo vacío. es importante que no inventes ningun dato. únicamente devuelve el JSON, con comillas dobles, sin comentarios ni explicación ni acentos."
            },
            
            {
                "role": "user",
                "content": content
            }
        ]
    )
    #si se menciona una minuta devuelve un diccionario json con el formato: {{ 'tipo':'sprint', 'accion':'valor', 'nombre' : 'valor', 'objetivo':'valor' 'fecha_inicio' : 'YYYY-MM-DD', 'fecha_fin' : 'YYYY-MM-DD', 'estado':'valor'}}
    response_dict = completion.to_dict()

    # Capturar el mensaje de salida
    output_message = response_dict['choices'][0]['message']['content']

    # Guardar el mensaje en una variable
    resultado = output_message

    # Texto inicial (puede ser una lista o texto que luego se convierte en JSON)
    texto = resultado

    # Convertir el texto a una lista de diccionarios

    datos = json.loads(texto)


    if all(datos[key] != "" for key in datos):  # Verificar si no hay campos vacíos
        
        respuesta, n = switch_comandos(datos)
        return respuesta, n 
    else:
        if datos.get("accion") == "consultar":
            respuesta, n = switch_comandos(datos)
            return respuesta, n
        elif datos.get("tipo")=="tarea" and isinstance(datos, dict) and datos.get("resumen") == "":
            respuesta, n = switch_comandos(datos)
            return respuesta, n
        else:
            return JSONResponse(content="", status_code=206), "datos incompletos"

def generarJsonMinuta(content):

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                "content": (
                f"Eres un asistente eficiente y preciso para tomar notas en reuniones. La fecha de hoy es {fecha_hora_actual}. "
                "Analiza cuidadosamente el contenido de la reunión y genera JSONs en función de la información proporcionada. "
                "Sigue estas reglas: \n\n"
                "1. Para cada tarea asignada, devuelve un JSON con este formato:\n"
                "{'tipo': 'tarea', 'accion': 'crear/eliminar', 'nombre_proyecto': 'valor', 'nombre_tarea': 'valor', 'nombre_sprint':'valor',"
                "'nombre_persona': 'valor', 'estado': 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', "
                "'prioridad': 'baja/media/alta', 'resumen': 'valor'}\n\n"
                "2. Para cada proyecto mencionado, devuelve un JSON con este formato:\n"
                "{'tipo': 'proyecto', 'accion': 'crear/eliminar', 'nombre_proyecto': 'valor', 'estado': 'valor', "
                "'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'baja/media/alta', 'resumen': 'valor'}\n\n"
                "3. Si se menciona un nuevo sprint, devuelve un JSON con este formato:\n"
                "{'tipo': 'sprint', 'accion':'nombre': 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD'}\n\n"
                "Reglas adicionales:\n"
                "-accion indica si se desea crear, consultar o modificar\n"
                "-prioridad solo puede tomar los siguientes valores: baja, media y alta\n"
                "-el nombre de la persona en caso de tipo tarea debe ser el nombre de la persona a la que se le asigno la tarea\n"
                "-los valores que puede tomar en estado son unicamente: En curso, Atraso, Planificación, En pausa, Hecho y Cancelado.-\n"
                "-Para el caso de estado en sprints los valores que puede tomar son: Past, Last, Next, Future y Current.\n"
                "- Si no se menciona explícitamente un valor, infiérelo solo si es razonable hacerlo. De lo contrario, déjalo vacío.\n"
                "- No inventes datos.\n"
                "- Devuelve únicamente los JSONs,  con comillas dobles, sin comentarios ni explicación ni acentos."),
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

        import re
        # Buscar solo las líneas que empiezan y terminan con llaves válidas
        limpio = re.findall(r'\{.*?\}', resultado, re.DOTALL)

        datos = [json.loads(line) for line in limpio]

        # Listas para almacenar los datos completos y los incompletos
        completos = []
        incompletos = []

        # Clasificar los datos
        for dato in datos:
            if all(dato[key] != "" for key in dato):  # Verificar si no hay campos vacíos
                completos.append(dato)
            else:
                incompletos.append(dato)
        status = 2

        if completos !=[] :
            respuesta, n = switch_minuta(completos)
            
        if incompletos !=[] :
            for x in incompletos:
                db = get_db()
                db.minutas.insert_one(x)
            status = 2
        else:
            status = 1

        if incompletos == [] and completos == []:
            return -2

        return status

    except Exception as e:
        return f"Error en jsonminuta {e}"

def generarResumenMinuta(content):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                "content": f"eres una secretaria muy buena, tu trabajo consiste en hacer un resumen de las cosas mas importantes que sucedieron en una reunion, debes hacer el resumen tomando en cuenta las tareas proyectos u otras cosas que se desean crear o eliminar, a quien han sido asignadas la fecha de inicio y fecha de entrega además de los detalles que consideres relevantes considera que hoy es {fecha_hora_actual} y si no te dan fecha de inicio toma el dia de hoy como inicio. Devuelve el resumen sin caracteres especiales ni numeracion."
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
        minuta = output_message
        return minuta
    except Exception as e:
        return f"Error en resumen {e}"