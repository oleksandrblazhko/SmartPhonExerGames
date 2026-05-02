import stanza

stanza.download('uk')
nlp = stanza.Pipeline('uk')

text = """
Цю асану можна виконувати будь-де, де можна розкласти килимок для фітнес-йоги.
1. Почніть вправу в упорі стоячи на колінах. Руки перед плечами, а коліна під стегнами. Широко розташуйте пальці ніг та зігніть їх на себе. Вдихніть.
2. Видихніть, коли піднімаєте стегна, відриваєте коліна від килима та випрямляєте ноги. Тримайте коліна злегка зігнутими, коли подовжуєте спину. Потягніться п’ятами до килимка. Випряміть коліна, не фіксуючи їх.
3. Розведіть пальці рук. Притисніть пальці до килимка. Притисніть лопатки до спини, потім розведіть їх. Розслабте шию і тримайте голову між плечами.
4. Сильно активуйте квадратний м’яз, щоб зняти тягар ваги тіла з рук.
Ця дія значною мірою допомагає зробити цю позу більш розслаблюючою.
5. Поверніть стегна ніг всередину,
тримайте куприк високо, а п’яти опустіть до килимка.
6. Переконайтеся, що відстань між вашими руками та ногами правильна, опустіться вперед у положення планки.
Відстань між руками та ногами в цих двох позах має бути однаковою. Не наближайте ноги до рук, щоб п’яти торкнулися килимка.
7. Залишайтеся в позі на 10 (спочатку на 3-5) або більше циклів дихання. На видиху зігніть коліна й опустіться у вихідне положення або в "Позу дитини".
"""

doc = nlp(text)


def extract_triples(sent):
    root = None
    subj = None
    obj = None

    triples = []

    for w in sent.words:
        if w.deprel == "root":
            root = w
        elif w.deprel == "nsubj":
            subj = w
        elif w.deprel == "obj":
            obj = w

    if root and subj and obj:
        triples.append((subj.text, root.text, obj.text))

    return triples

def build_tree(sent):
    """
    Будує структуру head → children
    """
    tree = {}

    for w in sent.words:
        tree.setdefault(w.head, []).append(w)

    return tree


def print_ascii_tree(sent):
    tree = build_tree(sent)

    root = next(w for w in sent.words if w.deprel == "root")

    def dfs(node, prefix=""):
        children = tree.get(node.id, [])

        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)

            connector = "└── " if is_last else "├── "

            print(prefix + connector + f"{child.text} ({child.deprel})")

            extension = "    " if is_last else "│   "
            dfs(child, prefix + extension)

    print(f"{root.text} (ROOT)")
    dfs(root)

for i, sent in enumerate(doc.sentences):
    print(f"\nSentence {i+1}: {sent.text}\n")

    print_ascii_tree(sent)

    print("\nTriples:")
    for t in extract_triples(sent):
        print("  ", t)