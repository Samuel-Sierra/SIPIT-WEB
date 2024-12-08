from openai import OpenAI
from datetime import datetime
import json

fecha_hora_actual = datetime.now()
client = OpenAI()

def generarJson(content):

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": f"Eres un asistente muy util y perspicaz que toma notas en reuniones. Recuerda que la fecha de hoy es {fecha_hora_actual} en caso de no tener fecha de inicio asume que empieza en este momento, lee detalladamente la reunion y para cada tarea asignada en la reunión devuelve un diccionario JSON con el formato: {{'tipo': 'tarea','accion': 'valor','nombre_proyecto': 'valor', 'nombre_tarea':'valor', 'nombre_persona': 'valor', 'estado' : 'valor', 'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}}, accion indica si se desea eliminar o crear, prioridad solo puede tomar valores baja media y alta, el nombre de la persona debe ser el nombre de la persona a la que se le asigno la tarea. Para cada proyecto debes devolver un json con el siguiente formato{{'tipo':'proyecto', 'accion':'valor', 'nombre_proyecto': 'valor','estado':'valor',  'fecha_inicio': 'YYYY-MM-DD', 'fecha_fin': 'YYYY-MM-DD', 'prioridad': 'valor', 'resumen': 'valor'}} s  si se desea hacer un nuevo sprint devuelve un diccionario json con el formato: {{ tipo : sprint, nombre : valor, fecha_inicio : YYYY-MM-DD, fecha_fin : YYYY-MM-DD}} si alguno de los valores no viene en el texto, trata de inferirlo solo con la informacion del texto, si no se puede dejalo vacío. es importante que no inventes ningun dato. únicamente devuelve el JSON sin comentarios ni explicación"
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

    # Guardar los datos completos en un archivo JSON
    with open("datos_completos.json", "w", encoding="utf-8") as archivo_completos:
        json.dump(completos, archivo_completos, ensure_ascii=False, indent=4)

    # Guardar los datos incompletos en otro archivo JSON
    with open("datos_incompletos.json", "w", encoding="utf-8") as archivo_incompletos:
        json.dump(incompletos, archivo_incompletos, ensure_ascii=False, indent=4)

    print("Los datos han sido almacenados en 'datos_completos.json' y 'datos_incompletos.json'")

    # Resultados
    print("Datos completos:")
    print(json.dumps(completos, indent=4))

    print("\nDatos incompletos:")
    print(json.dumps(incompletos, indent=4))




