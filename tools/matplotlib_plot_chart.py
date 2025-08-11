from langchain_core.tools import tool
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional

@tool
def matplotlib_plot_chart(
    dataframe_dict: dict,
    x_col: str,
    chart_type: str,
    output_path: str,
    y_col: Optional[str] = None
) -> str:
    """
    Generates a Matplotlib chart from a serialized Pandas DataFrame with validation and error handling.

    Args:
        dataframe_dict: Serialized DataFrame (e.g., df.to_dict())
        x_col: X-axis column name
        chart_type: One of ['bar', 'hist', 'line', 'scatter']
        output_path: Path to save the chart (e.g., 'chart.png')
        y_col: Optional Y-axis column name (required for bar/line/scatter)

    Returns:
        Path where chart was saved

    Raises:
        ValueError: If columns are missing, invalid chart type, or DataFrame conversion fails
    """
    # Convert to DataFrame
    try:
        df = pd.DataFrame.from_dict(dataframe_dict)
    except Exception as e:
        raise ValueError(f"Failed to create DataFrame: {str(e)}")

    # Validate columns
    if x_col not in df.columns:
        raise ValueError(f"X column '{x_col}' not found in DataFrame (columns: {', '.join(df.columns)})")
    if chart_type != 'hist' and (y_col is None or y_col not in df.columns):
        raise ValueError(f"Y column '{y_col}' required for {chart_type} and must exist in DataFrame")

    # Validate chart type
    allowed_types = ['bar', 'hist', 'line', 'scatter']
    if chart_type not in allowed_types:
        raise ValueError(f"Invalid chart type '{chart_type}' (allowed: {', '.join(allowed_types)})")

    # Create plot
    plt.figure(figsize=(10, 6))
    if chart_type == 'bar':
        plt.bar(df[x_col], df[y_col])
    elif chart_type == 'hist':
        plt.hist(df[x_col], bins='auto', edgecolor='white')
    elif chart_type == 'line':
        plt.plot(df[x_col], df[y_col], linewidth=2)
    elif chart_type == 'scatter':
        plt.scatter(df[x_col], df[y_col], s=50, alpha=0.7)

    # Format plot
    plt.xlabel(x_col, fontsize=12)
    if y_col:
        plt.ylabel(y_col, fontsize=12)
        plt.title(f'{chart_type.capitalize()} of {y_col} vs {x_col}', fontsize=14)
    else:
        plt.title(f'{chart_type.capitalize()} of {x_col}', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save and clean up
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path