import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# Load CSV file
df = pd.read_csv("/Users/liujingyi/Desktop/kanazawa_jobs.csv")

# Remove whitespace from column names
df.columns = [col.strip() for col in df.columns]

# Function to extract salary from cicon1 column
def extract_salary(value):
    if pd.isna(value):
        return None
    match = re.search(r"\d+(?:,\d+)?", str(value))
    if match:
        return int(match.group().replace(",", ""))
    return None

# Apply salary extraction to create new column
df["cicon1_cleaned"] = df["cicon1"].apply(extract_salary)

# Remove abnormal salary values (e.g., > 3000 yen/hour)
df_filtered = df[df["cicon1_cleaned"] < 3000]

# Get top 10 jobs by salary
top10 = df_filtered.sort_values(by="cicon1_cleaned", ascending=False).head(10)

# Create bar chart of top 10 salaries
fig_rank = go.Figure(
    data=[
        go.Bar(
            x=top10["会社"],  # Company name
            y=top10["cicon1_cleaned"],  # Salary
            text=top10["cicon1_cleaned"],
            textposition="auto",
            marker_color="indianred"
        )
    ]
)

# Update layout
fig_rank.update_layout(
    title="給与額による求人ランキング（上位10件）",
    xaxis_title="会社名",
    yaxis_title="給与額（円）",
    font=dict(size=14),
    height=500,
    width=1000
)

# Show the plot
fig_rank.show()
