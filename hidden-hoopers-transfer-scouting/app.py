import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Hidden Hoopers - Transfer Scouting", layout="centered")
st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")
st.markdown("Use data from T-Rank to find **undervalued transfer-heavy teams** that could break out this season.")

# Debug file presence
if "trank.csv" not in os.listdir('.'):
    st.error("❌ 'trank.csv' not found in the root directory. Upload or place it alongside app.py.")
    st.stop()

# Load data
df = pd.read_csv("trank.csv")

# Clean and preprocess
df['Ret Mins'] = df['Ret Mins'].str.replace('%', '', regex=False).astype(float)
df['RPMs'] = df['RPMs'].str.replace('%', '', regex=False).astype(float)

# Filter for undervalued teams:
undervalued = df[
    (df['Trans.'] >= 5) &
    (df['Ret Mins'] < 40) &
    ((df['AdjOE'].rank(ascending=False) <= 50) | (df['AdjDE'].rank() <= 50))
].copy()

# Generate scouting notes
undervalued['Scouting Report'] = undervalued.apply(
    lambda row: f"🔥 **{row['Team']}** has {int(row['Trans.'])} transfers, just {row['Ret Mins']}% of minutes returning, but projected AdjOE: {row['AdjOE']} and AdjDE: {row['AdjDE']}. This team might shock everyone.",
    axis=1
)

# UI Dropdown
team = st.selectbox("🔍 Select a team to scout:", undervalued['Team'].sort_values().unique())

# Display details
team_data = undervalued[undervalued['Team'] == team].iloc[0]
st.markdown(f"""
### 🏷️ Team: {team}
- 🔄 Transfers: `{int(team_data['Trans.'])}`
- 🔁 Returning Minutes: `{team_data['Ret Mins']}%`
- ⚔️ Adjusted Offense (AdjOE): `{team_data['AdjOE']}`
- 🛡️ Adjusted Defense (AdjDE): `{team_data['AdjDE']}`

📋 **Scouting Summary**  
{team_data['Scouting Report']}
""")

# Footer
st.markdown("---")
st.caption("Built by Mauli Patel • Data from T-Rank (Bart Torvik) • Illinois Basketball Analytics Assignment")
