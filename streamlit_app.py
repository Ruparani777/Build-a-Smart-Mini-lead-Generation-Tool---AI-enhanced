import streamlit as st
import pandas as pd
import base64

# Page setup
st.set_page_config(page_title="Smart Lead Scorer", layout="wide")
st.title("🚀 AI-Enhanced Lead Scoring Tool")
st.markdown("Upload your raw leads and view AI-enhanced scoring for decision-making.")

# File upload
uploaded_leads = st.file_uploader("📤 Upload your raw leads CSV", type=["csv"])
uploaded_scores = st.file_uploader("📤 Upload your AI-scored leads CSV", type=["csv"])

if uploaded_leads is not None and uploaded_scores is not None:
    # Load CSV files
    leads_df = pd.read_csv(uploaded_leads)
    scored_df = pd.read_csv(uploaded_scores)

    # Merge data
    merged_df = pd.merge(leads_df, scored_df, on="Company", how="left")

    st.success("✅ Files uploaded and merged successfully!")

    # Score filtering
    min_score = st.slider("🎯 Minimum AI Score Filter", min_value=0, max_value=100, value=70)
    filtered_df = merged_df[merged_df["AI Score"] >= min_score]

    st.subheader(f"🔎 Showing {len(filtered_df)} leads with AI score ≥ {min_score}")
    st.caption("Use the slider to filter high-quality leads based on their AI readiness score.")

    # Display filtered leads using Streamlit's native table
    st.dataframe(filtered_df, use_container_width=True)

    # Download filtered leads
    csv = filtered_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_leads.csv">📥 Download Filtered Leads CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

else:
    st.warning("👆 Please upload both CSV files to continue.")
    
