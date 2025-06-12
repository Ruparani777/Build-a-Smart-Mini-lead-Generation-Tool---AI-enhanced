import streamlit as st
import pandas as pd
import base64
from simple_salesforce import Salesforce
from streamlit_authenticator import Authenticate
import yaml

# Page setup
st.set_page_config(page_title="Smart Lead Scorer", layout="wide")

# --- Authentication Setup ---
with open('config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.title(f"🚀 Welcome {name} - AI-Enhanced Lead Scoring Tool")
    st.markdown("Upload your raw leads and view AI-enhanced scoring for decision-making.")

    # File upload
    uploaded_leads = st.file_uploader("📄 Upload your raw leads CSV", type=["csv"])
    uploaded_scores = st.file_uploader("📄 Upload your AI-scored leads CSV", type=["csv"])

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
        href = f'<a href="data:file/csv;base64,{b64}" download="filtered_leads.csv">📅 Download Filtered Leads CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

        # --- CRM Integration (Salesforce Example) ---
        with st.expander("📢 Push to Salesforce CRM"):
            sf_username = st.text_input("Salesforce Username")
            sf_password = st.text_input("Salesforce Password", type='password')
            sf_token = st.text_input("Salesforce Security Token", type='password')

            if st.button("📢 Connect and Upload Leads"):
                try:
                    sf = Salesforce(username=sf_username, password=sf_password, security_token=sf_token)
                    for _, row in filtered_df.iterrows():
                        sf.Lead.create({
                            'Company': row['Company'],
                            'Email': row.get('Email', ''),
                            'Phone': row.get('Phone', ''),
                            'FirstName': row.get('First Name', 'Lead'),
                            'LastName': row.get('Last Name', 'Candidate'),
                            'Status': 'Open - Not Contacted',
                            'Description': f"AI Score: {row['AI Score']}"
                        })
                    st.success("Leads pushed to Salesforce CRM successfully!")
                except Exception as e:
                    st.error(f"CRM upload failed: {e}")
else:
    st.error("Please enter valid credentials.")
