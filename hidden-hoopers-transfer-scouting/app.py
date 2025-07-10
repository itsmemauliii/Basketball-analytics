import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hidden Hoopers - Transfer Scouting", layout="centered")
st.title("🏀 Hidden Hoopers: Transfer Portal Scouting Tool")

st.markdown("""
Upload the **cleaned T-Rank CSV** to interactively scout teams based on transfer activity, returning minutes, and offensive/defensive potential.
""")

uploaded_file = st.file_uploader("📂 Upload `trank_cleaned.csv`", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        df = df[df["Ret Mins"] != "Ret Mins"]

        # Clean percentage and numeric columns
        df["Ret Mins"] = df["Ret Mins"].astype(str).str.replace('%', '', regex=False).astype(float)
        df["RPMs"] = df["RPMs"].astype(str).str.replace('%', '', regex=False).astype(float)
        df["AdjOE"] = df["AdjOE"].astype(float)
        df["AdjDE"] = df["AdjDE"].astype(float)
        df["Trans."] = pd.to_numeric(df["Trans."], errors='coerce').fillna(0).astype(int)

        # Sidebar filters
        st.sidebar.header("🔧 Filter Criteria")

        min_transfers = st.sidebar.slider("Minimum Transfers", 0, 15, 3)
        max_ret_mins = st.sidebar.slider("Max Returning Minutes (%)", 0, 100, 50)
        max_efficiency_rank = st.sidebar.slider("Top AdjOE / AdjDE Rank", 1, 363, 100)

        # Apply filters
        df["AdjOE Rank"] = df["AdjOE"].rank(ascending=False)
        df["AdjDE Rank"] = df["AdjDE"].rank()

        filtered_df = df[
            (df["Trans."] >= min_transfers) &
            (df["Ret Mins"] < max_ret_mins) &
            ((df["AdjOE Rank"] <= max_efficiency_rank) | (df["AdjDE Rank"] <= max_efficiency_rank))
        ]

        st.markdown(f"### 🎯 {len(filtered_df)} Undervalued Teams Found")

        if filtered_df.empty:
            st.warning("No teams match the current filter criteria.")
        else:
            team = st.selectbox("🔍 Choose a team to scout:", filtered_df["Team"].sort_values().unique())
            team_data = filtered_df[filtered_df["Team"] == team].iloc[0]

            st.markdown(f"""
            ## 🏷️ **{team_data['Team']}**
            - 🔄 Transfers: `{int(team_data['Trans.'])}`
            - 🔁 Returning Minutes: `{team_data['Ret Mins']}%`
            - ⚔️ AdjOE: `{team_data['AdjOE']}` (Rank {int(team_data['AdjOE Rank'])})
            - 🛡️ AdjDE: `{team_data['AdjDE']}` (Rank {int(team_data['AdjDE Rank'])})
            - ⏱️ Tempo: `{team_data['Tempo']}`

            📊 **Scouting Summary**  
            `{team_data['Team']}` could be an under-the-radar breakout team this season with high efficiency potential and significant roster turnover.
            """)

    except Exception as e:
        st.error(f"❌ Error loading or processing file: {e}")
else:
    st.info("📁 Please upload `trank_cleaned.csv` to begin scouting.")
