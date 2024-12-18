import json
import requests
from openai import OpenAI

class ComandosNotion:
    def __init__(self):
        self.NOTION_API_URL = "https://api.notion.com/v1/pages"
        self.NOTION_TOKEN = "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"
        self.HEADERS = {
            "Authorization": f"Bearer {self.NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        self.DATABASE_IDS = {
            "tasks": "1232595bac6f812d8674d1f4e4012af9",
            "projects": "1232595bac6f81659e03db547d901cb9",
            "sprints": "1232595bac6f8146a026d520ac1b0fed",
            "minutas": "13f2595bac6f80c1b9e1d5d80cc7bbbe"
        }

    def create_notion_entry(self, database_id, properties):
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        response = requests.post(self.NOTION_API_URL, headers=self.HEADERS, json=data)
        return response

    def crear_tarea(self, data):
        proyecto_id = self.obtener_id_por_nombre(data["nombre_proyecto"], "proyecto")
        sprint_id = self.obtener_id_por_nombre(data["nombre_sprint"], "sprint")
        properties = {
            "Nombre de la tarea": {
                "title": [{"text": {"content": data["nombre_tarea"]}}]
            },
            "Estado": {
                "status": {"name": data.get("estado", "Sin empezar")}
            },
            "Responsable": {
                "select": {"name":data.get("titular", "")}
            },
            "Fecha": {
                "date": {
                    "start": data.get("fecha_inicio", ""),
                    "end": data.get("fecha_fin", "")
                }
            },
            "Prioridad": {
                "select": {"name": data["prioridad"]}
            },
            "Sprint": {
                "relation": [{"id": sprint_id}]
            },
            "Nombre del Proyecto": {
                "relation": [{"id": proyecto_id}]
            },
            "Descripción": {
                "rich_text": [{"text": {"content": data["resumen"]}}]
            }
        }
        respuesta = self.create_notion_entry(self.DATABASE_IDS["tasks"], properties)
        return respuesta

    def crear_proyecto(self, data):
        properties = {
            "Nombre del proyecto": {
                #"title": [{"text": {"content": {"content": data["nombre_proyecto"]}}}]
                "title": [{"text": {"content": data["nombre_proyecto"]}}]
            },
            "Estado": {
                "status": {"name": data["estado"]}
            },
            "Responsable": {
                "select": {"name":data.get("titular", "")}
            },
            "Fechas": {
                "date": {
                    "start": data["fecha_inicio"],
                    "end": data["fecha_fin"]
                }
            },
            "Prioridad": {
                "select": {"name": data["prioridad"]}
            }
        }
        respuesta = self.create_notion_entry(self.DATABASE_IDS["projects"], properties)
        return respuesta

    def crear_sprint(self, data):
        properties = {
            "Nombre del Sprint": {
                "title": [{"text": {"content": data["nombre"]}}]
            },
            "Fechas": {
                "date": {
                    "start": data["fecha_inicio"],
                    "end": data["fecha_fin"]
                }
            },
            "Estado de Sprint": {
                "status": {"name": data["estado"]}
            }
        }
        respuesta = self.create_notion_entry(self.DATABASE_IDS["sprints"], properties)
        return respuesta
    
    def crear_minuta(self, data):
        proyecto_id = self.obtener_id_por_nombre(data["nombre_proyecto"], "proyecto")
        sprint_id = self.obtener_id_por_nombre(data["nombre_sprint"], "sprint")
        properties = {
            "Nombre": {
                "title": [{"text": {"content": data["nombre"]}}]
            },
            "Objetivo": {
                "rich_text": [{"text": {"content": data["objetivo"]}}]
            },
            "Fecha": {
                "date": {"start": data["fecha_inicio"]}
            },
            "Participantes": {
                "multi_select": [{"name": nombre.strip()} for nombre in data["participantes"].split(",")]
            },
            "Resumen": {
                "rich_text": [{"text": {"content": data["resumen"]}}]
            },
            "Sprint": {
                "relation": [{"id": sprint_id}]
            },
            "Proyecto": {
                "relation": [{"id": proyecto_id}]
            }
        }

        respuesta = self.create_notion_entry(self.DATABASE_IDS["minutas"], properties)
        return respuesta
    
    def consultar_datos_notion(self, url_pregunta, cabecera, valor1,tipo, page_size=10):
        if tipo=="minuta":
            valor2="Nombre"
        elif tipo=="tarea":
            valor2="Nombre de la tarea"
        elif tipo=="proyecto":
            valor2="Nombre del proyecto"
        elif tipo=="sprint":
            valor2="Nombre del Sprint"
        # Cuerpo de la solicitud
        busqueda = {
            "page_size": page_size,
            "filter": {
                "and": [
                    {
                        "property": valor2,
                        "title": {
                            "equals": valor1
                        }
                    }
                ]
            }
        }

        try:
            # Realizar la solicitud a la API
            respuesta = requests.post(url_pregunta, headers=cabecera, data=json.dumps(busqueda))
            if respuesta.status_code == 200:
                print("Datos obtenidos con éxito")
                return respuesta.json()
            else:
                print(f"Error {respuesta.status_code}: {respuesta.text}")
                return None
        except Exception as e:
            print(f"Excepción al realizar la solicitud: {e}")
            return None



    def consultar_proyecto(self, data, flag):
        # Validar si 'nombre' está presente en 'data'
        if "nombre" not in data:
            print("Error: Falta el parámetro 'nombre' en los datos proporcionados.")
            return None

        nombre_proyecto = data["nombre"]
        url = "https://api.notion.com/v1/databases/1232595bac6f81659e03db547d901cb9/query"
        tipo=data["tipo"]
        resultado = self.consultar_datos_notion(url, self.HEADERS, nombre_proyecto,tipo, page_size=10)
        if len(resultado.get("results")) == 0:
            return "No se encontrarón resultados"
        else:
            if flag:
                interpretacion=self.interpretar_informacion(resultado)
                return interpretacion
            else:
                return resultado

    def consultar_sprint(self, data, flag):
        # Validar si 'nombre' está presente en 'data'
        if "nombre" not in data:
            print("Error: Falta el parámetro 'nombre' en los datos proporcionados.")
            return None

        nombre_proyecto = data["nombre"]
        tipo=data["tipo"]
        url = "https://api.notion.com/v1/databases/1232595bac6f8146a026d520ac1b0fed/query"
        resultado = self.consultar_datos_notion(url, self.HEADERS, nombre_proyecto,tipo, page_size=10)
        if len(resultado.get("results")) == 0:
            return "No se encontrarón resultados"
        else:
            if flag:
                interpretacion=self.interpretar_informacion(resultado)
                return interpretacion
            else:
                return resultado

    def consultar_tarea(self, data, flag):
        # Validar si 'nombre' está presente en 'data'
        if "nombre" not in data:
            print("Error: Falta el parámetro 'nombre' en los datos proporcionados.")
            return None

        nombre_proyecto = data["nombre"]
        tipo=data["tipo"]
        url = "https://api.notion.com/v1/databases/1232595bac6f812d8674d1f4e4012af9/query"
        resultado = self.consultar_datos_notion(url, self.HEADERS, nombre_proyecto,tipo, page_size=10)
        if len(resultado.get("results")) == 0:
            return "No se encontrarón resultados"
        else:
            if flag:
                interpretacion=self.interpretar_informacion(resultado)
                return interpretacion
            else:
                return resultado


    def interpretar_informacion(self,datos):
        client = OpenAI()
        content = json.dumps(datos)
        # se utiliza el role para que gpt entienda que hacer y content es el contenido del archivo que seleccionamos
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": "interpreta la información y dame un resumen"
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
        return resultado

    def consultar_minuta(self, data, flag):
        # Validar si 'nombre' está presente en 'data'
        if "nombre" not in data:
            print("Error: Falta el parámetro 'nombre' en los datos proporcionados.")
            return None

        nombre = data["nombre"]
        url = "https://api.notion.com/v1/databases/13f2595bac6f80c1b9e1d5d80cc7bbbe/query"
        tipo=data["tipo"]
        resultado = self.consultar_datos_notion(url, self.HEADERS, nombre,tipo, page_size=10)
        if len(resultado.get("results")) == 0:
            return "No se encontrarón resultados"
        else:
            if flag:
                interpretacion=self.interpretar_informacion(resultado)
                return interpretacion
            else:
                return resultado
    
    def obtener_id_por_nombre(self, nombre, tipo):
        """
        Consulta un proyecto, tarea o sprint por nombre y devuelve su ID.
        """
        if tipo == "proyecto":
            resultado = self.consultar_proyecto({"nombre": nombre, "tipo": "proyecto"},False)
        elif tipo == "tarea":
            resultado = self.consultar_tarea({"nombre": nombre, "tipo": "tarea"},False)
        elif tipo == "sprint":
            resultado = self.consultar_sprint({"nombre": nombre, "tipo": "sprint"},False)
        elif tipo == "minuta":
            resultado = self.consultar_minuta({"nombre": nombre, "tipo": "minuta"},False)
        else:
            print("Tipo desconocido.")
            return None

        if resultado and "results" in resultado and len(resultado["results"]) > 0:
            print(resultado["results"][0]["id"])
            return resultado["results"][0]["id"]  # Retorna el ID del primer resultado encontrado
        else:
            print(f"No se encontró ningún {tipo} con el nombre '{nombre}'.")
            return None

    def modificar_proyecto(self, data):
        datos_previos = self.consultar_proyecto({"nombre": data["nombre_proyecto"], "tipo": "proyecto"}, False)
        if not datos_previos:
            return None
        
        id_proyecto = datos_previos["results"][0]["id"]
        datos_previos = datos_previos.get("results")[0]
        aux = datos_previos.get("properties")
        
        # Extraer datos previos
        datos_ant = self.extraer_datos_proyecto(aux)
        modificar = data
        properties = {}
        
        # Modificar el nombre del proyecto si ha cambiado
        if "nombre_nuevo" in modificar:
            if datos_ant["nombre_proyecto"] != modificar["nombre_nuevo"]:
                properties["Nombre del proyecto"] = {"title": [{"text": {"content": modificar["nombre_nuevo"]}}]}
        
        # Modificar el estado si ha cambiado
        if "estado" in modificar:
            if datos_ant["estado"] != modificar["estado"]:
                properties["Estado"] = {"status": {"name": modificar["estado"]}}
        
        # Modificar las fechas
        if "fecha_inicio" in modificar and "fecha_fin" in modificar:
            properties["Fechas"] = {"date": {"start": modificar.get("fecha_inicio"), "end": modificar.get("fecha_fin")}}
        elif "fecha_inicio" in modificar:
            properties["Fechas"] = {"date": {"start": modificar.get("fecha_inicio"), "end": datos_ant.get("fecha_fin")}}
        elif "fecha_fin" in modificar:
            properties["Fechas"] = {"date": {"start": datos_ant.get("fecha_inicio"), "end": modificar.get("fecha_fin")}}
        
        # Modificar la prioridad si ha cambiado
        if "prioridad" in modificar:
            properties["Prioridad"] = {"select": {"name": modificar["prioridad"]}}
        
        # Modificar el responsable si ha cambiado
        if "titular" in modificar:
            if datos_ant["titular"] != modificar["titular"]:
                properties["Responsable"] = {"select": {"name": modificar["titular"]}}

        # Hacer la solicitud PATCH a la API de Notion
        response = requests.patch(f"{self.NOTION_API_URL}/{id_proyecto}", headers=self.HEADERS, json={"properties": properties})
        
        return response
    
    def modificar_tarea(self, data):
        datos_previos = self.consultar_tarea({"nombre": data["nombre_tarea"], "tipo": "tarea"}, False)
        if not datos_previos:
            return None
        id_tarea = datos_previos["results"][0]["id"]
        datos_previos = datos_previos.get("results")[0]
        aux = datos_previos.get("properties")
        datos_ant = self.extraer_datos_tareas(aux)

        properties = {}
        if "nombre_nuevo" in data and datos_ant["nombre_tarea"] != data["nombre_nuevo"]:
            properties["Nombre de la tarea"] = {"title": [{"text": {"content": data["nombre_nuevo"]}}]}
        if "estado" in data and datos_ant["estado"] != data["estado"]:
            properties["Estado"] = {"status": {"name": data["estado"]}}
        if "fecha_inicio" in data or "fecha_fin" in data:
            properties["Fecha"] = {"date": {
                "start": data.get("fecha_inicio", datos_ant["fecha_inicio"]),
                "end": data.get("fecha_fin", datos_ant["fecha_fin"])
            }}
        if "prioridad" in data and datos_ant["prioridad"] != data["prioridad"]:
            properties["Prioridad"] = {"select": {"name": data["prioridad"]}}
        if "nombre_proyecto" in data and datos_ant["nombre_proyecto"] != data["nombre_proyecto"]:
            proyecto_id = self.obtener_id_por_nombre(data["nombre_proyecto"], "proyecto")
            properties["Nombre del Proyecto"] ={"relation": [{"id": proyecto_id}]}
        if "nombre_sprint" in data and datos_ant["nombre_sprint"] != data["nombre_sprint"]:
            sprint_id = self.obtener_id_por_nombre(data["nombre_sprint"], "sprint")
            properties["Sprint"] ={"relation": [{"id": sprint_id}]}
        if "resumen" in data and datos_ant["resumen"] != data["resumen"]:
            properties["Descripción"] = {"rich_text": [{"text": {"content": data["resumen"]}}]}
        if "titular" in data:
            if datos_ant["titular"] != data["titular"]:
                properties["Responsable"] = {"select": {"name": data["titular"]}}
        response = requests.patch(f"{self.NOTION_API_URL}/{id_tarea}", headers=self.HEADERS, json={"properties": properties})
        return response

    def modificar_sprint(self, data):
        datos_previos = self.consultar_sprint({"nombre": data["nombre"], "tipo": "sprint"}, False)
        if not datos_previos:
            return None
        id_sprint = datos_previos["results"][0]["id"]
        datos_previos = datos_previos.get("results")[0]
        aux = datos_previos.get("properties")
        datos_ant = {
            "nombre": aux.get("Nombre del Sprint", {}).get("title", [{}])[0].get("plain_text", ""),
            "estado": aux.get("Estado de Sprint", {}).get("status", {}).get("name", ""),
            "fecha_inicio": aux.get("Fechas", {}).get("date", {}).get("start", ""),
            "fecha_fin": aux.get("Fechas", {}).get("date", {}).get("end", "")
        }

        properties = {}
        if "nombre_nuevo" in data and datos_ant["nombre"] != data["nombre_nuevo"]:
            properties["Nombre del Sprint"] = {"title": [{"text": {"content": data["nombre_nuevo"]}}]}
        if "estado" in data and datos_ant["estado"] != data["estado"]:
            properties["Estado de Sprint"] = {"status": {"name": data["estado"]}}
        if "fecha_inicio" in data or "fecha_fin" in data:
            properties["Fechas"] = {"date": {
                "start": data.get("fecha_inicio", datos_ant["fecha_inicio"]),
                "end": data.get("fecha_fin", datos_ant["fecha_fin"])
            }}

        response = requests.patch(f"{self.NOTION_API_URL}/{id_sprint}", headers=self.HEADERS, json={"properties": properties})
        return response
    def modificar_minuta(self, data):
        datos_previos = self.consultar_minuta({"nombre": data["nombre"], "tipo": "minuta"}, False)
        if not datos_previos:
            return None
        id_minuta = datos_previos["results"][0]["id"]
        datos_previos = datos_previos.get("results")[0]
        aux = datos_previos.get("properties")
        datos_ant = {
            "nombre": aux.get("Nombre", {}).get("title", [{}])[0].get("plain_text", ""),
            "objetivo": aux.get("Objetivo", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "fecha_inicio": aux.get("Fecha", {}).get("date", {}).get("start", ""),
            "participantes": aux.get("Participantes", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "resumen": aux.get("Resumen", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "nombre_sprint": aux.get("Sprint", {}).get("relation", [{}])[0].get("id", ""),
            "nombre_proyecto": aux.get("Proyecto", {}).get("relation", [{}])[0].get("id", "")
        }

        properties = {}
        if "nombre_nuevo" in data and datos_ant["nombre"] != data["nombre_nuevo"]:
            properties["Nombre"] = {"title": [{"text": {"content": data["nombre_nuevo"]}}]}
        if "objetivo" in data and datos_ant["objetivo"] != data["objetivo"]:
            properties["Objetivo"] = {"rich_text": [{"text": {"content": data["objetivo"]}}]}
        if "fecha_inicio" in data and datos_ant["fecha_inicio"] != data["fecha_inicio"]:
            properties["Fecha"] = {"date": {"start": data["fecha_inicio"]}}
        if "participantes" in data and datos_ant["participantes"] != data["participantes"]:
            properties["Participantes"] = {"multi_select": [{"name": nombre.strip()} for nombre in data["participantes"].split(",")]}
        if "resumen" in data and datos_ant["resumen"] != data["resumen"]:
            properties["Resumen"] = {"rich_text": [{"text": {"content": data["resumen"]}}]}
        if "nombre_sprint" in data and datos_ant["nombre_sprint"] != data["nombre_sprint"]:
            sprint_id = self.obtener_id_por_nombre(data["nombre_sprint"], "sprint")
            properties["Sprint"] = {"relation": [{"id": sprint_id}]}
        if "nombre_proyecto" in data and datos_ant["nombre_proyecto"] != data["nombre_proyecto"]:
            proyecto_id = self.obtener_id_por_nombre(data["nombre_proyecto"], "proyecto")
            properties["Proyecto"] = {"relation": [{"id": proyecto_id}]}

        response = requests.patch(f"{self.NOTION_API_URL}/{id_minuta}", headers=self.HEADERS, json={"properties": properties})
        return response
    def extraer_datos_minuta(self, aux):
        def obtener_valor(diccionario, *claves):
            """Función auxiliar para obtener valores anidados de forma segura."""
            for clave in claves:
                if isinstance(diccionario, dict):
                    diccionario = diccionario.get(clave)
                else:
                    return ""
            return diccionario if diccionario else ""

        participantes = [
            item.get("name", "") for item in aux.get("Participantes", {}).get("multi_select", [])
        ]
        participantes_str = ", ".join(participantes)
        return {
            "nombre": obtener_valor(aux, "Nombre", "title", 0, "plain_text"),
            "objetivo": obtener_valor(aux, "Objetivo", "rich_text", 0, "plain_text"),
            "fecha_inicio": obtener_valor(aux, "Fecha", "date", "start"),
            "participantes": participantes_str,
            "resumen": obtener_valor(aux, "Resumen", "rich_text", 0, "plain_text"),
            "nombre_sprint": obtener_valor(aux, "Sprint", "relation", 0, "id"),
            "nombre_proyecto": obtener_valor(aux, "Proyecto", "relation", 0, "id"),
        }

    def extraer_datos_sprint(self, aux):
        def obtener_valor(diccionario, *claves):
            """Función auxiliar para obtener valores anidados de forma segura."""
            for clave in claves:
                if isinstance(diccionario, dict):
                    diccionario = diccionario.get(clave)
                else:
                    return ""
            return diccionario if diccionario else ""

        return {
            "nombre": obtener_valor(aux, "Nombre del Sprint", "title", 0, "plain_text"),
            "estado": obtener_valor(aux, "Estado de Sprint", "status", "name"),
            "fecha_inicio": obtener_valor(aux, "Fechas", "date", "start"),
            "fecha_fin": obtener_valor(aux, "Fechas", "date", "end"),
        }

    def extraer_datos_tareas(self, aux):
        def obtener_valor(diccionario, *claves):
            """Función auxiliar para obtener valores anidados de forma segura."""
            for clave in claves:
                if isinstance(diccionario, dict):
                    diccionario = diccionario.get(clave)
                else:
                    return ""
            return diccionario if diccionario else ""

        return {
            "nombre_tarea": obtener_valor(aux, "Nombre de la tarea", "title", 0, "plain_text"),
            "estado": obtener_valor(aux, "Estado", "status", "name"),
            "fecha_inicio": obtener_valor(aux, "Fecha", "date", "start"),
            "fecha_fin": obtener_valor(aux, "Fecha", "date", "end"),
            "prioridad": obtener_valor(aux, "Prioridad", "select", "name"),
            "nombre_proyecto": obtener_valor(aux, "Nombre del Proyecto", "relation", 0, "id"),
            "nombre_sprint": obtener_valor(aux, "Sprint", "relation", 0, "id"),
            "resumen": obtener_valor(aux, "Descripción", "rich_text", 0, "plain_text"),
            "titular": obtener_valor(aux, "Responsable", "select", "name"),
        }

    def extraer_datos_proyecto(self, json_completo):
        def obtener_valor(diccionario, *claves):
            """Función auxiliar para obtener valores anidados de forma segura."""
            for clave in claves:
                if isinstance(diccionario, dict):
                    diccionario = diccionario.get(clave)
                else:
                    return ""
            return diccionario if diccionario else ""

        return {
            "nombre_proyecto": obtener_valor(json_completo, "Nombre del proyecto", "title", 0, "plain_text"),
            "estado": obtener_valor(json_completo, "Estado", "status", "name"),
            "titular": obtener_valor(json_completo, "Responsable", "select", "name"),
            "fecha_inicio": obtener_valor(json_completo, "Fechas", "date", "start"),
            "fecha_fin": obtener_valor(json_completo, "Fechas", "date", "end"),
            "prioridad": obtener_valor(json_completo, "Prioridad", "select", "name"),
        }

    def eliminar_minuta(self, nombre_minuta):
        id_minuta = self.obtener_id_por_nombre(nombre_minuta, "minuta")
        if not id_minuta:
            print(f"No se encontró ninguna minuta con el nombre '{nombre_minuta}' para archivar.")
            return None
        
        # Realizar la acción de archivo
        response = requests.patch(
            f"{self.NOTION_API_URL}/{id_minuta}",
            headers=self.HEADERS,
            json={"archived": True}
        )
        return response

    def eliminar_tarea(self, nombre_tarea):
        id_tarea = self.obtener_id_por_nombre(nombre_tarea, "tarea")
        if not id_tarea:
            print(f"No se encontró ninguna tarea con el nombre '{nombre_tarea}' para archivar.")
            return None

        # Verificar ID obtenido
        print(f"ID obtenido para '{nombre_tarea}': {id_tarea}")
        
        # Realizar la acción de archivo
        response = requests.patch(
            f"{self.NOTION_API_URL}/{id_tarea}",
            headers=self.HEADERS,
            json={"archived": True}
        )
        if response.status_code == 200:
            print("Tarea archivada con éxito")
        else:
            print(f"Error al archivar la tarea: {response.status_code} - {response.text}")

        return response
    
    def eliminar_proyecto(self, nombre_proyecto):
        id_proyecto = self.obtener_id_por_nombre(nombre_proyecto, "proyecto")
        if not id_proyecto:
            print(f"No se encontró ningún proyecto con el nombre '{nombre_proyecto}' para archivar.")
            return None

        # Verificar ID obtenido
        print(f"ID obtenido para '{nombre_proyecto}': {id_proyecto}")
        
        # Realizar la acción de archivo
        response = requests.patch(
            f"{self.NOTION_API_URL}/{id_proyecto}",
            headers=self.HEADERS,
            json={"archived": True}
        )
        if response.status_code == 200:
            print("Proyecto archivado con éxito")
        else:
            print(f"Error al archivar el proyecto: {response.status_code} - {response.text}")

        return response 
    
    def eliminar_sprint(self, nombre_sprint):
        id_sprint = self.obtener_id_por_nombre(nombre_sprint, "sprint")
        if not id_sprint:
            print(f"No se encontró ningún sprint con el nombre '{nombre_sprint}' para archivar.")
            return None

        # Verificar ID obtenido
        print(f"ID obtenido para '{nombre_sprint}': {id_sprint}")
        
        # Realizar la acción de archivo
        response = requests.patch(
            f"{self.NOTION_API_URL}/{id_sprint}",
            headers=self.HEADERS,
            json={"archived": True}
        )
        if response.status_code == 200:
            print("Sprint archivado con éxito")
        else:
            print(f"Error al archivar el sprint: {response.status_code} - {response.text}")
        return response

    def consultar_datos_notion(self, url_pregunta, cabecera, valor1, tipo, page_size=10):
        if tipo == "minuta":
            valor2 = "Nombre"
        elif tipo == "tarea":
            valor2 = "Nombre de la tarea"
        elif tipo == "proyecto":
            valor2 = "Nombre del proyecto"
        elif tipo == "sprint":
            valor2 = "Nombre del Sprint"
        else:
            print(f"Tipo desconocido: {tipo}")
            return None

        # Cuerpo de la solicitud
        busqueda = {
            "page_size": page_size,
            "filter": {
                "and": [
                    {
                        "property": valor2,
                        "title": {
                            "equals": valor1  # Asegúrate de que valor1 sea un string válido
                        }
                    }
                ]
            }
        }

        try:
            # Realizar la solicitud a la API
            respuesta = requests.post(url_pregunta, headers=cabecera, data=json.dumps(busqueda))
            if respuesta.status_code == 200:
                print("Datos obtenidos con éxito")
                return respuesta.json()
            else:
                print(f"Error {respuesta.status_code}: {respuesta.text}")
                return None
        except Exception as e:
            print(f"Excepción al realizar la solicitud: {e}")
            return None

        
    def consultar_todo_notion(self, url_pregunta, cabecera, tipo, page_size=10):
        if tipo == "minuta":
            valor2 = "Nombre"
        elif tipo == "tarea":
            valor2 = "Nombre de la tarea"
        elif tipo == "proyecto":
            valor2 = "Nombre del proyecto"
        elif tipo == "sprint":
            valor2 = "Nombre del Sprint"

        # Cuerpo de la solicitud SIN filtro
        busqueda = {
            "page_size": page_size
        }

        try:
            # Realizar la solicitud a la API
            respuesta = requests.post(url_pregunta, headers=cabecera, data=json.dumps(busqueda))
            if respuesta.status_code == 200:
                return respuesta.json()
            else:
                print(f"Error {respuesta.status_code}: {respuesta.text}")
                return None
        except Exception as e:
            print(f"Excepción al realizar la solicitud: {e}")
            return None


    def obtener_nombres(self, tipo):
        """
        Obtiene todos los nombres de una base de datos específica.
        """
        if tipo == "proyecto":
            url = "https://api.notion.com/v1/databases/1232595bac6f81659e03db547d901cb9/query"
        elif tipo == "sprint":
            url = "https://api.notion.com/v1/databases/1232595bac6f8146a026d520ac1b0fed/query"
        elif tipo == "tarea":
            url = "https://api.notion.com/v1/databases/1232595bac6f812d8674d1f4e4012af9/query"
        elif tipo == "minuta":
            url = "https://api.notion.com/v1/databases/13f2595bac6f80c1b9e1d5d80cc7bbbe/query"
        else:
            print("Error: Tipo desconocido.")
            return None

        datos = self.consultar_todo_notion(url, self.HEADERS, tipo, page_size=100)

        if datos and "results" in datos:
            nombres = []
            for entrada in datos["results"]:
                propiedades = entrada.get("properties", {})
                if tipo == "proyecto":
                    nombre = propiedades.get("Nombre del proyecto", {}).get("title", [{}])[0].get("plain_text", "")
                elif tipo == "sprint":
                    nombre = propiedades.get("Nombre del Sprint", {}).get("title", [{}])[0].get("plain_text", "")
                elif tipo == "tarea":
                    nombre = propiedades.get("Nombre de la tarea", {}).get("title", [{}])[0].get("plain_text", "")
                elif tipo == "minuta":
                    nombre = propiedades.get("Nombre", {}).get("title", [{}])[0].get("plain_text", "")
                
                if nombre:
                    nombres.append(nombre)
            
            return nombres
        else:
            return "No se encontraron datos."

        
    # Ejemplo de uso
    #texto = """SIPIT, crea una tarea con nombre "probando", que tenga fecha de inicio "01-11-2024" y con una fecha de conclusión "15-11-2024",
    #con un nivel de prioridad "Alta", con la descripción "Revisar y ajustar los puntos críticos del proyecto", la persona asignada es Sam, y el estado es En curso."""
    #CrearTarea(texto)

def main(data):
    cn = ComandosNotion()
    for item in data:
        accion=item.get("accion")
        if accion =="crear":
            tipo = item.get("tipo")
            print(accion)
            if tipo == "tarea":
                cn.crear_tarea(item)
            elif tipo == "proyecto":
                cn.crear_proyecto(item)
            elif tipo == "sprint":
                cn.crear_sprint(item)
            elif tipo == "minuta":
                cn.crear_minuta(item)
            else:
                print(f"Tipo desconocido: {tipo}")
        elif accion == "verTodo":
            tipo = item.get("tipo")
            if tipo == "proyecto":
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
                    print(a)
            elif tipo == "sprint":
                # Obtener todos los nombres de los sprints
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
                    print(a)
            elif tipo == "tarea":
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
                    print(a)
            elif tipo == "minuta":
            # Obtener todos los nombres de las minutas
                nombres_minutas = cn.obtener_nombres("minuta")
                print("Minutas:", nombres_minutas)
                for name in nombres_minutas:
                    item = {
                        "tipo": "minuta",
                        "accion": "consultar",
                        "nombre": name
                    }
                    datos_previos = cn.consultar_minuta(item, False)
                    datos_previos = datos_previos.get("results")[0]
                    n = datos_previos.get("properties")
                    a = cn.extraer_datos_minuta(n)
                    print(a)
        elif accion == "consultar":
            tipo = item.get("tipo")
            if tipo == "tarea":
                n=cn.consultar_tarea(item, True)
                print(n)
            elif tipo == "proyecto":
                datos_previos = cn.consultar_proyecto(item, False)
                datos_previos = datos_previos.get("results")[0]
                n = datos_previos.get("properties")
                
                a = cn.extraer_datos_proyecto(n)
                print(a)
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
                cn.modificar_tarea(item)
            elif tipo == "proyecto":
                cn.modificar_proyecto(item)
            elif tipo == "sprint":
                cn.modificar_sprint(item)
                print("si?")
            elif tipo == "minuta":
                cn.modificar_minuta(item)
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

if __name__ == "__main__":
    # JSON de ejemplo
    data = [
        
        {
        "tipo": "proyecto",
        "accion": "consultar",
        "nombre": "YUJU"
    }
    ]
    main(data)