# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth
from ai_scorer import gpt_lead_reason
from crm_connector import push_lead_to_hubspot

# --- Authentication Setup ---
users = {
    "roopa@example.com": {
        "name": "Roopa",
        "password": "2d826324f1eaf66b2db7aa8caf41c96e"
    }
}

authenticator = stauth.Authenticate(
    users,
    "auth_cookie", "some_signature_key", cookie_expiry_days=1
)

name, auth_status, username = authenticator.login("Login", "main")

if not auth_status:
    st.warning("Please log in to continue.")
    st.stop()

authenticator.logout("Logout", "sidebar")
st.success(f"Welcome {name}!")

# --- App Logic ---
st.title("🧠 AI-Powered Lead Scorer")

raw_file = st.file_uploader("Upload Raw Leads CSV", type="csv")
scored_file = st.file_uploader("Upload Scored Leads CSV", type="csv")

if raw_file and scored_file:
    leads_df = pd.read_csv(raw_file)
    scored_df = pd.read_csv(scored_file)

    if "Company" in leads_df.columns and "Company" in scored_df.columns:
        merged_df = pd.merge(leads_df, scored_df, on="Company", how="left")

        # GPT Reasoning
        with st.spinner("Generating AI explanations..."):
            merged_df["GPT_Reason"] = merged_df.apply(
                lambda row: gpt_lead_reason(
                    row.get("Company", ""), row.get("linkedin_url", ""), row.get("ai_score", 0)
                ), axis=1
            )

        # Score filter
        min_score = int(merged_df["ai_score"].min())
        max_score = int(merged_df["ai_score"].max())
        score_filter = st.slider("Filter by AI Score", min_value=min_score, max_value=max_score, value=(min_score, max_score))
        filtered_df = merged_df[(merged_df["ai_score"] >= score_filter[0]) & (merged_df["ai_score"] <= score_filter[1])]

        st.dataframe(filtered_df)

        # Visualizations
        st.subheader("📊 Score Distribution")
        st.plotly_chart(px.histogram(filtered_df, x="ai_score", nbins=10, title="Lead Score Distribution"))

        st.subheader("🏢 Company Breakdown")
        pie_fig = px.pie(filtered_df, names="Company", title="Leads by Company")
        st.plotly_chart(pie_fig)

        # CRM Push Button
        if st.button("🚀 Push to HubSpot"):
            for _, row in filtered_df.iterrows():
                push_lead_to_hubspot(row["Company"], row.get("linkedin_url", ""), row["ai_score"])
            st.success("✅ Leads pushed to HubSpot!")

        st.download_button("Download Filtered Leads", filtered_df.to_csv(index=False), file_name="filtered_leads.csv")

    else:
        st.error("❌ 'Company' column is missing in one of the files.")
else:
    st.info("Please upload both CSV files to continue.")
