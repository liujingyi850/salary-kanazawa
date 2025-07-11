import pandas as pd
import plotly.express as px
import re

# CSVファイルを読み込み
df = pd.read_csv("kanazawa_jobs.csv")

# 列名の空白を削除
df.columns = [col.strip() for col in df.columns]

# 給与（cicon1列）から数字を抽出
def extract_salary(value):
    if pd.isna(value):
        return None
    match = re.search(r"\d{1,3}(?:,\d{3})*", str(value))  # カンマ付きの数字を対応
    if match:
        return int(match.group().replace(",", ""))
    return None

df["cicon1_cleaned"] = df["cicon1"].apply(extract_salary)

# 異常値（3000円以上）を除外
df_filtered = df[df["cicon1_cleaned"] < 3000]

# 可視化（職種タイプごとの給与分布）
fig = px.strip(
    df_filtered,
    x="タイプ",
    y="cicon1_cleaned",
    color="タイプ",
    stripmode="overlay"
)

fig.update_layout(
    title="職種タイプごとの給与額の分布（cicon1列より抽出）",
    xaxis_title="職種タイプ",
    yaxis_title="給与額（円, 数値）",
    font=dict(family="Arial", size=16),
    title_font_size=22,
    width=1000,
    height=500
)

fig.show()


import streamlit as st

st.plotly_chart(fig)