import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hidden Hoopers - Transfer Scouting", layout="centered")
st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")
st.markdown("Upload a T-Rank CSV file to scout **undervalued transfer-heavy teams** ready to break out.")

# Upload section
uploaded_file = st.file_uploader("📂 Upload your T-Rank CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Preprocessing
        df['Ret Mins'] = df['Ret Mins'].str.replace('%', '', regex=False).astype(float)
        df['RPMs'] = df['RPMs'].str.replace('%', '', regex=False).astype(float)

        # Find undervalued
        undervalued = df[
            (df['Trans.'] >= 5) &
            (df['Ret Mins'] < 40) &
            ((df['AdjOE'].rank(ascending=False) <= 50) | (df['AdjDE'].rank() <= 50))
        ].copy()

        undervalued['Scouting Report'] = undervalued.apply(
            lambda row: f"🔥 **{row['Team']}** has {int(row['Trans.'])} transfers, only {row['Ret Mins']}% minutes returning, but strong AdjOE: {row['AdjOE']} and AdjDE: {row['AdjDE']}. A true hidden gem.",
            axis=1
        )

        if undervalued.empty:
            st.warning("No undervalued teams found based on the criteria.")
        else:
            team = st.selectbox("🔍 Select a team to scout:", undervalued['Team'].sort_values().unique())
            team_data = undervalued[undervalued['Team'] == team].iloc[0]

            st.markdown(f"""
            ### 🏷️ Team: {team}
            - 🔄 Transfers: `{int(team_data['Trans.'])}`
            - 🔁 Returning Minutes: `{team_data['Ret Mins']}%`
            - ⚔️ AdjOE: `{team_data['AdjOE']}`
            - 🛡️ AdjDE: `{team_data['AdjDE']}`

            📋 **Scouting Summary**  
            {team_data['Scouting Report']}
            """)

    except Exception as e:
        st.error(f"⚠️ Error loading file: {e}")
else:
    st.info("Please upload a `T-Rank.csv` file to begin analysis.")

# Footer
st.markdown("---")
st.caption("Built by Mauli Patel • Data from Bart Torvik (T-Rank) • Illinois Basketball Analytics Assignment")

