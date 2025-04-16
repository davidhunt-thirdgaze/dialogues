from flask import Flask, request, render_template, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Store conversation history and character state
conversation = []
max_messages = 20
current_speaker = "Moira"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/discuss', methods=['GET'])
def discuss():
    global current_speaker

    # Format history for GPT
    messages = [{"role": "system", "content": "You are simulating a conversation between Moira and Lee. Be vivid and insightful."}]
    for line in conversation:
        messages.append({"role": "user", "content": line})

    # Alternate speakers
    prompt = f"{current_speaker}:"
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        reply = response['choices'][0]['message']['content'].strip()

        # Update conversation history
        conversation.append(reply)
        if len(conversation) > max_messages:
            conversation.pop(0)

        # Alternate speaker
        current_speaker = "Lee" if current_speaker == "Moira" else "Moira"

        return jsonify({'message': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conversation', methods=['GET'])
def get_conversation():
    return jsonify({'conversation': conversation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
