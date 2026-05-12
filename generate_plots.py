import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_and_visualize_mechanics():
    """
    This script reads the structured game mechanics dataset, calculates the frequency
    of each mechanic, and generates a bar plot to visualize the results using only
    pandas and matplotlib.
    """
    # Define file paths
    # The script assumes it's run from the root of the project directory.
    csv_path = os.path.join('Docs', 'Results', 'Game_Mechanics_ML_Dataset.csv')
    output_dir = os.path.join('Docs', 'Results')
    output_filename = os.path.join(output_dir, 'mechanic_frequency.png')

    # Check if the source file exists
    if not os.path.exists(csv_path):
        print(f"Error: The source file was not found at {csv_path}")
        print("Please ensure the file from the previous analysis step exists.")
        return

    # Load the dataset
    df = pd.read_csv(csv_path)

    # Drop non-mechanic columns for analysis
    mechanics_df = df.drop(columns=['System', 'Game'])

    # Calculate the frequency of each mechanic
    mechanic_counts = mechanics_df.sum().sort_values(ascending=False)

    # --- Generate and Save the Bar Plot ---
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Use a simple grid style
    ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.75)
    ax.set_axisbelow(True)

    # Create the bar plot using matplotlib
    bars = ax.bar(mechanic_counts.index, mechanic_counts.values, color='skyblue')

    # Add titles and labels
    ax.set_title('Frequency of Gameplay Mechanics in Analyzed ExerGames', fontsize=16, pad=20)
    ax.set_xlabel('Gameplay Brick (Mechanic)', fontsize=12, labelpad=15)
    ax.set_ylabel('Number of Games', fontsize=12, labelpad=15)
    
    # Add count labels on top of each bar
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center', va='bottom')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the plot
    plt.savefig(output_filename)

    print(f"Successfully generated and saved the visualization to: {output_filename}")

if __name__ == '__main__':
    analyze_and_visualize_mechanics()
