"""
splitter.py — Row splitter stage.
 
Stub implementation — full logic implemented in T4-3.
 
Responsibilities (when complete):
- Split validated DataFrame into clean and rejected sets
- Clean rows: _is_valid == True, internal columns removed
- Rejected rows: _is_valid == False, rejection_reason preserved
"""
import pandas as pd
 
 
def split_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split validated DataFrame into clean and rejected DataFrames.
 
    Returns:
        (clean_df, rejected_df)
        - clean_df: valid rows, _is_valid and _rejection_reason removed
        - rejected_df: invalid rows, rejection_reason preserved
    """
    internal_cols = ["_is_valid", "_rejection_reason", "_source_sheet"]
 
    clean_mask = df["_is_valid"] == True
    rejected_mask = ~clean_mask
 
    clean_df = df[clean_mask].drop(
        columns=[c for c in internal_cols if c in df.columns],
        errors="ignore",
    ).reset_index(drop=True)
 
    rejected_df = df[rejected_mask].drop(
        columns=["_is_valid", "_source_sheet"],
        errors="ignore",
    ).rename(columns={"_rejection_reason": "rejection_reason"}).reset_index(drop=True)
 
    return clean_df, rejected_df
 