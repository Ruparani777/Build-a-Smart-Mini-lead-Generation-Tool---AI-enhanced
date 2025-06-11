import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Lead Scoring", layout="centered")
st.title("🚀 AI-Enhanced Lead Scoring Tool")
st.write("Upload your raw leads and view AI-enhanced scoring for decision-making.")

# Upload raw leads CSV
st.subheader("📤 Upload your raw leads CSV")
raw_file = st.file_uploader("Upload your raw leads CSV", type=["csv"])

# Upload AI-scored leads CSV
st.subheader("📤 Upload your AI-scored leads CSV")
scored_file = st.file_uploader("Upload your AI-scored leads CSV", type=["csv"])

if raw_file is not None and scored_file is not None:
    try:
        # Read the uploaded files
        leads_df = pd.read_csv(raw_file)
        scored_df = pd.read_csv(scored_file)

        # Strip column names of leading/trailing spaces
        leads_df.columns = leads_df.columns.str.strip()
        scored_df.columns = scored_df.columns.str.strip()

        # Log column names for debugging
        st.write("Raw leads columns:", leads_df.columns.tolist())
        st.write("Scored leads columns:", scored_df.columns.tolist())

        # Check if 'company_keyword' exists in both
        if "company_keyword" in leads_df.columns and "company_keyword" in scored_df.columns:
            # Merge data
            merged_df = pd.merge(leads_df, scored_df, on="company_keyword", how="left")
            st.success("Files uploaded and merged successfully!")

            # Show preview
            st.subheader("🔍 Merged Data Preview")
            st.dataframe(merged_df)

            # Download button
            csv = merged_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Merged CSV", csv, "merged_leads.csv", "text/csv")
        else:
            st.error("❌ 'company_keyword' column not found in both files. Please check your CSV column names.")
    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")
else:
    st.info("Please upload both CSV files to continue.")
    
