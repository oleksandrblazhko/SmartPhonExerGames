from triplet_extract import extract

text = "Cats love milk and mice."
triplets = extract(text)

for t in triplets:
    print(f"({t.subject}, {t.relation}, {t.object})")


