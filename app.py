import streamlit as st
import pandas as pd

# Load cleaned KenPom data
df = pd.read_csv("data/kenpom_2025_.csv")
df
# App layout
st.set_page_config(page_title="KenPom Matchup Analyzer", layout="wide")
st.title("🏀 KenPom Matchup Analyzer")
st.caption("Analyze team matchups using KenPom-style stats for NCAA 2025")

# Sidebar for selections
st.sidebar.header("Team Selection")

team_names = df["Team"].unique().tolist()

# Default to Illinois if available
illinois_index = int(df[df["Team"] == "Illinois"].index[0]) if "Illinois" in df["Team"].values else 0

team_1 = st.sidebar.selectbox("🔷 Select Your Team", team_names, index=illinois_index)
team_2 = st.sidebar.selectbox("🔶 Select Opponent", team_names)

# Get team stats
team1_stats = df[df["Team"] == team_1].squeeze()
team2_stats = df[df["Team"] == team_2].squeeze()

# Display team stats side-by-side
st.subheader(f"{team_1} vs {team_2}")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### 🔷 {team_1}")
    st.dataframe(team1_stats[["Conference", "Net Rating", "Offensive Rating", "Defensive Rating", "Adjusted Tempo", "Luck Factor"]])

with col2:
    st.markdown(f"### 🔶 {team_2}")
    st.dataframe(team2_stats[["Conference", "Net Rating", "Offensive Rating", "Defensive Rating", "Adjusted Tempo", "Luck Factor"]])

# Matchup Insights
st.markdown("---")
st.markdown("## 📊 Matchup Insights")

tempo_diff = team1_stats["Adjusted Tempo"] - team2_stats["Adjusted Tempo"]
off_advantage = team1_stats["Offensive Rating"] - team2_stats["Defensive Rating"]
def_advantage = team1_stats["Defensive Rating"] - team2_stats["Offensive Rating"]

st.info(f"**Tempo Gap:** `{tempo_diff:.2f}` → {'Push the pace!' if tempo_diff > 2 else 'Expect a slower tempo.'}")
st.success(f"**Offensive Advantage:** `{off_advantage:.2f}` → {'You have a scoring edge!' if off_advantage > 3 else 'Opponent has solid defense.'}")
st.warning(f"**Defensive Matchup:** `{def_advantage:.2f}` → {'Defensive test ahead!' if def_advantage < -3 else 'You can limit their offense.'}")
