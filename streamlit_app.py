import streamlit as st
import pandas as pd
import base64
from simple_salesforce import Salesforce
from streamlit_authenticator import Authenticate
import yaml
from ai_scorer import simple_ai_scoring # <-- IMPORT YOUR SCORING FUNCTION

# Page setup
st.set_page_config(page_title="Smart Lead Scorer", layout="wide")

# --- Authentication Setup ---
# Make sure your config.yaml is correctly named and configured
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
    st.markdown("Upload your raw leads CSV, and we'll score them for you.")

    uploaded_leads = st.file_uploader("📄 Upload your raw leads CSV", type=["csv"])

    if uploaded_leads is not None:
        leads_df = pd.read_csv(uploaded_leads)
        st.subheader("Raw Leads Data")
        st.dataframe(leads_df, use_container_width=True)

        if st.button("🤖 Run AI Scoring on Leads"):
            # Apply the scoring function directly
            leads_df["AI Score"] = leads_df.apply(
                lambda row: simple_ai_scoring(row.get("Company", ""), row.get("Description", "")),
                axis=1
            )
            # Store the scored data in session state to persist it
            st.session_state['scored_df'] = leads_df
            st.success("✅ AI Scoring Complete!")

    # Check if scored data exists in session state before showing the rest of the app
    if 'scored_df' in st.session_state:
        scored_df = st.session_state['scored_df']

        min_score = st.slider("🎯 Minimum AI Score Filter", min_value=0, max_value=100, value=70)
        filtered_df = scored_df[scored_df["AI Score"] >= min_score]

        st.subheader(f"🔎 Showing {len(filtered_df)} leads with AI score ≥ {min_score}")
        st.dataframe(filtered_df, use_container_width=True)

        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📅 Download Filtered Leads CSV",
            data=csv,
            file_name="filtered_leads.csv",
            mime="text/csv",
        )
        
        # --- CRM Integration (More Securely) ---
        with st.expander("📢 Push to Salesforce CRM"):
            st.info("This feature uses pre-configured credentials from Streamlit Secrets.")
            if st.button("📢 Connect and Upload to Salesforce"):
                try:
                    # Access credentials securely from st.secrets
                    sf_username = st.secrets["salesforce"]["username"]
                    sf_password = st.secrets["salesforce"]["password"]
                    sf_token = st.secrets["salesforce"]["token"]
                    
                    sf = Salesforce(username=sf_username, password=sf_password, security_token=sf_token)
                    
                    st.write(f"Uploading {len(filtered_df)} leads...")
                    for _, row in filtered_df.iterrows():
                        sf.Lead.create({
                            'Company': row['Company'],
                            'Status': 'Open - Not Contacted',
                            'Description': f"AI Score: {row['AI Score']}"
                        })
                    st.success("Leads pushed to Salesforce CRM successfully!")
                except Exception as e:
                    st.error(f"CRM upload failed: {e}")

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
