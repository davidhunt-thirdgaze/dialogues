from flask import Flask, jsonify, render_template
from openai import OpenAI
import os
import json
import threading
import time
 
app = Flask(__name__)

# Print environment variables for debugging (remove after confirmation)
print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("DEBUG: OPENAI_ORG_ID =", os.getenv("OPENAI_ORG_ID"))
print("DEBUG: OPENAI_PROJECT_ID =", os.getenv("OPENAI_PROJECT_ID"))

# Initialize OpenAI client with all required credentials
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID")
)

CONVO_FILE = "conversation.json"
MAX_LINES = 30
INTERVAL = 30  # seconds

# Create file if it doesn't exist
if not os.path.exists(CONVO_FILE):
    with open(CONVO_FILE, "w") as f:
        json.dump([], f)

def load_conversation():
    with open(CONVO_FILE, "r") as f:
        return json.load(f)

def save_conversation(convo):
    with open(CONVO_FILE, "w") as f:
        json.dump(convo[-MAX_LINES:], f)

def next_speaker(convo):
    if not convo:
        return "Moira"
    return "Lee" if convo[-1]["speaker"] == "Moira" else "Moira"

def generate_line(convo):
    speaker = next_speaker(convo)

    messages = [
        {"role": "system", "content": "You are two characters, Moira and Lee, having a philosophical dialogue. Keep responses short, reflective, and in character."}
    ]

    for line in convo[-6:]:
        messages.append({"role": "user", "content": f'{line["speaker"]}: {line["text"]}'})
    messages.append({"role": "user", "content": f"{speaker}:"})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=60,
            temperature=0.7
        )
        text = response.choices[0].message.content.strip()
        convo.append({"speaker": speaker, "text": text})
        save_conversation(convo)
        print(f"{speaker}: {text}")  # Runtime confirmation of response
    except Exception as e:
        print("GPT error:", e)

def background_loop():
    while True:
        convo = load_conversation()
        generate_line(convo)
        time.sleep(INTERVAL)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lines")
def lines():
    convo = load_conversation()
    return jsonify(convo)

threading.Thread(target=background_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
