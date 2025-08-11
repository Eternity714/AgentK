from langchain_core.tools import tool
import pandas as pd

@tool
def statistical_summary_tool(dataframe: pd.DataFrame) -> dict:
    """计算Pandas DataFrame中每个数值列的基本统计摘要（均值、中位数、标准差）。"""
    # 筛选数值型列
    numeric_df = dataframe.select_dtypes(include=['number'])
    stats_result = {}
    for col in numeric_df.columns:
        col_data = numeric_df[col]
        stats_result[col] = {
            "mean": round(col_data.mean(), 4),
            "median": round(col_data.median(), 4),
            "std": round(col_data.std(), 4)
        }
    return stats_result