from langchain_core.tools import tool
import pandas as pd
from typing import List, Optional, Dict

@tool
def pandas_compute_statistics(dataframe_dict: Dict, stat_types: List[str], columns: Optional[List[str]] = None) -> Dict:
    """Computes specified statistics for columns in a serialized Pandas DataFrame.

    Args:
        dataframe_dict: Serialized Pandas DataFrame (e.g., output of df.to_dict()).
        stat_types: List of statistics to compute (e.g., ['mean', 'median', 'std', 'count']).
        columns: Optional list of columns to analyze. Defaults to all numeric columns.

    Returns:
        Dictionary of {column: {stat: value}} with computed statistics for each target column.
    """
    # Convert serialized dict back to DataFrame
    df = pd.DataFrame.from_dict(dataframe_dict)

    # Determine target columns (numeric if not specified)
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    target_columns = columns if columns is not None else numeric_columns
    # Filter to only numeric columns
    target_columns = [col for col in target_columns if col in numeric_columns]

    if not target_columns:
        return {}

    # Compute statistics for each column and stat type
    results = {}
    for col in target_columns:
        col_stats = {}
        for stat in stat_types:
            try:
                # Get the statistic value if the method exists
                stat_value = getattr(df[col], stat)()
                col_stats[stat] = stat_value
            except AttributeError:
                # Handle invalid stat types by setting to None
                col_stats[stat] = None
        results[col] = col_stats

    return results