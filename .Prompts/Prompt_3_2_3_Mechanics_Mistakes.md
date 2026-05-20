# Persona:

Раніше ти вже виконав завдання - .Prompts\Prompt_3_2_2_GamePlay-2.0-Matrix.md
Результат завдання - Docs\ExerGamesExamples\Results\matrix_brci.md
Попередній аналіз резульзату виявив, що є механіки, для яких значення BRCI значно менше 100%.
Наприклад, для механіки Achieve середнє значення BRCI за всіма іграми = 82%
Треба робити детальній аналіз для механіки Achieve.
Для такого аналізу треба окремо зібрати інформацію про ігри, для яких Achieve BRCI < 90%

# Tasks:
1) У файлі matrix_brci.md знайди всі ігри, для яких Achieve BRCI < 90%
2) знайди у каталозі Docs\ExerGamesExamples\Results файли з результатами екпериментів для цих ігор 
3) запиши у результуючий json-файл такі дані, які пов'язано з механікою Achieve:
- система (system), 
- гра (game), 
- номер експерименту (experiment), 
- пояснення входження механіки (encluded_mechanics), 
- пояснення невходження / сумнівності (excluded_or_uncertain)

# Context

Приклад результуючого файлу - .Prompts\Prompt_3_2_3_Mechanics_Mistakes_example.json

# Format
1) результат збережи у файлі .Prompts\Mechanic_Achieve_Mistakes_Result.json
