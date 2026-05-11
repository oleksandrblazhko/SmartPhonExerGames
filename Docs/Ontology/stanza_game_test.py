import stanza
from collections import defaultdict

# --- Download and initialize the Stanza pipeline ---
# stanza.download('en', verbose=False)
nlp = stanza.Pipeline('en', verbose=False)

# --- Text for analysis ---
TEXT = """
Two players control characters in a confined arena.
Each character has a set of attacks, defenses, and special moves.
Victory is achieved by reducing the opponent’s health bar to zero.
A round continues until one participant wins the required number of rounds.
"""

def get_phrase_from_head(sent, head):
    """Builds a phrase from a head word and its direct modifiers."""
    words = []
    
    # Collect all modifiers, including possessives
    modifiers = [w for w in sent.words if w.head == head.id]
    
    # Add possessor phrase first if it exists
    poss_mod = next((m for m in modifiers if m.deprel == 'nmod:poss'), None)
    if poss_mod:
        # Build the possessor's phrase recursively
        words.append(get_phrase_from_head(sent, poss_mod))

    # Add other pre-modifiers (det, amod, nummod, compound)
    pre_modifiers = [m for m in modifiers if m.deprel in ('det', 'amod', 'nummod', 'compound')]
    for m in sorted(pre_modifiers, key=lambda w: w.id):
        words.append(m.text)

    # Add the head word itself
    words.append(head.text)
    
    # Join and clean up space around possessive 's
    return ' '.join(words).replace(" 's", "'s")

def expand_conjunctions(sent, head_word):
    """Finds all words connected to the head_word by a conjunction."""
    items = [head_word] + [w for w in sent.words if w.head == head_word.id and w.deprel == 'conj']
    return items

def extract_general_triples(sent):
    """Extracts semantic triples from a parsed sentence using general rules."""
    triples = []
    root = next((w for w in sent.words if w.deprel == "root"), None)
    if not root:
        return []

    subjects = [w for w in sent.words if "subj" in w.deprel]

    for subj in subjects:
        # --- Subject Attribute/Quantity Modifiers ---
        for w in sent.words:
            if w.head == subj.id:
                if w.deprel == 'amod':
                    triples.append((subj.text, 'attribute', w.text))
                elif w.deprel == 'nummod':
                    triples.append((subj.text, 'quantity', w.text))
        
        # --- Main Relation Extraction ---
        if 'nsubj:pass' in subj.deprel:
            # Passive Voice: e.g., "Victory is achieved by reducing..."
            advcl = next((w for w in sent.words if w.head == root.id and w.deprel == 'advcl'), None)
            if advcl and next((m for m in sent.words if m.head == advcl.id and m.deprel == 'mark' and m.text == 'by'), None):
                agent_obj = next((w for w in sent.words if w.head == advcl.id and w.deprel == 'obj'), None)
                if agent_obj:
                    triples.append((subj.text, 'achieved_by', f'reducing {get_phrase_from_head(sent, agent_obj)}'))
                    triples.append(('reducing', 'target', get_phrase_from_head(sent, agent_obj)))
                    obl = next((w for w in sent.words if w.head == advcl.id and w.deprel == 'obl'), None)
                    if obl:
                        triples.append((get_phrase_from_head(sent, agent_obj), 'value', obl.text))

        else: # Active Voice
            for obj in [w for w in sent.words if w.head == root.id and w.deprel == 'obj']:
                if obj.lemma in ('set', 'kind', 'number'):
                    real_obj_head = next((w for w in sent.words if w.head == obj.id and w.deprel.startswith('nmod')), None)
                    if real_obj_head:
                        for item in expand_conjunctions(sent, real_obj_head):
                            triples.append((subj.text, root.text, get_phrase_from_head(sent, item)))
                else:
                    triples.append((get_phrase_from_head(sent, subj), root.text, get_phrase_from_head(sent, obj)))
    
    # --- Root-level Modifiers (Prepositions, Adverbial Clauses) ---
    for w in sent.words:
        if w.head == root.id:
            if w.deprel == 'obl':
                prep = next((p.text for p in sent.words if p.head == w.id and p.deprel == 'case'), None)
                if prep:
                    triples.append((root.text, prep, w.text))
                    # Check for attributes on the object of the preposition
                    for mod in sent.words:
                        if mod.head == w.id and mod.deprel == 'amod':
                            triples.append((w.text, 'attribute', mod.text))
            
            elif w.deprel == 'advcl':
                marker = next((m for m in sent.words if m.head == w.id and m.deprel == 'mark'), None)
                # Ensure it's not the passive 'by' clause handled earlier
                if marker and not (marker.text == 'by' and 'nsubj:pass' in [s.deprel for s in subjects]):
                    clause_subj = next((cs for cs in sent.words if cs.head == w.id and 'subj' in cs.deprel), None)
                    if clause_subj:
                        triples.append((subjects[0].text, f'{root.text}_{marker.text}', f'{w.lemma}_event'))
                        clause_obj = next((co for co in sent.words if co.head == w.id and co.deprel == 'obj'), None)
                        if clause_obj:
                             triples.append((clause_subj.text, w.text, get_phrase_from_head(sent, clause_obj)))


    return list(dict.fromkeys(triples))

def main():
    """Main function to process the text and print triples."""
    doc = nlp(TEXT)
    
    for i, sent in enumerate(doc.sentences):
        print(f"""
# Sentence {i+1}: 
{sent.text.strip()}""")
        triples = extract_general_triples(sent)
        print("""
# Виявлені триплети:""")
        for t in triples:
            print(t)

if __name__ == "__main__":
    main()
