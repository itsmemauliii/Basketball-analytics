import streamlit as st
import pandas as pd
import os

# --- Helper Functions ---

def generate_scouting_report(row):
    """Generates a scouting report string for a given team row."""
    return (
        f"{row['Team']} added {int(row['Trans.'])} new transfers with only "
        f"{row['Ret Mins']}% minutes returning. They’re projected with "
        f"{row['AdjOE']} AdjOE and {row['AdjDE']} AdjDE — a sleeper team to watch."
    )

def filter_and_process_data(df):
    """
    Filters the DataFrame for undervalued teams and generates scouting reports.
    Assumes 'Ret Mins' and 'RPMs' might still have '%' and need conversion.
    """
    # Ensure 'Ret Mins' and 'RPMs' are clean and numeric
    # Check if any value in the column contains '%' before attempting to replace and convert
    if df['Ret Mins'].astype(str).str.contains('%').any():
        df['Ret Mins'] = df['Ret Mins'].str.replace('%', '').astype(float)
    if df['RPMs'].astype(str).str.contains('%').any():
        df['RPMs'] = df['RPMs'].str.replace('%', '').astype(float)

    # Apply the filtering criteria
    undervalued = df[
        (df['Trans.'] >= 5) &
        (df['Ret Mins'] < 40) &
        ((df['AdjOE'].rank(ascending=False) <= 50) | (df['AdjDE'].rank() <= 50))
    ].copy() # .copy() to avoid SettingWithCopyWarning

    # Generate the scouting report for the filtered teams
    undervalued['Scouting Report'] = undervalued.apply(generate_scouting_report, axis=1)
    return undervalued

# --- Streamlit Application ---

st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")

# Load data
try:
    df = pd.read_csv("trank.csv")
except FileNotFoundError:
    st.error("`trank.csv` not found. Make sure the file is in the same directory as this script.")
    st.stop() # Stop the app if the file is not found

# Process the data using the helper function
processed_df = filter_and_process_data(df.copy()) # Pass a copy to avoid modifying original df

# Check if any undervalued teams were found
if processed_df.empty:
    st.warning("No teams found matching the 'undervalued' criteria with the current data.")
else:
    # Select a team from the processed data
    selected_team = st.selectbox("Select a team to scout", processed_df['Team'].unique())

    # Display information for the selected team
    team_data = processed_df[processed_df['Team'] == selected_team].iloc[0]
    st.write(f"### {selected_team}")
    st.write(f"**Transfers:** {int(team_data['Trans.'])}")
    st.write(f"**Returning Minutes:** {team_data['Ret Mins']}%")
    st.write(f"**Adjusted Offensive Efficiency (AdjOE):** {team_data['AdjOE']}")
    st.write(f"**Adjusted Defensive Efficiency (AdjDE):** {team_data['AdjDE']}")
    st.success(f"**Scouting Report:** {team_data['Scouting Report']}")
