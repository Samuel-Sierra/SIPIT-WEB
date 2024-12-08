import json
import requests
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
os.environ["GROQ_API_KEY"] = "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"

class comandosNotion:

    def __init__(self):

        self.model = ChatGroq(
            model="llama3-8b-8192",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        
        self.TOKEN_NOTION = "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"
        self.ID_DATABASE = "1232595bac6f812d8674d1f4e4012af9"
        self.URL_CREACION = "https://api.notion.com/v1/pages"
        self.URL_BUSQUEDA = "https://api.notion.com/v1/databases/{}/query".format(self.ID_DATABASE)
        self.URL_ACTUALIZACION = "https://api.notion.com/v1/pages/{page_id}"
        self.CABECERA = {
            "Authorization": f"Bearer {self.TOKEN_NOTION}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

        # Constantes de datos
        self.TITULAR = {
            "id": "notion%3A%2F%2Ftasks%2Fassign_property",
            "type": "people",
            "people": [
                {
                    "object": "user",
                    "id": "52530542-7f01-412e-a370-662a3cb775dc",
                    "name": "Karina Santiago",
                    "type": "person",
                    "person": {
                        "email": "asantiagom1802@alumno.ipn.mx"
                    }
                }
            ]
        }

        self.ETIQUETAS = [{"name": "Web"}, {"name": "Mejora"}]
        self.ESTADO = "En curso"
        self.ID_PROYECTO = "1232595b-ac6f-816c-9240-dae9cbd7dfd8"
    
    def CrearTarea(self,texto):
        # Definir el prompt para extraer valores del texto de entrada
        promptc = ChatPromptTemplate.from_template("""
        Extrae el nombre del proyecto, el nombre de la tarea, la fecha de inicio, la fecha de conclusión, el nivel de prioridad, el nombre
        de la persona a la que esta asignada, el estado y la descripción del siguiente comando:
        {texto}
        y que los valores tengan este formato: nombre_proyecto="valor",nombre_tarea="valor",nombre_persona="valor", estado="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor", resumen="valor".
        Devuelve estos datos como un diccionario JSON con las claves "nombre_proyecto","nombre_tarea","nombre_persona", "estado", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """)

        # Extraer los datos necesarios con el modelo
        chainc = promptc | self.model | StrOutputParser()
        resultado_prompt = chainc.invoke({"texto": texto})
        datos_tarea = json.loads(resultado_prompt)

        # Definir los datos de la nueva entrada combinando los parámetros extraídos y las constantes
        nueva_entrada = {
            "parent": {"database_id": self.ID_DATABASE},
            "properties": {
                "Nombre de la tarea": {
                    "title": [{"text": {"content": datos_tarea["nombre_tarea"]}}]
                },
                "Titular": self.TITULAR,
                #"Estado": {
                #    "status": {"name": ESTADO}
                #},
                "Persona asignada": {
                "multi_select": [{"name": datos_tarea["nombre_persona"]}]
                                    },
                "Estado": {
                    "status": {"name": datos_tarea["estado"]}
                },
                "Fecha": {
                    "date": {
                        "start": datos_tarea["fecha_inicio"],
                        "end": datos_tarea["fecha_fin"]
                    }
                },
                "Proyecto": {
                    "id": "notion%3A%2F%2Ftasks%2Ftask_to_project_relation",
                    "type": "relation",
                    "relation": [{"id": self.ID_PROYECTO}]
                },
                "Prioridad": {
                    "select": {"name": datos_tarea["prioridad"]}
                },
                "Descripción": {
                    "rich_text": [{"text": {"content": datos_tarea["resumen"]}}]
                }
            }
        }

        # Realizar la solicitud POST a la API de Notion para crear una nueva entrada
        respuesta = requests.post(self.URL_CREACION, headers=self.CABECERA, data=json.dumps(nueva_entrada))
        return respuesta


    # Ejemplo de uso
    #texto = """SIPIT, crea una tarea con nombre "probando", que tenga fecha de inicio "01-11-2024" y con una fecha de conclusión "15-11-2024",
    #con un nivel de prioridad "Alta", con la descripción "Revisar y ajustar los puntos críticos del proyecto", la persona asignada es Sam, y el estado es En curso."""
    #CrearTarea(texto)