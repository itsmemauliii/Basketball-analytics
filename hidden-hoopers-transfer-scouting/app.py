import streamlit as st
import pandas as pd
import os

st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")

# Check files in current directory
st.write("Files in current directory:", os.listdir('.'))

# Load data
try:
    df = pd.read_csv("trank.csv")
except FileNotFoundError:
    st.error("trank.csv not found. Make sure the file is in the root directory.")
    st.stop()

# Clean data: Convert percent fields and filter
df['Ret Mins'] = df['Ret Mins'].str.replace('%', '').astype(float)
df['RPMs'] = df['RPMs'].str.replace('%', '').astype(float)

undervalued = df[
    (df['Trans.'] >= 5) &
    (df['Ret Mins'] < 40) &
    ((df['AdjOE'].rank(ascending=False) <= 50) | (df['AdjDE'].rank() <= 50))
].copy()

undervalued['Scouting Report'] = undervalued.apply(
    lambda row: f"{row['Team']} added {int(row['Trans.'])} new transfers with only {row['Ret Mins']}% minutes returning. They’re projected with {row['AdjOE']} AdjOE and {row['AdjDE']} AdjDE — a sleeper team to watch.",
    axis=1
)

selected_team = st.selectbox("Select a team to scout", undervalued['Team'])

team_data = undervalued[undervalued['Team'] == selected_team].iloc[0]
st.write(f"### {selected_team}")
st.write(f"Transfers: {int(team_data['Trans.'])}")
st.write(f"Returning Minutes: {team_data['Ret Mins']}%")
st.write(f"AdjOE: {team_data['AdjOE']}")
st.write(f"AdjDE: {team_data['AdjDE']}")
st.success(team_data['Scouting Report'])
