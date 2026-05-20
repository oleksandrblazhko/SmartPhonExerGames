
import json
import os
import re

def parse_md_table(content):
    lines = content.strip().split('
')
    rows = [re.split(r'\s*\|\s*', line.strip()) for line in lines if line.strip().startswith('|')]
    if not rows:
        return []
    
    # Remove the first and last empty elements from each row
    parsed_rows = []
    for row in rows:
        if len(row) > 1:
            parsed_rows.append(row[1:-1])

    if len(parsed_rows) < 2:
        return []

    header = [h.strip() for h in parsed_rows[0]]
    
    # It seems the header is not always consistent, let's rely on column order
    # Let's hardcode the expected column order based on the prompt and file structure
    # | Назва системи | Назва гри | Перелік назв механік, які увійшли | Пояснення входження механіки | Пояснення невходження / сумнівності |
    
    data = []
    for row in parsed_rows[2:]: # Starting from the third line which is the first data row
        if len(row) == 5:
            data.append({
                'system': row[0].strip(),
                'game': row[1].strip(),
                'included_mechanics_list': row[2].strip(),
                'included_explanation': row[3].strip(),
                'excluded_explanation': row[4].strip()
            })
    return data

def find_achieve_explanation(text):
    # Find the explanation for Achieve, which starts with "Achieve:"
    match = re.search(r'Achieve:[^|]*', text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return ""

def main():
    games_to_analyze = {
        "Wii Fit / Soccer Heading",
        "Wii Fit / Penguin Slide",
        "Wii Fit / Snowball Fight",
        "Wii Fit / Hosedown",
        "Wii Fit / Scuba Search",
        "PlankPad / Fruit Slicer",
        "PlankPad / Stix & Stones",
        "PlankPad / Meteor Madness",
        "PlankPad / Candy Monster",
        "PlankPad / Duck Shoot",
        "PlankPad / Snow Cruisin",
        "PlankPad / Wave Rider",
        "BoBo Balance / Crazy Snowboard",
        "BoBo Balance / Color Tunnel",
        "BoBo Balance / Car",
        "BoBo Balance / Candy Rex",
        "BoBo Balance / Ice Adventure",
        "BoBo Balance / Submarine",
        "BoBo Balance / Harvest Rush",
        "BoBo Balance / Tetromino"
    }

    results_dir = os.path.join('Docs', 'ExerGamesExamples', 'Results')
    output_file = os.path.join('.Prompts', 'Mechanic_Achieve_Mistakes_Result.json')
    
    all_results = []

    for i in range(1, 34):
        md_file = os.path.join(results_dir, f'Game_GamePlay_2.0_Result_{i}.md')
        if os.path.exists(md_file):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parsed_data = parse_md_table(content)

            for item in parsed_data:
                full_game_name = f"{item['system']} / {item['game']}"
                if full_game_name in games_to_analyze:
                    
                    encluded_mechanics = ""
                    excluded_or_uncertain = ""

                    if 'Achieve' in item['included_mechanics_list']:
                        encluded_mechanics = find_achieve_explanation(item['included_explanation'])
                    else: # if not in included, must be in excluded/uncertain
                        excluded_or_uncertain = find_achieve_explanation(item['excluded_explanation'])

                    result_item = {
                        "system": item['system'],
                        "game": item['game'],
                        "experiment": i,
                        "encluded_mechanics": encluded_mechanics,
                        "excluded_or_uncertain": excluded_or_uncertain,
                    }
                    all_results.append(result_item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
