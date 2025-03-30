# natsu_ai_rag.py
import os
import json
import google.generativeai as genai
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph
from audio2 import listen, speak
from build_graph_from_file import encode_graph  # ✅ Added import for encoding

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

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
                if not any(msg["role"] == "system" for msg in history):
                    history.insert(0, {"role": "system", "content": system_prompt})
                return history
        except json.JSONDecodeError:
            print("⚠️ JSON file corrupt. Starting fresh.")
    return [{"role": "system", "content": system_prompt}]

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def build_graph(convo):
    graph = NetworkxEntityGraph()
    for i in range(0, len(convo) - 1, 2):
        if convo[i]["role"] == "user" and convo[i+1]["role"] == "assistant":
            user = convo[i]["content"]
            ai = convo[i+1]["content"]
            graph.add_triple(user.strip(), "talked_to", ai.strip())
    return graph

def query_graph(graph, question):
    try:
        rels = graph.get_triples()
        if not rels:
            return ""
        context = "\n".join([f"{s} --{p}--> {o}" for s, p, o in rels])
        prompt = f"""Here's what I already know:\n{context}\n\nNow answer this: {question}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("⚠️ Graph error:", e)
        return ""

def chat_with_natsu(user_input, history):
    history.append({"role": "user", "content": user_input})

    enriched_prompt = f"User said: {user_input}"
    response = model.generate_content(enriched_prompt)
    assistant_message = response.text.strip()

    history.append({"role": "assistant", "content": assistant_message})
    save_history(history)
    return assistant_message

def main():
    history = load_history()
    try:
        while True:
            user_input = listen().strip()
            if user_input.lower() in ["quit", "exit", "stop"]:
                speak("Alright, peace out.")
                break
            reply = chat_with_natsu(user_input, history)
            speak(reply)
    finally:
        print("🧠 Building knowledge graph from chat history...")
        graph = build_graph(history)
        triples = graph.get_triples()
        print("✅ Graph built with", len(triples), "relationships.")
        for s, p, o in triples:
            print(f"- {s} --{p}--> {o}")

        # ✅ Save encoded graph
        encode_graph(graph)

if __name__ == "__main__":
    main()