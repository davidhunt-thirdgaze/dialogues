from flask import Flask, jsonify, render_template
import openai
import os
import json
import threading
import time

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

CONVO_FILE = "conversation.json"
MAX_LINES = 30
INTERVAL = 30  # seconds

# Initialize file if missing
if not os.path.exists(CONVO_FILE):
    with open(CONVO_FILE, "w") as f:
        json.dump([], f)

# Load conversation from file
def load_conversation():
    with open(CONVO_FILE, "r") as f:
        return json.load(f)

# Save conversation to file
def save_conversation(convo):
    with open(CONVO_FILE, "w") as f:
        json.dump(convo[-MAX_LINES:], f)

# Alternate speakers
def next_speaker(convo):
    if not convo:
        return "Moira"
    return "Lee" if convo[-1]["speaker"] == "Moira" else "Moira"

# Generate next line using GPT
def generate_line(convo):
    speaker = next_speaker(convo)
    messages = [{"role": "system", "content": "You are two characters named Moira and Lee having a philosophical dialogue. Keep responses short and reflective."}]
    
    # Add last few lines for context
    for line in convo[-6:]:
        messages.append({"role": "user", "content": f'{line["speaker"]}: {line["text"]}'})
    
    messages.append({"role": "user", "content": f"{speaker}:"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=60,
            temperature=0.7
        )
        text = response['choices'][0]['message']['content'].strip()
        convo.append({"speaker": speaker, "text": text})
        save_conversation(convo)
    except Exception as e:
        print("GPT error:", e)

# Background thread to update conversation every 30 seconds
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

# Start background thread
threading.Thread(target=background_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
