import os
import json
from dotenv import load_dotenv
from atproto import Client
from google import genai
from pymongo import MongoClient

# Cargar las credenciales del  .env
load_dotenv()
BSKY_IDENTIFIER = os.getenv('BSKY_IDENTIFIER')
BSKY_PASSWORD = os.getenv('BSKY_PASSWORD')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Nombres para la entrega
archivo_txt = "1_3_Corrales_Borrego_Israel.txt"
archivo_json = "1_3_Corrales_Borrego_Israel.json"
perfil_objetivo = "stephenking.bsky.social" 


# Conectar a Bluesky y extraer datos
print("Conectando a Bluesky")
client_bsky = Client()
client_bsky.login(BSKY_IDENTIFIER, BSKY_PASSWORD)

# Obtener bio --Ampliación
perfil = client_bsky.get_profile(perfil_objetivo)
biografia = perfil.description if perfil.description else "Sin biografía"

# Obtener los posts del feed
feed = client_bsky.get_author_feed(perfil_objetivo, limit=10)
posts_limpios = []

for item in feed.feed:
    # Obtenemos el texto de forma segura; si no existe, devuelve una cadena vacía
    texto_raw = getattr(item.post.record, 'text', '')
    if texto_raw:
        texto = str(texto_raw).replace('\n', ' ').strip()
        if texto:
            posts_limpios.append(texto)

# 3. Guardar en MongoDB
print("Guardando datos iniciales en MongoDB...")
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["practica_bluesky"]
coleccion = db["analisis_perfiles"]

documento_inicial = {
    "usuario": perfil_objetivo,
    "biografia": biografia,
    "posts": posts_limpios
}

resultado = coleccion.insert_one(documento_inicial)
id_mongo = resultado.inserted_id

# Preparar el prompt y consultar a Gemini
print("Analizando con Gemini")
contexto = "Eres un analista de datos de redes sociales."
feed_unido = "\n".join(posts_limpios)
instrucciones = "Proporciona un resumen breve del tema principal del perfil y el tono de sus publicaciones."

prompt = f"{contexto}\n\nBIOGRAFÍA: {biografia}\n\nPOSTS:\n{feed_unido}\n\nTAREA:\n{instrucciones}"

client_gemini = genai.Client(api_key=GEMINI_API_KEY)
response = client_gemini.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
analisis_texto = response.text

# Generar .txt, actualización en Mongo y .json
print("Generando archivos")

# Guardar respuesta de Gemini en el archivo .txt
with open(archivo_txt, "w", encoding="utf-8") as f:
    f.write(str(analisis_texto or ""))

# Actualizar el documento en MongoDB con el análisis
coleccion.update_one(
    {"_id": id_mongo},
    {"$set": {"analisis_gemini": analisis_texto}}
)

# Recuperar el documento final (excluyendo _id para evitar fallos al exportar a JSON)
documento_final = coleccion.find_one({"_id": id_mongo}, {"_id": 0})

# Guardar el documento completo en el archivo .json
with open(archivo_json, "w", encoding="utf-8") as f:
    json.dump(documento_final, f, ensure_ascii=False, indent=4)

print("Finalizado.")