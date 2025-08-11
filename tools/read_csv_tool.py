from langchain_core.tools import tool
import pandas as pd

@tool
def read_csv_tool(file_path: str) -> pd.DataFrame:
    """Reads a CSV file from the given file path and returns a Pandas DataFrame."""
    return pd.read_csv(file_path)