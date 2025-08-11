from langchain_core.tools import tool
import pandas as pd
import os
import numpy as np

@tool
def pandas_create_dataframe(file_path: str = None, data_dict: dict = None) -> dict:
    """Creates a Pandas DataFrame from a supported file or data dictionary, then serializes it to a dict.
    
    Args:
        file_path: Path to a CSV (.csv), Excel (.xlsx/.xls), or JSON (.json) file.
        data_dict: Python dictionary with column names as keys and lists/Series/arrays as values.
    
    Returns:
        Serialized DataFrame as a dictionary (orient='columns').
    
    Raises:
        ValueError: If neither/both inputs are provided, or unsupported file extension.
        FileNotFoundError: If the file path does not exist.
        TypeError: If data_dict values are not list-like.
        pd.errors.ParserError: If the file cannot be parsed into a DataFrame.
    """
    # Validate input exclusivity
    if (file_path is None and data_dict is None) or (file_path is not None and data_dict is not None):
        raise ValueError("Provide exactly one of 'file_path' (for files) or 'data_dict' (for in-memory data).")
    
    # Handle file-based DataFrame creation
    if file_path:
        # Check file existence
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")
        
        # Map file extensions to Pandas readers
        ext = os.path.splitext(file_path)[1].lower()
        reader_map = {
            ".csv": pd.read_csv,
            ".xlsx": pd.read_excel,
            ".xls": pd.read_excel,
            ".json": pd.read_json
        }
        
        if ext not in reader_map:
            raise ValueError(f"Unsupported file type: {ext}. Use CSV (.csv), Excel (.xlsx/.xls), or JSON (.json).")
        
        # Read file and create DataFrame
        try:
            df = reader_map[ext](file_path)
        except pd.errors.ParserError as e:
            raise pd.errors.ParserError(f"Failed to parse file: {str(e)}")
    
    # Handle dictionary-based DataFrame creation
    else:
        # Validate all values are list-like
        for col_name, values in data_dict.items():
            if not isinstance(values, (list, pd.Series, np.ndarray)):
                raise TypeError(f"Values for column '{col_name}' must be list-like (list, Series, or array). Got {type(values).__name__}.")
        
        # Create DataFrame from dictionary
        df = pd.DataFrame(data_dict)
    
    # Serialize DataFrame to dictionary (orient='columns' is default)
    return df.to_dict()
