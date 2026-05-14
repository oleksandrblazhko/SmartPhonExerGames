## Comparison Matrix of Game Mechanic Frequencies
This matrix shows the frequency of each core game mechanic identified in the different analysis result files.
| Mechanic   |   Game_GamePlay_2.0_Result_1.md |   Game_GamePlay_2.0_Result_2.md |   Game_GamePlay_2.0_Result_3.md |   Game_GamePlay_2.0_Result_4.md |   Game_GamePlay_2.0_Result_5.md |   Game_GamePlay_2.0_Result_6.md |   Game_GamePlay_2.0_Result_7.md |   Game_GamePlay_2.0_Result_8.md |   Game_GamePlay_2.0_Result_9.md |   Game_GamePlay_2.0_Result_10.md |   Game_GamePlay_2.0_Result_11.md |
|:-----------|--------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|--------------------------------:|---------------------------------:|---------------------------------:|
| Avoid      |                              20 |                              21 |                              23 |                              24 |                              17 |                              32 |                              22 |                              25 |                              19 |                               24 |                               25 |
| Achieve    |                              29 |                              32 |                              31 |                              30 |                              30 |                              32 |                              30 |                              31 |                              34 |                               32 |                               33 |
| Destroy    |                              16 |                              12 |                              16 |                              15 |                              16 |                              14 |                              17 |                              18 |                              11 |                               19 |                               14 |
| Create     |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                                0 |                                0 |
| Manage     |                               9 |                              11 |                              10 |                               7 |                              12 |                               9 |                               8 |                               8 |                               9 |                                8 |                                7 |
| Move       |                              47 |                              45 |                              46 |                              47 |                              47 |                              44 |                              47 |                              43 |                              45 |                               46 |                               46 |
| Random     |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                                0 |                                0 |
| Select     |                               1 |                               1 |                               1 |                               1 |                               0 |                               1 |                               0 |                               2 |                               0 |                                0 |                                1 |
| Shoot      |                               4 |                               4 |                               4 |                               4 |                               4 |                               4 |                               4 |                               4 |                               4 |                                4 |                                4 |
| Write      |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                               0 |                                0 |                                0 |

---
## Python Script Used

```python
import pandas as pd
import glob
import re
import os
from thefuzz import fuzz

def get_reference_mechanics(file_path):
    """
    Parses the reference markdown file to extract the list of English mechanic names.
    Extracts the English name from patterns like: 1) Механіка “Уникнення” (Avoid)
    """
    mechanics = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'\((\w+)\)', line) # Find text in parentheses
                if match:
                    mechanics.append(match.group(1))
    except FileNotFoundError:
        print(f"Error: Reference file not found at {file_path}")
        return []
    return mechanics

def parse_result_file(file_path):
    """
    Parses a result markdown file and extracts a flat list of all mentioned mechanics
    from the 'Перелік назв механік, які увійшли' column.
    """
    mechanics = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            header_index = -1
            for i, line in enumerate(lines):
                if "Перелік назв механік, які увійшли" in line:
                    header_index = i
                    break
            
            if header_index == -1:
                return []

            mechanics_col_index = 3 
            
            for line in lines[header_index + 2:]:
                if line.startswith('|'):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) > mechanics_col_index:
                        mechanic_str = parts[mechanics_col_index]
                        if mechanic_str:
                            raw_split = re.split(r'[,/]', mechanic_str)
                            mechanics.extend([m.strip() for m in raw_split if m.strip()])

    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return []
    return mechanics


def main():
    """
    Main function to perform the comparison and generate the markdown matrix.
    """
    project_root = r'C:\Users\User\Yoga\SmartPhonExerGames'
    reference_file = os.path.join(project_root, 'Docs', 'ExerGamesExamples', 'GamePlayBricks-2.0.md')
    results_dir = os.path.join(project_root, 'Docs', 'ExerGamesExamples', 'Results')
    result_files_pattern = os.path.join(results_dir, 'Game_GamePlay_2.0_Result_*.md')

    reference_mechanics = get_reference_mechanics(reference_file)
    if not reference_mechanics:
        print(f"Could not find reference mechanics in {reference_file}. Exiting.")
        return

    result_files = glob.glob(result_files_pattern)
    if not result_files:
        print(f"No result files found matching pattern: {result_files_pattern}")
        return

    comparison_data = {}
    
    for file_path in result_files:
        file_name = os.path.basename(file_path)
        mentioned_mechanics = parse_result_file(file_path)
        
        freq_count = {mechanic: 0 for mechanic in reference_mechanics}
        
        for mentioned in mentioned_mechanics:
            if not mentioned: continue
            # Find the best fuzzy match in the reference list
            best_match, score = max(
                [(ref, fuzz.ratio(mentioned, ref)) for ref in reference_mechanics], 
                key=lambda item: item[1]
            )
            
            # Use a threshold to decide if it's a valid match
            if score > 90: # Increased threshold for more accurate matching
                freq_count[best_match] += 1
                
        comparison_data[file_name] = freq_count

    if comparison_data:
        df = pd.DataFrame(comparison_data)
        # Sort columns by file number for logical order
        df = df.reindex(sorted(df.columns, key=lambda x: int(re.search(r'_(\d+)\.md', x).group(1))), axis=1)
        df.index.name = 'Mechanic'
        
        print("## Comparison Matrix of Game Mechanic Frequencies")
        print("This matrix shows the frequency of each core game mechanic identified in the different analysis result files.")
        print(df.to_markdown())
    else:
        print("No comparison data was generated.")

if __name__ == '__main__':
    main()
```
