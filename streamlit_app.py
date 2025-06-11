import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="AI Lead Scoring Tool", layout="wide")

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

if raw_file and scored_file:
    # Read CSVs
    leads_df = pd.read_csv(raw_file)
    scored_df = pd.read_csv(scored_file)

    # Strip column names
    leads_df.columns = leads_df.columns.str.strip()
    scored_df.columns = scored_df.columns.str.strip()

    # Merge on 'company_keyword'
    merged_df = pd.merge(leads_df, scored_df, on="company_keyword", how="left")

    st.success("✅ Files uploaded and merged successfully!")

    # Add score category column
    def classify_score(score):
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    merged_df["score_category"] = merged_df["ai_score"].apply(classify_score)

    # Filter UI
    st.subheader("🎯 Filter by Score Category")
    selected_categories = st.multiselect(
        "Select score categories to display:",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"]
    )

    filtered_df = merged_df[merged_df["score_category"].isin(selected_categories)]

    st.subheader("🔍 Filtered Leads")
    st.dataframe(filtered_df)

    # Pie chart
    st.subheader("📊 AI Score Category Distribution")
    category_counts = merged_df["score_category"].value_counts().reset_index()
    category_counts.columns = ["Score Category", "Count"]

    fig = px.pie(category_counts, values="Count", names="Score Category", title="Lead Score Category Breakdown")
    st.plotly_chart(fig, use_container_width=True)

    # Excel download
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Filtered Leads")
            writer.save()
        output.seek(0)
        return output

    excel_file = convert_df_to_excel(filtered_df)
    st.download_button(
        label="⬇️ Download Filtered Leads as Excel",
        data=excel_file,
        file_name="filtered_leads.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Please upload both the raw leads and AI-scored leads CSV files.")
    
