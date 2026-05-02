import spacy

# Завантаження NLP моделі
# python -m spacy download en_core_web_md
# nlp = spacy.load("en_core_web_lg")
nlp = spacy.load("en_core_web_sm")

text = """
Two players control characters in a confined arena.
Each character has a set of attacks, defenses, and special moves.
Victory is achieved by reducing the opponent’s health bar to zero.
A round continues until one participant wins the required number of rounds.
"""

doc = nlp(text)


#for chunk in doc.noun_chunks:
#    print(chunk.text)

triples = []

# 🔹 Проста мапа прийменників → семантика
prep_map = {
    "in": "located_in",
    "on": "located_on",
    "at": "located_at",
    "until": "until_event",
    "by": "caused_by",
    "to": "target"
}

# =========================================================
# 🔹 Основний цикл по реченнях
# =========================================================
for sent in doc.sents:

    sent_doc = nlp(sent.text)

    for token in sent_doc:

        # =====================================================
        # 🔹 1. Обробка дієслів (основні події)
        # =====================================================
        if token.pos_ == "VERB":

            subject = None
            obj = None

            # --- SUBJECT ---
            for child in token.children:
                if "subj" in child.dep_:
                    subject = child.lemma_

            # --- OBJECT ---
            for child in token.children:
                if child.dep_ in ("dobj", "obj"):
                    obj = child.lemma_

            if subject and obj:
                triples.append((subject, token.lemma_, obj))

            # =================================================
            # 🔹 2. Прийменникові конструкції
            # =================================================
            for child in token.children:
                if child.dep_ == "prep":

                    prep = child.lemma_

                    for subchild in child.children:
                        if subchild.dep_ == "pobj":

                            relation = prep_map.get(prep, prep)

                            triples.append(
                                (subject, relation, subchild.lemma_)
                            )

            # =================================================
            # 3. Причинні / часові / умовні конструкції
            # advcl — adverbial clause (прислівникова обставина), наприклад, quickly, slowly, very, yesterday
            # npadvmod - noun phrase adverbial modifier (обставина, виражена іменниковою групою, яка діє як прислівник), наприклад, next week, this morning, last year, three hours
            # advmod - adverbial modifier (обставинне підрядне речення), наприклад, because he was tired, if the player wins, until the round ends, when the game starts
            # =================================================
            for child in token.children:
                if child.dep_ in ("advcl", "npadvmod", "advmod"):

                    triples.append(
                        (subject, "has_context", child.lemma_)
                    )

        # =====================================================
        # 🔹 4. Обробка "has / is / are" конструкцій
        # =====================================================
        if token.lemma_ in ("have", "be"):

            subject = None

            for child in token.children:
                if "subj" in child.dep_:
                    subject = child.lemma_

                if child.dep_ in ("dobj", "attr", "acomp"):
                    triples.append((subject, "has", child.lemma_))

# =========================================================
# 🔹 Вивід результату
# =========================================================
for t in triples:
    print(t)