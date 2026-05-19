# Docs\ExerGamesExamples\Results\matrix.py

import json
import re
from pathlib import Path
from collections import defaultdict

# ============================================================
# GAMEPLAY BRICKS MECHANICS
# ============================================================

MECHANICS = [
    "Avoid",
    "Achieve",
    "Destroy",
    "Create",
    "Manage",
    "Move",
    "Random",
    "Select",
    "Shoot",
    "Write"
]

# JSON files are expected to be located
# in the same directory as matrix.py
BASE_DIR = Path(__file__).parent


# ============================================================
# HELPERS
# ============================================================

def extract_experiment_number(filename: str):
    """
    Extract experiment number from filename.

    Example:
        Game_GamePlay_2.0_Result_3.json -> 3
    """

    match = re.search(r"_(\d+)\.json$", filename)

    if match:
        return int(match.group(1))

    return None


def load_json_files():
    """
    Load all experiment JSON files.
    """

    files = []

    for path in BASE_DIR.glob("*.json"):

        experiment = extract_experiment_number(path.name)

        if experiment is not None:
            files.append((experiment, path))

    files.sort(key=lambda x: x[0])

    return files


# ============================================================
# BRCI
# ============================================================

def brci(values):
    """
    BRCI — Binary Response Concentration Index

    Українське пояснення:
    BRCI вимірює рівень концентрації
    бінарних результатів (0/1)
    між експериментами.

    Інтерпретація:
    - 100%:
        повна стабільність
        (усі 0 або усі 1)

    - ~50%:
        максимальна варіативність
        (наближений розподіл 50/50)

    Високі значення:
        стабільне визначення механіки.

    Низькі значення:
        нестабільність між експериментами.
    """

    if not values:
        return 0.0

    p = sum(values) / len(values)

    score = 1 - 2 * p * (1 - p)

    return score * 100


def format_brci(score: float) -> str:
    """
    Форматування BRCI:
    - округлення до цілого
    - червоний, якщо < 100
    """

    value = round(score)

    if value < 100:
        return f'<span style="color:red">{value}%</span>'

def format_brci(score: float) -> str:
    """
    Форматування BRCI:
    - 100% → без кольору
    - 90–99% → жовтий
    - < 90% → червоний
    - округлення до цілого
    """

    value = round(score)

    if value < 90:
        return f'<span style="color:red">{value}%</span>'

    if value < 100:
        return f'<span style="color:orange">{value}%</span>'

    return f"{value}%"
    


# ============================================================
# MAIN
# ============================================================

def main():

    json_files = load_json_files()

    if not json_files:
        print("No JSON files found.")
        return

    print(f"Detected experiment files: {len(json_files)}")

    # --------------------------------------------------------
    # DATA STORAGE
    # --------------------------------------------------------

    # (system, game) -> experiment -> mechanics set
    game_data = defaultdict(dict)

    # preserve game order from experiment 1
    ordered_games = []

    # --------------------------------------------------------
    # READ JSON FILES
    # --------------------------------------------------------

    for experiment_number, filepath in json_files:

        print(f"Reading: {filepath.name}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for row in data:

            system = row.get("system", "").strip()
            game = row.get("game", "").strip()

            mechanics = {
               mechanic.get("name", "").strip()
               for mechanic in row.get(
                   "included_mechanics",
                  []
               )
            }

            key = (system, game)

            if experiment_number == 1:
                ordered_games.append(key)

            game_data[key][experiment_number] = mechanics

    print(f"Detected games: {len(ordered_games)}")

    # --------------------------------------------------------
    # BUILD MARKDOWN TABLE
    # --------------------------------------------------------

    lines = []

    header = [
        "system",
        "game",
        "experiment"
    ] + MECHANICS

    separator = ["---"] * len(header)

    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(separator) + " |")

    # ========================================================
    # GLOBAL STORAGE:
    # collect mean BRCI across games
    # ========================================================

    global_scores = {
        mechanic: []
        for mechanic in MECHANICS
    }

    # --------------------------------------------------------
    # PROCESS EACH GAME
    # --------------------------------------------------------

    for system, game in ordered_games:

        experiment_map = game_data[(system, game)]

        # vectors per mechanic
        per_mechanic = {
            mechanic: []
            for mechanic in MECHANICS
        }

        # ----------------------------------------------------
        # EXPERIMENT ROWS
        # ----------------------------------------------------

        for experiment_number in sorted(experiment_map.keys()):

            mechanics = experiment_map[experiment_number]

            row = [
                system,
                game,
                str(experiment_number)
            ]

            for mechanic in MECHANICS:

                value = 1 if mechanic in mechanics else 0

                row.append(str(value))

                per_mechanic[mechanic].append(value)

            lines.append("| " + " | ".join(row) + " |")

        # ----------------------------------------------------
        # GAME BRCI ROW
        # ----------------------------------------------------

        brci_row = [
            system,
            game,
            "BRCI(game_i)"
        ]

        for mechanic in MECHANICS:

            score = brci(per_mechanic[mechanic])

            brci_row.append(f"{score:.2f}%")

            # save game-level BRCI
            global_scores[mechanic].append(score)

        lines.append("| " + " | ".join(brci_row) + " |")

    # --------------------------------------------------------
    # MEAN BRCI ROW
    # --------------------------------------------------------

    mean_row = [
        "ALL",
        "ALL",
        "Mean BRCI"
    ]

    for mechanic in MECHANICS:

        scores = global_scores[mechanic]

        if scores:
            mean_score = sum(scores) / len(scores)
        else:
            mean_score = 0.0

        mean_row.append(f"{mean_score:.2f}%")

    lines.append("| " + " | ".join(mean_row) + " |")

    # --------------------------------------------------------
    # GAME SUMMARY TABLE (FINAL RESULTS PER GAME)
    # --------------------------------------------------------

    lines.append("")
    lines.append("## Game Summary (Final BRCI per Game)")
    lines.append("")

    summary_header = ["system", "game", "BRCI(game_i)"] + MECHANICS
    summary_separator = ["---"] * len(summary_header)

    lines.append("| " + " | ".join(summary_header) + " |")
    lines.append("| " + " | ".join(summary_separator) + " |")

    for system, game in ordered_games:

        experiment_map = game_data[(system, game)]

        per_mechanic = {
            mechanic: []
            for mechanic in MECHANICS
        }

        # rebuild binary vectors across experiments
        for experiment_number in sorted(experiment_map.keys()):

            mechanics = experiment_map[experiment_number]

            for mechanic in MECHANICS:

                value = 1 if mechanic in mechanics else 0
                per_mechanic[mechanic].append(value)

        row = [
            system,
            game,
            "BRCI"
        ]

        for mechanic in MECHANICS:

            score = brci(per_mechanic[mechanic])
            # row.append(f"{score:.2f}%")
            row.append(format_brci(score))

        lines.append("| " + " | ".join(row) + " |")    

    # --------------------------------------------------------
    # SAVE MARKDOWN
    # --------------------------------------------------------

    output_file = BASE_DIR / "matrix_brci.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Matrix saved to: {output_file}")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()