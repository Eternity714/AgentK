from langchain_core.tools import tool
import pandas as pd

@tool
def data_preprocessor(data: pd.DataFrame, options: dict) -> pd.DataFrame:
    """
    Preprocesses a DataFrame based on specified options.
    Supports handling missing values (fill or drop) and type conversions.
    Options dict can include:
    - missing_value_strategy: 'fill' or 'drop' (default: 'drop')
    - fill_value: value to use when filling missing values (default: 0 for numeric, '' for string)
    - type_conversions: dict of {column_name: target_type} (e.g., {'age': int})
    """
    processed_data = data.copy()
    
    # Handle missing values
    missing_strategy = options.get('missing_value_strategy', 'drop')
    if missing_strategy == 'fill':
        fill_val = options.get('fill_value')
        if fill_val is None:
            # Auto-determine fill value based on column type
            fill_val = {}
            for col in processed_data.columns:
                if pd.api.types.is_numeric_dtype(processed_data[col]):
                    fill_val[col] = 0
                else:
                    fill_val[col] = ''
        processed_data = processed_data.fillna(fill_val)
    elif missing_strategy == 'drop':
        processed_data = processed_data.dropna()
    
    # Handle type conversions
    type_conversions = options.get('type_conversions', {})
    for col, dtype in type_conversions.items():
        if col in processed_data.columns:
            processed_data[col] = processed_data[col].astype(dtype)
    
    return processed_data