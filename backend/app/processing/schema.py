"""
schema.py — Final schema enforcement stage.
 
Stub implementation — full logic implemented in T5-6.
 
Responsibilities (when complete):
- Enforce exact output column order
- Drop any internal or extra columns
- Ensure clean_df matches warehouse schema exactly
"""
import pandas as pd
 
OUTPUT_SCHEMA = [
    "First", "Last", "Address1", "City", "State",
    "Zip", "DonationDate", "DonationAmount", "Client",
]
 
 
def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enforce final output schema — correct columns in correct order.
 
    Stub: selects only schema columns that exist in the DataFrame.
    Full implementation in T5-6 will enforce all columns are present.
    """
    present = [col for col in OUTPUT_SCHEMA if col in df.columns]
    return df[present].reset_index(drop=True)
 