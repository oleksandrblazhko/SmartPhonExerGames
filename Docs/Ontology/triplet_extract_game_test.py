# https://pypi.org/project/triplet-extract/
# https://github.com/adlumal/triplet-extract

from triplet_extract import OpenIEExtractor

extractor = OpenIEExtractor(
    # deep_search=True,
    enable_clause_split=True,    # Split complex sentences into clauses
    enable_entailment=False,      # Generate entailed shorter forms
    min_confidence=1.0           # Filter low-confidence triplets
)

text = """Two players control characters in a confined arena.
Each character has a set of attacks, defenses, and special moves.
Victory is achieved by reducing the opponent’s health bar to zero.
A round continues until one participant wins the required number of rounds."""

triplets = extractor.extract_triplet_objects(text)

for t in triplets:
    print(f"({t.subject},{t.relation},{t.object})");

    