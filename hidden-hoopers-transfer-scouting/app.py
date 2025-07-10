import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hidden Hoopers - Transfer Scouting", layout="centered")
st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")

st.markdown("""
Upload the **cleaned T-Rank CSV** to identify **undervalued teams** in the transfer portal.

### Criteria:
- 🔁 **Returning Minutes** < 40%
- 🔄 **5+ Transfers**
- ⚔️ Ranked Top 50 in **AdjOE** or **AdjDE**
""")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload cleaned T-Rank CSV (trank_cleaned.csv)", type=["csv"])

if uploaded_file is not None:
    try:
        # Read and process the CSV
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        # Convert necessary fields to float after removing %
        df["Ret Mins"] = df["Ret Mins"].astype(str).str.replace('%', '', regex=False).astype(float)
        df["RPMs"] = df["RPMs"].astype(str).str.replace('%', '', regex=False).astype(float)

        # Filter undervalued breakout candidates
        filtered_df = df[
            (df["Trans."] >= 5) &
            (df["Ret Mins"] < 40) &
            ((df["AdjOE"].rank(ascending=False) <= 50) | (df["AdjDE"].rank() <= 50))
        ].copy()

        if filtered_df.empty:
            st.warning("No undervalued teams matched the criteria.")
        else:
            team = st.selectbox("🔍 Choose a team to scout:", filtered_df["Team"].sort_values().unique())
            team_data = filtered_df[filtered_df["Team"] == team].iloc[0]

            st.markdown(f"""
            ## 🏷️ **{team_data['Team']}**
            - 🔄 Transfers: `{int(team_data['Trans.'])}`
            - 🔁 Returning Minutes: `{team_data['Ret Mins']}%`
            - ⚔️ AdjOE: `{team_data['AdjOE']}`
            - 🛡️ AdjDE: `{team_data['AdjDE']}`
            - ⏱️ Tempo: `{team_data['Tempo']}`

            📊 **Scouting Summary**  
            `{team_data['Team']}` has strong offensive or defensive metrics despite limited returning minutes. 
            With {team_data['Trans.']} transfers and a new core, this team may be an under-the-radar breakout.
            """)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("📁 Please upload `trank_cleaned.csv` to begin scouting.")
