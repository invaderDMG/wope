from flask import Flask, request, render_template, jsonify
import os
import requests
from dotenv import load_dotenv
from atproto import Client, models

load_dotenv()

app = Flask(__name__)

# Threads
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")
THREADS_USER_ID = os.getenv("THREADS_USER_NUMBER_ID")

# Bluesky
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    content = request.json.get("text")

    result = {"threads": {}, "bluesky": {}}

    # Threads
    try:
        create_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
        create_params = {
            "media_type": "TEXT",
            "text": content,
            "access_token": THREADS_ACCESS_TOKEN
        }

        create_response = requests.post(create_url, data=create_params)
        create_response.raise_for_status()
        creation_id = create_response.json().get("id")

        publish_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
        publish_params = {
            "creation_id": creation_id,
            "access_token": THREADS_ACCESS_TOKEN
        }

        publish_response = requests.post(publish_url, data=publish_params)
        publish_response.raise_for_status()
        result["threads"] = {"status": "success", "message": "Publicado en Threads ✅"}

    except Exception as e:
        result["threads"] = {"status": "error", "message": str(e)}

    # Bluesky
    try:
        client = Client()
        client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
        post = client.send_post(content)
        result["bluesky"] = {"status": "success", "message": "Publicado en Bluesky ✅"}
    except Exception as e:
        result["bluesky"] = {"status": "error", "message": str(e)}

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
