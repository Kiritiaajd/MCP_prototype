import pandas as pd

# Load the TAT score data once when this module is imported
tat_data = pd.read_excel("data/TAT_score.xlsx")

def query_tat_score(filters: dict) -> str:
    """
    Query TAT score data based on filters provided by GPT function call.

    Args:
        filters (dict): A dictionary with keys matching column names and
                        values to filter on. For example:
                        {"Cust_ID": "CTPT-1015", "Zone": "NORTH"}

    Returns:
        str: A summary of the filtered data or a no-results message.
    """

    df = tat_data.copy()

    # Apply filters one by one
    for key, value in filters.items():
        if key in df.columns and value:
            df = df[df[key].astype(str).str.contains(str(value), case=False, na=False)]

    if df.empty:
        return "No matching TAT score records found for the given criteria."

    # For demo: return top 3 records summary as text
    result_rows = df.head(3)
    summaries = []
    for _, row in result_rows.iterrows():
        summaries.append(
            f"Application No: {row['Application_No']}, Customer: {row['Cust_Name']}, "
            f"Status: {row['Application_Status']}, Final Approval Month: {row['Final_Approval_Month']}, "
            f"Overall TAT: {row['Overall_TAT']}"
        )

    return "\n".join(summaries)
