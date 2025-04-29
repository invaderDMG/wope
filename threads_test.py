import os
import requests
from dotenv import load_dotenv

# Cargar las variables del entorno
load_dotenv()

# Leer variables del entorno
access_token = os.getenv("THREADS_ACCESS_TOKEN")
user_id = os.getenv("THREADS_USER_NUMBER_ID")
post_text = "¡Este es mi primer post en Threads usando la API! 🚀"

# Paso 1: Crear el contenedor del post (media_container_id)
create_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
create_params = {
    "media_type": "TEXT",
    "text": post_text,
    "access_token": access_token
}

try:
    print("🛠️  Creando contenedor del post...")
    create_response = requests.post(create_url, data=create_params)
    create_response.raise_for_status()
    creation_id = create_response.json().get("id")

    if not creation_id:
        raise ValueError("No se recibió un media_container_id válido en la respuesta.")

    print(f"✅ Contenedor creado con ID: {creation_id}")

    # Paso 2: Publicar el post usando el ID obtenido
    publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
    publish_params = {
        "creation_id": creation_id,
        "access_token": access_token
    }

    print("📤 Publicando el post...")
    publish_response = requests.post(publish_url, data=publish_params)
    publish_response.raise_for_status()

    print("🎉 Post publicado exitosamente en Threads.")

except requests.exceptions.HTTPError as errh:
    print(f"❌ Error HTTP: {errh}")
    print(f"🔍 Respuesta: {errh.response.text}")
except Exception as e:
    print(f"❌ Ocurrió un error general: {e}")
