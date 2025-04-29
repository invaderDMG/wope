import os
from dotenv import load_dotenv
from atproto import Client

# Cargar variables del entorno
load_dotenv()

handle = os.getenv("BLUESKY_HANDLE")
password = os.getenv("BLUESKY_PASSWORD")

# Crear cliente y loguearse
client = Client()
client.login(handle, password)

# Publicar un post
text = "Hola, mundo desde Bluesky 🟦 con Python ✨"
client.send_post(text)

print("✅ Post publicado en Bluesky")
