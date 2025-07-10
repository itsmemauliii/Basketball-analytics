import streamlit as st
import pandas as pd
from utils.scouting_logic import filter_undervalued_teams, generate_scouting_report

# Load data
df = pd.read_csv('data/T-Rank.csv')
df
df = filter_undervalued_teams(df)

st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")
selected_team = st.selectbox("Select a team", df['Team'])

team_data = df[df['Team'] == selected_team].iloc[0]
st.write(f"### {selected_team}")
st.write(f"Transfers: {int(team_data['Trans.'])}")
st.write(f"Returning Minutes: {team_data['Ret Mins']}%")
st.write(f"AdjOE: {team_data['AdjOE']}")
st.write(f"AdjDE: {team_data['AdjDE']}")
st.success(team_data['Scouting Report'])
