from langchain_core.tools import tool
import os
import pandas as pd

@tool
def data_loader(file_path: str) -> pd.DataFrame:
    """Loads a CSV or Excel file into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV or Excel file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is not supported (only CSV/Excel allowed).
        pd.errors.ParserError: If there's an error parsing the CSV/Excel file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at path: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == '.csv':
        return pd.read_csv(file_path)
    elif file_ext in ('.xlsx', '.xls'):
        return pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Only CSV (.csv) and Excel (.xlsx/.xls) are allowed.")