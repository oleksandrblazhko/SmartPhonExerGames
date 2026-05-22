import matplotlib.pyplot as plt
import pandas as pd

# Дані, отримані в результаті аналізу 48 ігор
data = {
    "Mechanic": [
        "Move", "Avoid", "Random", "Achieve", "Destroy", 
        "Manage", "Shoot", "Select", "Create", "Write"
    ],
    "Count": [47, 30, 26, 25, 20, 7, 3, 1, 0, 0]
}

df = pd.DataFrame(data)
df = df.sort_values(by="Count", ascending=False)

# Створення гістограми
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

bars = ax.bar(df["Mechanic"], df["Count"], color='skyblue')

# Додавання назв та міток
ax.set_title('Частота ігрових механік (Gameplay Bricks 2.5) у 48 Exergame-іграх', fontsize=16)
ax.set_xlabel('Ігрова механіка', fontsize=12)
ax.set_ylabel('Кількість ігор', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Додавання значень над стовпцями
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center', fontsize=11)

plt.tight_layout()

# Збереження графіку у файл
output_path = 'Docs/Results/mechanic_frequency_2.5.png'
plt.savefig(output_path)

print(f"Графік успішно збережено у файлі: {output_path}")
