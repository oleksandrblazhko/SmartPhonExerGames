import re
import os
from collections import defaultdict

def parse_game_data(file_path):
    """
    Parses the markdown table from Game_Classification_Result_gem.md
    to extract game names and their associated mechanics.
    """
    games_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content into lines and find the table part
    lines = content.split('\n')
    table_started = False
    header_line = ""
    data_lines = []

    for line in lines:
        if "| :---" in line:  # This is the separator line for markdown tables
            table_started = True
            continue
        if table_started and line.strip():
            if not header_line:
                # Assuming the line before separator is the header
                header_line = lines[lines.index(line) - 2]
            data_lines.append(line)
        elif table_started and not line.strip():
            # Stop if an empty line is encountered after the table started
            break
    
    if not header_line:
        raise ValueError("Could not find table header in the provided file.")

    headers = [h.strip() for h in header_line.strip('|').split('|')]
    
    game_name_idx = headers.index('Назва гри') if 'Назва гри' in headers else -1
    system_name_idx = headers.index('Назва системи') if 'Назва системи' in headers else -1
    mechanics_idx = headers.index('Ігрові механіки') if 'Ігрові механіки' in headers else -1

    if -1 in [game_name_idx, system_name_idx, mechanics_idx]:
        raise ValueError("Required columns 'Назва гри', 'Назва системи', 'Ігрові механіки' not found in the table header.")

    for line in data_lines:
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) > max(game_name_idx, system_name_idx, mechanics_idx):
            system_name = cells[system_name_idx]
            game_name = cells[game_name_idx]
            mechanics_str = cells[mechanics_idx]
            mechanics = set(m.strip() for m in mechanics_str.split(', '))
            if mechanics: # Only add games with at least one mechanic
                games_data.append({
                    'system': system_name,
                    'game_name': game_name,
                    'mechanics': mechanics
                })
    return games_data

def build_universe(games_data):
    """
    Builds the universe of all unique mechanics from the parsed game data.
    """
    universe = set()
    for game in games_data:
        universe.update(game['mechanics'])
    return universe

def greedy_set_cover(universe, games_data):
    """
    Implements the greedy heuristic for the Set Cover problem.
    Finds a minimal set of games (subsets of mechanics) to cover the universe.
    
    Args:
        universe (set): The set of all unique mechanics.
        games_data (list of dict): List of dictionaries, each representing a game.
                                   Each dict must have 'game_name' and 'mechanics' (a set).

    Returns:
        tuple: (selected_games, coverage_progression, final_coverage_score)
               - selected_games (list of str): Names of the selected games.
               - coverage_progression (list of dict): Details of coverage at each step.
               - final_coverage_score (float): Percentage of universe covered.
    """
    covered_mechanics = set()
    selected_games = []
    coverage_progression = []
    
    remaining_universe = set(universe)

    print("
--- Greedy Set Cover Algorithm ---")
    step = 0
    while remaining_universe:
        step += 1
        best_game = None
        max_new_coverage = -1

        # Find the game that covers the most currently uncovered mechanics
        for game in games_data:
            # Skip games already selected (or those that offer no new coverage)
            if game['game_name'] in selected_games:
                continue
            
            new_covered = game['mechanics'].intersection(remaining_universe)
            if len(new_covered) > max_new_coverage:
                max_new_coverage = len(new_covered)
                best_game = game

        if best_game is None or max_new_coverage == 0:
            print(f"Step {step}: No more games can cover new mechanics. Remaining uncovered: {len(remaining_universe)}")
            break # No more useful games to select

        selected_games.append(best_game['game_name'])
        covered_mechanics.update(best_game['mechanics'])
        remaining_universe = universe - covered_mechanics
        
        current_coverage_percentage = (len(covered_mechanics) / len(universe)) * 100
        
        coverage_progression.append({
            'step': step,
            'selected_game': best_game['game_name'],
            'new_mechanics_covered_count': max_new_coverage,
            'total_mechanics_covered_count': len(covered_mechanics),
            'current_coverage_percentage': current_coverage_percentage,
            'uncovered_mechanics_count': len(remaining_universe)
        })
        print(f"Step {step}: Selected '{best_game['game_name']}'. Covered {max_new_coverage} new mechanics. Total covered: {len(covered_mechanics)}/{len(universe)} ({current_coverage_percentage:.2f}%)")

    final_coverage_score = (len(covered_mechanics) / len(universe)) * 100
    print(f"
Algorithm Finished. Total games selected: {len(selected_games)}")
    print(f"Final coverage: {len(covered_mechanics)}/{len(universe)} ({final_coverage_score:.2f}%)")
    if remaining_universe:
        print(f"Remaining uncovered mechanics: {', '.join(sorted(list(remaining_universe)))}")
    
    return selected_games, coverage_progression, final_coverage_score

def main():
    script_dir = os.path.dirname(__file__)
    # Go up two directories to reach the project root if script is in .tasks/
    project_root = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))
    
    game_classification_file = os.path.join(project_root, 'Docs', 'Results', 'Game_Classification_Result_gem.md')
    output_file = os.path.join(project_root, 'Docs', 'Results', 'Minimal_Combination_Coverage_Result.md')

    print(f"Reading game classification from: {game_classification_file}")
    games_data = parse_game_data(game_classification_file)
    
    if not games_data:
        print("No game data found or parsed successfully. Exiting.")
        return

    universe = build_universe(games_data)
    print(f"Universe of unique mechanics ({len(universe)}): {', '.join(sorted(list(universe)))}")

    selected_games, coverage_progression, final_coverage_score = greedy_set_cover(universe, games_data)

    # --- Generate Output File ---
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Результати алгоритму мінімального покриття комбінацій механік (Greedy Heuristic)

")
        f.write("## Вхідні дані
")
        f.write(f"- Файл класифікації ігор: `{os.path.basename(game_classification_file)}`
")
        f.write(f"- Загальна кількість ігор, проаналізованих: {len(games_data)}
")
        f.write(f"- Універсум унікальних механік ({len(universe)}): `{', '.join(sorted(list(universe)))}`

")

        f.write("## Параметри алгоритму
")
        f.write("- Використаний алгоритм: Greedy Heuristic

")

        f.write("## Прогрес покриття механік
")
        f.write("| Крок | Обрана гра | Нові механіки покрито (кількість) | Всього механік покрито (кількість) | Поточне покриття (%) | Непокрито механік (кількість) |
")
        f.write("| :--- | :--- | :---: | :---: | :---: | :---: |
")
        for entry in coverage_progression:
            f.write(f"| {entry['step']} | {entry['selected_game']} | {entry['new_mechanics_covered_count']} | {entry['total_mechanics_covered_count']} | {entry['current_coverage_percentage']:.2f} | {entry['uncovered_mechanics_count']} |
")
        f.write("
")
        
        f.write("## Підсумкові результати
")
        f.write(f"- **Кількість обраних ігор для покриття:** {len(selected_games)}
")
        f.write(f"- **Обрані ігри:** {', '.join(selected_games)}
")
        f.write(f"- **Фінальний відсоток покриття:** {final_coverage_score:.2f}%
")
        
        if len(universe) > len(covered_mechanics):
            uncovered = universe - covered_mechanics
            f.write(f"- **Непокрито механік:** {', '.join(sorted(list(uncovered)))}
")
        else:
            f.write("- **Всі механіки успішно покрито.**
")

    print(f"
Results written to: {output_file}")

if __name__ == "__main__":
    main()
