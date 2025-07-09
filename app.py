import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("kenpom_2025_.csv")
df

st.title("🏀 NCAA KenPom Matchup Analyzer")

# Select teams
team_1 = st.selectbox("Select Your Team", df["Team"].unique(), index=df[df["Team"] == "Illinois"].index[0])
team_2 = st.selectbox("Select Opponent", df["Team"].unique())

# Fetch stats
t1 = df[df["Team"] == team_1].squeeze()
t2 = df[df["Team"] == team_2].squeeze()

st.subheader(f"{team_1} vs {team_2} – Matchup Breakdown")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {team_1}")
    st.write(t1[["Conference", "Net Rating", "Offensive Rating", "Defensive Rating", "Adjusted Tempo", "Luck Factor"]])

with col2:
    st.markdown(f"### {team_2}")
    st.write(t2[["Conference", "Net Rating", "Offensive Rating", "Defensive Rating", "Adjusted Tempo", "Luck Factor"]])

# Matchup insights
st.markdown("### 📊 Matchup Insights")
tempo_gap = t1["Adjusted Tempo"] - t2["Adjusted Tempo"]
off_gap = t1["Offensive Rating"] - t2["Defensive Rating"]
def_gap = t1["Defensive Rating"] - t2["Offensive Rating"]

st.write(f"**Tempo Gap:** {tempo_gap:.2f} → {'Push the pace' if tempo_gap > 2 else 'Watch for slow-down'}")
st.write(f"**Offensive Advantage:** {off_gap:.2f} → {'Exploit offensive edge' if off_gap > 5 else 'Expect resistance'}")
st.write(f"**Defensive Challenge:** {def_gap:.2f} → {'Strong D-matchup' if def_gap < -5 else 'May struggle defending'}")
