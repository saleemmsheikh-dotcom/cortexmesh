def detect_similarity(solutions):
    texts = [s["solution"] for s in solutions]

    return len(set(texts)) == 1
