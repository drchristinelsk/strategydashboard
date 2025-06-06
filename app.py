import streamlit as st
import pandas as pd

# Load the CSV file
df = pd.read_csv("quantconnect_backtest_summary.csv")

# Extract the date part from "M1_YYYYMMDD" and convert to datetime
df["Date"] = pd.to_datetime(df["Date"].str.extract(r"M1_(\d{8})")[0], format="%Y%m%d", errors="coerce")

st.title("QuantConnect Backtest Performance Dashboard")

# Sidebar filter
strategies = df["Strategy"].unique()
selected_strategies = st.sidebar.multiselect("Select Strategies", strategies, default=strategies)

# Filter based on selection
filtered_df = df[df["Strategy"].isin(selected_strategies)]

st.subheader("Equity Over Time")
for strategy in selected_strategies:
    strategy_data = filtered_df[filtered_df["Strategy"] == strategy]
    st.line_chart(data=strategy_data.set_index("Date")[["Start Equity", "End Equity"]], height=300)

st.subheader("Key Metrics Over Time")
metrics = ["Sharpe Ratio", "Sortino Ratio", "Drawdown", "Total Net Profit"]
selected_metric = st.selectbox("Select Metric", metrics)

chart_data = filtered_df.pivot(index="Date", columns="Strategy", values=selected_metric)
st.line_chart(chart_data)

st.subheader("Raw Data Table")
st.dataframe(filtered_df.sort_values("Date", ascending=False))
