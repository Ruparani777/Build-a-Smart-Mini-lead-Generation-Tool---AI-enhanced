import streamlit as st
import pandas as pd
import plotly.express as px

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

        # Debug column names
        st.write("Raw leads columns:", leads_df.columns.tolist())
        st.write("Scored leads columns:", scored_df.columns.tolist())

        # Ensure required column exists
        if "company_keyword" in leads_df.columns and "company_keyword" in scored_df.columns:
            merged_df = pd.merge(leads_df, scored_df, on="company_keyword", how="left")
            st.success("Files uploaded and merged successfully!")

            # Filter by ai_score
            if "ai_score" in merged_df.columns:
                min_score, max_score = float(merged_df["ai_score"].min()), float(merged_df["ai_score"].max())
                st.subheader("🎯 Filter Leads by AI Score")
                score_range = st.slider("Select score range", float(min_score), float(max_score), (min_score, max_score))
                filtered_df = merged_df[(merged_df["ai_score"] >= score_range[0]) & (merged_df["ai_score"] <= score_range[1])]
                
                # Data preview
                st.subheader("🔍 Filtered Leads")
                st.dataframe(filtered_df)

                # Pie Chart of Score Distribution
                st.subheader("📊 AI Score Distribution (Binned)")
                binned_scores = pd.cut(filtered_df["ai_score"], bins=5)
                score_counts = binned_scores.value_counts().sort_index()
                fig_pie = px.pie(values=score_counts.values, names=score_counts.index.astype(str), title="Score Range Distribution")
                st.plotly_chart(fig_pie)

                # Optional: Bar chart of scores per company
                st.subheader("🏢 AI Score by Company")
                fig_bar = px.bar(filtered_df, x="company_keyword", y="ai_score", title="Company vs AI Score", labels={"company_keyword": "Company"}, height=400)
                st.plotly_chart(fig_bar)

                # Download filtered data
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Filtered Leads", csv, "filtered_leads.csv", "text/csv")
            else:
                st.warning("⚠️ 'ai_score' column not found in AI-scored CSV.")
        else:
            st.error("❌ 'company_keyword' column not found in both files.")
    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")
else:
    st.info("Please upload both CSV files to continue.")
                
