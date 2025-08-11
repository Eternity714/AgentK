from langchain_core.tools import tool
import pandas as pd

@tool
def data_analyzer(data: pd.DataFrame, analysis_specs: list) -> dict:
    """Performs specified statistical analyses on a DataFrame. Each analysis spec includes a column (or columns for correlation) and an analysis type (mean/median/correlation)."""
    results = {}
    for spec in analysis_specs:
        column = spec['column']
        analysis_type = spec['type']
        if analysis_type == 'mean':
            result_key = f"{column}_mean"
            results[result_key] = data[column].mean()
        elif analysis_type == 'median':
            result_key = f"{column}_median"
            results[result_key] = data[column].median()
        elif analysis_type == 'correlation':
            if not isinstance(column, list) or len(column) != 2:
                raise ValueError("Correlation analysis requires exactly two columns specified as a list.")
            col1, col2 = column
            result_key = f"{col1}_vs_{col2}_correlation"
            results[result_key] = data[col1].corr(data[col2])
        else:
            raise ValueError(f"Unsupported analysis type: {analysis_type}")
    return results