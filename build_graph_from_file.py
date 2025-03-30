import json
from langchain_community.graphs import NetworkxEntityGraph
from dataclasses import dataclass

HISTORY_FILE = "conversation_history.json"

# Proper triple structure for LangChain
@dataclass
class Triple:
    subject: str
    predicate: str
    object_: str  # ⚠️ Underscore matters

def build_graph_from_history(history):
    graph = NetworkxEntityGraph()
    for i in range(0, len(history) - 1, 2):
        if history[i]["role"] == "user" and history[i+1]["role"] == "assistant":
            user_input = history[i]["content"].strip()
            ai_response = history[i+1]["content"].strip()
            if user_input and ai_response:
                triple = Triple(subject=user_input, predicate="talked_to", object_=ai_response)
                graph.add_triple(triple)
    return graph

def encode_graph(graph):
    triples = graph.get_triples()
    encoded = [f"{s} --{p}--> {o}" for s, p, o in triples]
    
    # Write to file
    with open("encoded_graph.txt", "w", encoding="utf-8") as f:
        for line in encoded:
            f.write(line + "\n")

    # Also print to console
    print("🧠 Encoded Knowledge Graph:")
    for line in encoded:
        print("•", line)

def main():
    print("🧠 Building graph from conversation_history.json...")
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    graph = build_graph_from_history(history)
    encode_graph(graph)

if __name__ == "__main__":
    main()
