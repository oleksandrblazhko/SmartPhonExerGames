import re
import json
import sys
from pathlib import Path

# ============================================
# Допоміжні функції
# ============================================

def clean_text(text: str) -> str:
    """
    Очищення markdown-тексту.
    """

    if text is None:
        return ""

    text = text.strip()

    # прибираємо markdown bold
    text = text.replace("**", "")

    # прибираємо зайві пробіли
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_mechanics(mechanics_str: str):
    """
    Перетворення рядка механік у список.
    """

    if not mechanics_str.strip():
        return []

    return [m.strip() for m in mechanics_str.split(",")]


def parse_explanations(text: str):
    """
    Розбір пояснень виду:

    **Avoid:** текст ...
    **Move:** текст ...

    у структуру:
    {
        "Avoid": "...",
        "Move": "..."
    }
    """

    text = text.replace("\n", " ")

    pattern = r"\*\*(.*?)\:\*\*\s*(.*?)(?=\s*\*\*.*?\:\*\*|$)"

    matches = re.findall(pattern, text)

    result = {}

    for mechanic, explanation in matches:

        mechanic = clean_text(mechanic)
        explanation = clean_text(explanation)

        result[mechanic] = explanation

    return result


# ============================================
# Парсер markdown-таблиці
# ============================================

def parse_markdown_table(md_text: str):

    lines = md_text.splitlines()

    rows = []

    for line in lines:

        line = line.strip()

        # тільки рядки таблиці
        if not line.startswith("|"):
            continue

        # пропускаємо separator
        if re.match(r'^\|\s*:?-+:?\s*\|', line):
            continue

        columns = [c.strip() for c in line.strip("|").split("|")]

        # очікуємо 5 колонок
        if len(columns) != 5:
            continue

        # пропускаємо header
        if columns[0] == "Назва системи":
            continue

        system_name = clean_text(columns[0])
        game_name = clean_text(columns[1])

        mechanics = split_mechanics(clean_text(columns[2]))

        included_explanations = parse_explanations(columns[3])
        excluded_explanations = parse_explanations(columns[4])

        row = {
            "system": system_name,
            "game": game_name,

            "mechanics": mechanics,

            "included_mechanics": [
                {
                    "name": mechanic,
                    "explanation": included_explanations.get(mechanic, "")
                }
                for mechanic in mechanics
            ],

            "excluded_or_uncertain": [
                {
                    "name": mechanic,
                    "explanation": explanation
                }
                for mechanic, explanation
                in excluded_explanations.items()
            ]
        }

        rows.append(row)

    return rows


# ============================================
# Збереження JSON
# ============================================

def save_json(data, output_path):

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# ============================================
# Main
# ============================================

def main():

    # перевірка аргументів
    if len(sys.argv) != 2:

        print("Використання:")
        print("python md_to_json.py <markdown_file.md>")

        return

    input_file = Path(sys.argv[1])

    # перевірка існування
    if not input_file.exists():

        print(f"Файл не знайдено: {input_file}")

        return

    # перевірка розширення
    if input_file.suffix.lower() != ".md":

        print("Потрібно передати .md файл")

        return

    # формування json-імені
    output_file = input_file.with_suffix(".json")

    # читання markdown
    md_text = input_file.read_text(encoding="utf-8")

    # парсинг
    parsed_data = parse_markdown_table(md_text)

    # збереження
    save_json(parsed_data, output_file)

    print(f"JSON успішно створено:")
    print(output_file)

    print(f"Кількість записів: {len(parsed_data)}")


if __name__ == "__main__":
    main()