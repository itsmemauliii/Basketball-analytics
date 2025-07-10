import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hidden Hoopers - Transfer Scouting", layout="centered")
st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")

st.markdown("""
Upload your **T-Rank CSV** to scout **undervalued transfer-heavy teams**.

We'll highlight:
- 🔄 Teams with **5+ transfers**
- 📉 Less than **40% returning minutes**
- ⚔️ Top-50 **offensive or defensive** adjusted efficiency (AdjOE or AdjDE)
""")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload your T-Rank CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Load and clean the data
        df = pd.read_csv(uploaded_file, skiprows=1)  # skip metadata row
        df.columns = df.columns.str.strip().str.replace('\xa0', ' ', regex=False)

        # Optional: show column names for debugging
        # st.write("📄 Columns:", df.columns.tolist())

        # Clean 'Ret Mins' and 'RPMs'
        df['Ret Mins'] = df['Ret Mins'].str.replace('%', '', regex=False).astype(float)
        df['RPMs'] = df['RPMs'].str.replace('%', '', regex=False).astype(float)

        # Filter for undervalued breakout teams
        undervalued = df[
            (df['Trans.'] >= 5) &
            (df['Ret Mins'] < 40) &
            ((df['AdjOE'].rank(ascending=False) <= 50) | (df['AdjDE'].rank() <= 50))
        ].copy()

        # Add scouting report
        undervalued['Scouting Report'] = undervalued.apply(
            lambda row: f"🔥 **{row['Team']}** has {int(row['Trans.'])} transfers, only {row['Ret Mins']}% minutes returning, "
                        f"but has AdjOE: {row['AdjOE']} and AdjDE: {row['AdjDE']}. High ceiling alert!",
            axis=1
        )

        # UI Output
        if undervalued.empty:
            st.warning("⚠️ No undervalued teams matched the scouting criteria.")
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
        st.error(f"❌ Error loading or processing file: {e}")
else:
    st.info("📌 Please upload a valid `T-Rank.csv` file to begin analysis.")

# Footer
st.markdown("---")
st.caption("🔍 Built by Mauli Patel • Data Source: Bart Torvik (T-Rank) • For Illinois MBB Internship")
