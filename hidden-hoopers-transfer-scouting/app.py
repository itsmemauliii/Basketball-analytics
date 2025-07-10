import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hidden Hoopers - Transfer Scouting", layout="centered")
st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")
st.markdown(
    """
Upload a **T-Rank CSV file** to scout **undervalued transfer-heavy teams** likely to break out.
We look for teams with:
- 🔄 5+ incoming transfers  
- 📉 Less than 40% minutes returning  
- 📈 Top-50 offense (AdjOE) or defense (AdjDE) projection
"""
)

# Step 1: Upload CSV
uploaded_file = st.file_uploader("📂 Upload your T-Rank CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Step 2: Read the CSV, skip first row if it's a note
        df = pd.read_csv(uploaded_file, skiprows=1)

        # Step 3: Clean percent columns
        df['Ret Mins'] = df['Ret Mins'].str.replace('%', '', regex=False).astype(float)
        df['RPMs'] = df['RPMs'].str.replace('%', '', regex=False).astype(float)

        # Step 4: Filter undervalued teams
        undervalued = df[
            (df['Trans.'] >= 5) &
            (df['Ret Mins'] < 40) &
            ((df['AdjOE'].rank(ascending=False) <= 50) | (df['AdjDE'].rank() <= 50))
        ].copy()

        # Step 5: Create scouting reports
        undervalued['Scouting Report'] = undervalued.apply(
            lambda row: f"🔥 **{row['Team']}** has {int(row['Trans.'])} transfers, just {row['Ret Mins']}% minutes returning, but impressive AdjOE: {row['AdjOE']} and AdjDE: {row['AdjDE']}. Sleeper team alert!",
            axis=1
        )

        if undervalued.empty:
            st.warning("⚠️ No undervalued teams found based on the criteria.")
        else:
            team = st.selectbox("🔍 Select a team to scout:", undervalued['Team'].sort_values().unique())
            team_data = undervalued[undervalued['Team'] == team].iloc[0]

            # Step 6: Show team info
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
        st.error(f"⚠️ Failed to process file: {e}")
else:
    st.info("📌 Please upload a valid `T-Rank.csv` file to get started.")

# Footer
st.markdown("---")
st.caption("🔍 Built by Mauli Patel • Data: Bart Torvik • Illinois MBB Internship Project")
