# pip install numpy==1.26.4
# pip install allennlp allennlp-models

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

# =====================================================
# 🔹 Load SRL model
# =====================================================

url = "https://storage.googleapis.com/allennlp-public-models/" \
      "structured-prediction-srl-bert.2020.12.15.tar.gz"

Predictor.from_path(url, strict=False)


text = """
Two players control characters in a confined arena.
Each character has a set of attacks, defenses, and special moves.
Victory is achieved by reducing the opponent’s health bar to zero.
A round continues until one participant wins the required number of rounds.
"""

# =====================================================
# 🔹 Convert SRL output → triples
# =====================================================
triples = []

sentences = [s.strip() for s in text.split(".") if s.strip()]

for sent in sentences:

    result = predictor.predict(sentence=sent)

    verbs = result.get("verbs", [])

    for v in verbs:

        description = v["description"]

        # =================================================
        # 🔹 Simple parsing of SRL tags
        # =================================================
        tokens = result["words"]

        arg0 = None
        arg1 = None
        verb = v["verb"]

        for word, tag in zip(tokens, description.split()):

            if "ARG0" in tag:
                arg0 = word

            if "ARG1" in tag:
                arg1 = word

        if arg0 and arg1:
            triples.append((arg0, verb, arg1))

# =====================================================
# 🔹 Output
# =====================================================
for t in triples:
    print(t)