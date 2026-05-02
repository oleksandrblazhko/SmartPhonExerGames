import spacy

nlp = spacy.load("en_core_web_sm")

text = """
Two players control characters in a confined arena.
Each character has a set of attacks, defenses, and special moves.
Victory is achieved by reducing the opponent’s health bar to zero.
A round continues until one participant wins the required number of rounds.
"""

doc = nlp(text)

triples = []

prep_map = {
    "in": "located_in",
    "by": "caused_by",
    "to": "target",
    "until": "until_event"
}

REL_MAP = {
    "have": "has",
    "has": "has",
    "achieve": "achieves",
    "continue": "continues",
    "win": "wins",
    "control": "controls",
    "reduce": "reduces"
}

# -------------------------
# SUBJECT
# -------------------------
def get_subject(v):
    for c in v.children:
        if c.dep_ in ("nsubj", "nsubjpass", "csubj"):
            return c
    return None


# -------------------------
# SET EXPANSION (clean list semantics)
# -------------------------
def expand_set(token):

    items = []

    for c in token.children:
        if c.dep_ == "prep" and c.lemma_ == "of":
            for obj in c.children:

                if obj.pos_ in ("NOUN", "PROPN", "ADJ"):
                    items.append(obj)

                items.extend(list(obj.conjuncts))

    return items


# -------------------------
# OBJECT EXTRACTION (semantic-safe)
# -------------------------
def get_objects(v):

    objs = []

    for c in v.children:

        # direct objects
        if c.dep_ in ("dobj", "obj", "attr", "pobj", "dative"):

            if c.lemma_ == "set":
                objs.extend(expand_set(c))
                continue

            objs.append(c)
            objs.extend(list(c.conjuncts))

        # 🔥 CRITICAL FIX: xcomp (reducing, achieving, winning)
        if c.dep_ == "xcomp":
            objs.append(c)

        # 🔥 CRITICAL FIX: pcomp (by reducing X)
        if c.dep_ == "prep":
            for p in c.children:
                if p.dep_ in ("pcomp", "pobj"):
                    objs.append(p)

    # dedup
    seen = set()
    out = []

    for o in objs:
        if o is None:
            continue

        if o.lemma_ in seen:
            continue

        seen.add(o.lemma_)
        out.append(o)

    return out


# -------------------------
# NORMALIZATION (stable NP)
# -------------------------
def norm(t):

    if t.lemma_ in ("set", "require", "confine"):
        return ""

    words = []

    if t.pos_ in ("NOUN", "PROPN", "ADJ"):
        words.append(t.lemma_)

    for c in t.children:
        if c.dep_ in ("compound", "amod"):
            words.insert(0, c.lemma_)

    return "_".join(words)


# -------------------------
# MAIN
# -------------------------
for sent in doc.sents:

    sent_doc = nlp(sent.text)

    for v in sent_doc:

        if v.pos_ != "VERB":
            continue

        subj = get_subject(v)
        if not subj:
            continue

        subj = subj.lemma_
        rel = REL_MAP.get(v.lemma_, v.lemma_)

        # -------------------------
        # OBJECT TRIPLES
        # -------------------------
        for o in get_objects(v):

            o_norm = norm(o)
            if not o_norm:
                continue

            if o.lemma_ == subj:
                continue

            triples.append((subj, rel, o_norm))

        # -------------------------
        # PREPOSITIONS
        # -------------------------
        for c in v.children:
            if c.dep_ == "prep":

                for p in c.children:
                    if p.dep_ == "pobj":

                        p_norm = norm(p)
                        if p_norm:
                            triples.append(
                                (subj,
                                 prep_map.get(c.lemma_, c.lemma_),
                                 p_norm)
                            )

        # -------------------------
        # XCOMP EVENTS (semantic fix)
        # -------------------------
        for c in v.children:
            if c.dep_ == "xcomp":

                obj = norm(c)
                if obj:
                    triples.append((subj, v.lemma_, obj))


# -------------------------
# OUTPUT
# -------------------------
triples = sorted(set(triples))

for t in triples:
    print(t)