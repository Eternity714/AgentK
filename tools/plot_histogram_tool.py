import pandas as pd
import matplotlib.pyplot as plt
from langchain_core.tools import tool
import os

@tool
def plot_histogram_tool(data: list, column_name: str) -> str:
    """Plots a histogram for the specified column in the given data and saves it to a file.

    Args:
        data: A list of dictionaries representing the dataset (each dict is a row).
        column_name: The name of the column to plot the histogram for.

    Returns:
        str: The file path where the histogram is saved.
    """
    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Check if column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in data.")

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df[column_name], bins=10, edgecolor='black')
    plt.title(f'Histogram of {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)

    # Save the plot
    file_path = 'histogram.png'
    plt.savefig(file_path)
    plt.close()  # Close the plot to free memory

    return os.path.abspath(file_path)