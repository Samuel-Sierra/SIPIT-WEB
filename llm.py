from openai import OpenAI
from datetime import datetime
import json
from notion import ComandosNotion

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

def generarJsonComando(content):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": f"Eres un asistente muy util y perspicaz que toma notas en reuniones. Recuerda que la fecha de hoy es {fecha_hora_actual} en caso de no tener fecha de inicio asume que empieza en este momento, lee detalladamente la reunion y para cada tarea asignada en la reunión devuelve un diccionario JSON con el formato: {{'tipo': 'tarea','accion': 'valor','nombre_proyecto': 'valor', 'nombre_tarea':'valor', 'nombre_persona': 'valor', 'estado' : 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}, accion indica si se desea eliminar o crear, prioridad solo puede tomar valores baja media y alta, el nombre de la persona debe ser el nombre de la persona a la que se le asigno la tarea. Para cada proyecto debes devolver un json con el siguiente formato{{'tipo':'proyecto', 'accion':'valor', 'nombre_proyecto': 'valor','estado':'valor',  'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}} s  si se desea hacer un nuevo sprint devuelve un diccionario json con el formato: {{ tipo : sprint, nombre : valor, fecha_inicio : YYYY-MM-DD, fecha_fin : YYYY-MM-DD}} si alguno de los valores no viene en el texto, trata de inferirlo solo con la informacion del texto, si no se puede dejalo vacío. es importante que no inventes ningun dato. únicamente devuelve el JSON, con comillas dobles, sin comentarios ni explicación ni acentos"
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
    incompletos = []

    if all(datos[key] != "" for key in datos):  # Verificar si no hay campos vacíos
        completos.append(datos)
        respuesta, n = switch_comandos(datos)
        return respuesta, n 
    else:
        incompletos.append(datos)

def generarJsonMinuta(content):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": f"Eres un asistente muy util y perspicaz que toma notas en reuniones. Recuerda que la fecha de hoy es {fecha_hora_actual} en caso de no tener fecha de inicio asume que empieza en este momento, lee detalladamente la reunion y para cada tarea asignada en la reunión devuelve un diccionario JSON con el formato: {{'tipo': 'tarea','accion': 'valor','nombre_proyecto': 'valor', 'nombre_tarea':'valor', 'nombre_persona': 'valor', 'estado' : 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}, accion indica si se desea eliminar o crear, prioridad solo puede tomar valores baja media y alta, el nombre de la persona debe ser el nombre de la persona a la que se le asigno la tarea. Para cada proyecto debes devolver un json con el siguiente formato{{'tipo':'proyecto', 'accion':'valor', 'nombre_proyecto': 'valor','estado':'valor',  'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}} s  si se desea hacer un nuevo sprint devuelve un diccionario json con el formato: {{ tipo : sprint, nombre : valor, fecha_inicio : YYYY-MM-DD, fecha_fin : YYYY-MM-DD}} si alguno de los valores no viene en el texto, trata de inferirlo solo con la informacion del texto, si no se puede dejalo vacío. es importante que no inventes ningun dato. únicamente devuelve el JSON sin comentarios ni explicación ni acentos"
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

    # Clasificar los datos
    for dato in datos:
        if all(dato[key] != "" for key in dato):  # Verificar si no hay campos vacíos
            completos.append(dato)
        else:
            incompletos.append(dato)


    if completos !=[] :
        respuesta, n = switch_comandos(completos)
        return respuesta, n 
