import streamlit as st
import pandas as pd

st.title("Build a Smart Mini lead Generation Tool")

try:
    df = pd.read_csv("app/scored_leads_100.csv")
    st.success("Loaded scored_leads_100.csv successfully.")
    
    score_filter = st.slider("Minimum AI Score", 1, 10, 6)
    filtered = df[df["ai_score"] >= score_filter]
    
    st.write(f"Showing {len(filtered)} leads with AI score >= {score_filter}")
    st.dataframe(filtered)

    st.download_button("Download Filtered Leads", filtered.to_csv(index=False), file_name="filtered_leads.csv")
except FileNotFoundError:
    st.error("Please run scraper.py and ai_scorer.py first to generate leads.")
