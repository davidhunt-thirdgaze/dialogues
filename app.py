from flask import Flask, render_template, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Set up OpenAI client using project-based key + project ID
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID")
)

# System prompt defines Moira and Lee's recursive philosophical structure
dialogue_history = [
    {
        "role": "system",
        "content": (
            "Moira and Lee discuss philosophical recursion, silence, instability, and structure. "
            "Replies alternate between Moira and Lee. Each reply is concise (1–3 sentences)."
        )
    }
]

current_speaker = "Moira"

def get_next_line():
    global dialogue_history, current_speaker

    prompt = dialogue_history + [{"role": "user", "content": f"{current_speaker}:"}]
    print("🔍 Prompt about to be sent:", prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=prompt,
            temperature=0.8,
            max_tokens=60
        )
        reply_text = response.choices[0].message.content.strip()

        dialogue_history.append({
            "role": "assistant",
            "content": f"{current_speaker}: {reply_text}"
        })

        current_speaker_switch()
        return reply_text

    except Exception as e:
        import traceback
        print("❌ OpenAI API Error:", e)
        traceback.print_exc()
        return f"ERROR: {str(e)}"

def current_speaker_switch():
    global current_speaker
    current_speaker = "Lee" if current_speaker == "Moira" else "Moira"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dialogue')
def dialogue():
    line = get_next_line()
    return jsonify({"speaker": current_speaker, "line": line})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
