# https://pypi.org/project/triplet-extract/

from triplet_extract import OpenIEExtractor

extractor = OpenIEExtractor(
    enable_clause_split=True,    # Split complex sentences into clauses
    enable_entailment=True,      # Generate entailed shorter forms
    min_confidence=1.0           # Filter low-confidence triplets
)

text = """Two players control characters in a confined arena.
Each character has a set of attacks, defenses, and special moves.
Victory is achieved by reducing the opponent’s health bar to zero.
A round continues until one participant wins the required number of rounds."""

triplets = extractor.extract_triplet_objects(text)

for t in triplets:
    print(f"Subject: {t.subject}")
    print(f"Relation: {t.relation}")
    print(f"Object: {t.object}")
    print(f"Confidence: {t.confidence}")
    