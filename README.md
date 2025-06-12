# Build-a-Smart-Mini-lead-Generation-Tool---AI-enhanced
 🚀 Smart AI-Enhanced Lead Generation & Scoring Tool

Welcome to the AI Readiness Lead Scoring App — a smart, secure, and scalable lead filtering tool designed to streamline post-acquisition growth using AI-driven insights.

Built for Caprae Capital’s AI Readiness Challenge, this project replicates key features of SaaSquatchLeads with a unique twist: filtering and CRM integration based on AI scoring models.

🔍 Project Overview

This Streamlit-based web app allows authenticated users to:

- 📁 Upload raw leads (CSV format)
- 🤖 Match leads with AI-based scoring files
- 🎯 Filter leads based on customizable AI thresholds
- 📊 View results in an interactive table
- 💾 Download filtered leads instantly
- 🔗 Push high-quality leads to Salesforce CRM
- 🔐 Secure the entire app with password authentication

📁 Directory Structure

Build-a-Smart-Mini-lead-Generation-Tool---AI-enhanced/
│
#streamlit\_app.py          
#Main web app- ai\_scorer.py            
# Dummy AI scoring logic- scraper.py                
# Lead scraping logic (static example)-config.yaml               
# Authentication configuration-requirements.txt          
# Python dependencies -scored\_leads\_100.csv      
# Sample scored data-leads_100.csv #Sample raw leads 
README.md                 
# You are here!


 ✅ Features

 🔐 login System-  Secured with streamlit-authenticator` and config.yaml                 
 📤 File Upload - Upload raw lead data and scored leads (CSV)                                
Filtering by AI Score - Interactive slider to select minimum AI readiness score                 
 📊 Visual Dashboard- View merged, filtered leads in an easy-to-read table                      
 💾 Download Option - Export filtered leads as a clean CSV                                 
 🔌 CRM Integration-Push high-quality leads directly  to Salesforce crm

 🚀 How to Run

🌐 Streamlit Cloud
1. Fork this repo and deploy it to [Streamlit Cloud](https://streamlit.io/cloud)
2. Ensure all files including `streamlit_app.py`, `config.yaml`, and CSV files are uploaded
3. Set up any secrets for Salesforce credentials (optional)

 🧑‍💻 Local Setup (Optional)
 
bash
# Clone repo
git clone https://github.com/Ruparani777/Build-a-Smart-Mini-lead-Generation-Tool---AI-enhanced.git
cd Build-a-Smart-Mini-lead-Generation-Tool---AI-enhanced

# Create virtual environment and install dependencies
pip install -r requirements.txt

# Run app
streamlit run streamlit_app.py

---
 🔐 Authentication Setup

Modify `config.yaml` to define usernames and hashed passwords.
Generate hashed passwords using this script:

Python
from streamlit_authenticator.hasher import Hasher
hashed = Hasher(['your_password']).generate()
print(hashed)



🔗 Salesforce CRM Integration

To enable CRM upload:

 Provide your Salesforce `username`, `password`, and `security token`
 Leads will be pushed automatically via `simple_salesforce`

-

📝 Submission Summary
⏱️ Time spent: \~5 hours
 ✅ Focus: Quality-first development of a lead scoring & filtering engine
 💡 Value: Combines AI scoring, user-friendly UI, and CRM automation for high-leverage M\&A impact




📷 Demo Video

➡️ [Live app)(https://github.com/Ruparani777/Build-a-Smart-Mini-lead-Generation-Tool---AI-enhanced#demo)



 💡 Future Improvements

 Add automated lead enrichment from public data
 Deploy as a containerized app with Docker
Enhance CRM integrations (HubSpot, Zoho)
Add chatbot interface for filtering assistance

-

 🙋‍♀️ Author

Ruparani Thupakula
Caprae AI Readiness Challenge Submission
GitHub(https://github.com/Ruparani777)


