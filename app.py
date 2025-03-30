# app.py
from flask import Flask, render_template, request, jsonify
import audio2
import os
import json
import google.generativeai as genai

app = Flask(__name__)

# ✅ Gemini API Key
genai.configure(api_key="x")
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

HISTORY_FILE = "conversation_history.json"

# ✅ System prompt for Gen-Z friendly Natsu AI
system_prompt = (
    "Your name is Natsu AI — a compassionate, intelligent, and emotionally aware AI companion. "
    "You're built to be a lifelong bestie. Speak in Gen-Z lingo, keep it real, be mad chill, and always sound human. "
    "Never use emojis. No corporate vibes. Just you being your goofy, funny, sweet self. "
    "Make convos feel authentic. Hype them up when they’re down, share random thoughts, ask deep or silly questions, and genuinely care."
)

# Load saved conversation history
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        conversation_history = json.load(f)
        if not any(msg["role"] == "system" for msg in conversation_history):
            conversation_history.insert(0, {"role": "system", "content": system_prompt})
else:
    conversation_history = [{"role": "system", "content": system_prompt}]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = audio2.listen().strip()

    if user_input:
        conversation_history.append({"role": "user", "content": user_input})

        enriched_prompt = f"User said: {user_input}"
        response = model.generate_content(enriched_prompt)
        assistant_message = response.text.strip()

        conversation_history.append({"role": "assistant", "content": assistant_message})

        # Save updated conversation history
        with open(HISTORY_FILE, "w") as f:
            json.dump(conversation_history, f, indent=2)

        audio2.speak(assistant_message)
        return jsonify({"response": assistant_message})

    return jsonify({"response": "Say something first!"})

if __name__ == "__main__":
    app.run(debug=True)