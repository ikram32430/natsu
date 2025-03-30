def encode_graph(graph):
    triples = graph.get_triples()
    encoded = [f"{s} --{p}--> {o}" for s, p, o in triples]
    with open("encoded_graph.txt", "w", encoding="utf-8") as f:
        for line in encoded:
            f.write(line + "\n")
    print("🧠 Encoded graph saved to encoded_graph.txt")
