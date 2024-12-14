from pymongo import MongoClient

def get_db():
    try:
        conn = MongoClient("mongodb+srv://sierrafierrosamuel:JjW11CTZ1jvdbUD6@minutas.appxl.mongodb.net/")
        db = conn.SIPIT
    except ConnectionError:
        print("Error de conexion")
    return db