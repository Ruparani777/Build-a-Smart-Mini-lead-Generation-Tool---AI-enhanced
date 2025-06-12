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
        # --- CRM Integration ---
with st.expander("📢 Push to Salesforce CRM"):
    st.info("This section demonstrates how the app would connect to a CRM like Salesforce.")
    st.markdown("""
    In a real-world scenario, the app would securely connect to Salesforce using credentials 
    stored in Streamlit's secrets manager. For this demo, the connection is disabled.
    """)
    
    # The button is disabled to prevent errors
    if st.button("📢 Connect and Upload to Salesforce", disabled=True):
        # This code will not run because the button is disabled.
        # It's left here to show the logic.
        pass

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
