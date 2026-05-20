import re
import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict


# ============================================
# Константи
# ============================================

ALL_MECHANICS = [
    "Move",
    "Avoid",
    "Destroy",
    "Achieve",
    "Shoot",
    "Manage",
    "Create",
    "Select",
    "Random",
    "Write"
]


# ============================================
# Data Classes
# ============================================

@dataclass
class Mechanic:
    name: str
    explanation: str


@dataclass
class GameRow:
    system: str
    game: str
    included_mechanics: List[Mechanic]
    excluded_or_uncertain: List[Mechanic]


# ============================================
# Допоміжні функції
# ============================================

def clean_text(text: str) -> str:
    """
    Очищення markdown-тексту.
    """

    if not text:
        return ""

    text = text.replace("<br>", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_mechanic_name(name: str) -> str:
    """
    Нормалізація назви механіки.
    """

    if not name:
        return ""

    name = name.strip()

    # прибираємо markdown formatting
    name = re.sub(r"^[`*]+", "", name)
    name = re.sub(r"[`*]+$", "", name)

    # нормалізація пробілів
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def split_mechanics(mechanics_str: str) -> List[str]:
    """
    Перетворення рядка механік у список.
    """

    if not mechanics_str:
        return []

    return [
        normalize_mechanic_name(m)
        for m in mechanics_str.split(",")
        if m.strip()
    ]


def parse_explanations(
    text: str,
    mechanics: List[str]
) -> Dict[str, str]:
    """
    Парсинг пояснень механік.

    Працює з форматами:
    - Move: text
    - **Move**: text
    - Move confirmed ...
    - Move підтверджено ...
    """

    if not text:
        return {}

    text = clean_text(text)

    result = {}

    # сортуємо за довжиною
    # щоб уникнути часткових збігів
    mechanics = sorted(
        mechanics,
        key=len,
        reverse=True
    )

    escaped = [
        re.escape(m)
        for m in mechanics
    ]

    mechanics_pattern = "|".join(escaped)

    pattern = re.compile(
        rf'\b({mechanics_pattern})\b(.*?)(?=\b({mechanics_pattern})\b|$)',
        re.DOTALL | re.IGNORECASE
    )

    matches = pattern.findall(text)

    for mechanic, explanation, _ in matches:

        mechanic = normalize_mechanic_name(mechanic)

        explanation = clean_text(explanation)

        # прибираємо зайві розділювачі
        explanation = re.sub(
            r"^[:\-–—\s]+",
            "",
            explanation
        )

        result[mechanic] = explanation

    return result


def is_separator_line(line: str) -> bool:
    """
    Перевірка markdown separator line.
    """

    return bool(
        re.match(r'^\|[\s:\-\|]+\|$', line)
    )


def split_markdown_row(line: str) -> List[str]:
    """
    Безпечний split markdown row.
    """

    columns = re.split(
        r'(?<!\\)\|',
        line.strip("|")
    )

    return [c.strip() for c in columns]


# ============================================
# Парсер markdown-таблиці
# ============================================

def parse_markdown_table(md_text: str) -> List[GameRow]:

    lines = md_text.splitlines()

    rows = []

    for line in lines:

        line = line.strip()

        # тільки рядки таблиці
        if not line.startswith("|"):
            continue

        # separator line
        if is_separator_line(line):
            continue

        columns = split_markdown_row(line)

        # очікуємо 5 колонок
        if len(columns) != 5:
            continue

        # header row
        if columns[0] == "Назва системи":
            continue

        system_name = clean_text(columns[0])
        game_name = clean_text(columns[1])

        mechanics = split_mechanics(
            clean_text(columns[2])
        )

        # included explanations
        included_explanations = parse_explanations(
            columns[3],
            mechanics
        )

        # excluded explanations
        excluded_explanations = parse_explanations(
            columns[4],
            ALL_MECHANICS
        )

        # ====================================
        # included mechanics
        # ====================================

        included_mechanics = []

        used_mechanics = set()

        for mechanic in mechanics:

            included_mechanics.append(
                Mechanic(
                    name=mechanic,
                    explanation=included_explanations.get(
                        mechanic,
                        ""
                    )
                )
            )

            used_mechanics.add(mechanic)

        # додаємо механіки,
        # які є у поясненнях,
        # але відсутні у mechanics
        for mechanic, explanation in included_explanations.items():

            if mechanic not in used_mechanics:

                included_mechanics.append(
                    Mechanic(
                        name=mechanic,
                        explanation=explanation
                    )
                )

        # ====================================
        # excluded mechanics
        # ====================================

        excluded_mechanics = []

        for mechanic, explanation in excluded_explanations.items():

            excluded_mechanics.append(
                Mechanic(
                    name=mechanic,
                    explanation=explanation
                )
            )

        row = GameRow(
            system=system_name,
            game=game_name,
            included_mechanics=included_mechanics,
            excluded_or_uncertain=excluded_mechanics
        )

        rows.append(row)

    return rows


# ============================================
# Збереження JSON
# ============================================

def save_json(data: List[GameRow], output_path: Path):
    """
    Збереження JSON.
    """

    serializable_data = [
        asdict(row)
        for row in data
    ]

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(
            serializable_data,
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

    try:

        # читання markdown
        md_text = input_file.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        print("Помилка читання UTF-8")

        return

    except Exception as e:

        print(f"Помилка читання файлу: {e}")

        return

    # парсинг
    parsed_data = parse_markdown_table(md_text)

    try:

        # збереження
        save_json(parsed_data, output_file)

    except Exception as e:

        print(f"Помилка запису JSON: {e}")

        return

    print("JSON успішно створено:")
    print(output_file)

    print(
        f"Кількість записів: "
        f"{len(parsed_data)}"
    )


if __name__ == "__main__":
    main()