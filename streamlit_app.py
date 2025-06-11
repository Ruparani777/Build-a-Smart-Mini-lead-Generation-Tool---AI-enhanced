
    # Excel download
    import streamlit as st
import pandas as pd

st.title("🚀 AI-Enhanced Lead Scoring Tool")
st.write("Upload your raw leads and view AI-enhanced scoring for decision-making.")

# Upload raw leads CSV
st.subheader("📤 Upload your raw leads CSV")
raw_file = st.file_uploader("Upload your raw leads CSV", type=["csv"])
leads_df = None

# Upload AI-scored leads CSV
st.subheader("📤 Upload your AI-scored leads CSV")
scored_file = st.file_uploader("Upload your AI-scored leads CSV", type=["csv"])
scored_df = None

# If both files are uploaded
if raw_file is not None and scored_file is not None:
    # Read the files
    leads_df = pd.read_csv(raw_file)
    scored_df = pd.read_csv(scored_file)

    # Optional: clean column names
    leads_df.columns = leads_df.columns.str.strip()
    scored_df.columns = scored_df.columns.str.strip()

    # Merge based on "company_keyword"
    merged_df = pd.merge(leads_df, scored_df, on="company_keyword", how="left")

    st.success("Files uploaded and merged successfully!")
    st.subheader("🔍 Merged Data Preview")
    st.dataframe(merged_df)

    # Optional: download merged data
    csv = merged_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Merged CSV", csv, "merged_leads.csv", "text/csv")

else:
    st.info("Please upload both the raw leads and AI-scored CSV files.")
    
