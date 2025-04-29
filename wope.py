import os
import requests
from dotenv import load_dotenv
from atproto import Client, models

# Cargar variables del .env
load_dotenv()

# Texto a publicar (puedes también pasarlo como argumento si lo prefieres)
post_text = "WoPe: ¡Publicando en Threads y Bluesky al mismo tiempo vía API! 🚀"

# ======= THREADS =======
def post_to_threads(text):
    access_token = os.getenv("THREADS_ACCESS_TOKEN")
    user_id = os.getenv("THREADS_USER_NUMBER_ID")

    try:
        print("🛠️  [Threads] Creando contenedor...")
        create_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
        create_params = {
            "media_type": "TEXT",
            "text": text,
            "access_token": access_token
        }
        create_resp = requests.post(create_url, data=create_params)
        create_resp.raise_for_status()
        creation_id = create_resp.json().get("id")

        if not creation_id:
            raise ValueError("No se recibió un media_container_id válido de Threads.")

        print(f"✅ [Threads] Contenedor creado: {creation_id}")

        print("📤 [Threads] Publicando post...")
        publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
        publish_params = {
            "creation_id": creation_id,
            "access_token": access_token
        }
        publish_resp = requests.post(publish_url, data=publish_params)
        publish_resp.raise_for_status()

        print("🎉 [Threads] Post publicado exitosamente.")

    except Exception as e:
        print(f"❌ [Threads] Error al publicar: {e}")


# ======= BLUESKY =======
def post_to_bluesky(text):
    handle = os.getenv("BLUESKY_HANDLE")
    app_password = os.getenv("BLUESKY_PASSWORD")

    try:
        print("🔐 [Bluesky] Autenticando...")
        client = Client()
        client.login(handle, app_password)

        print("📤 [Bluesky] Publicando post...")
        post = client.send_post(text)

        print(f"🎉 [Bluesky] Post publicado. URI: {post.uri}")

    except Exception as e:
        print(f"❌ [Bluesky] Error al publicar: {e}")


# ======= MAIN =======
if __name__ == "__main__":
    post_to_threads(post_text)
    print("—" * 40)
    post_to_bluesky(post_text)
