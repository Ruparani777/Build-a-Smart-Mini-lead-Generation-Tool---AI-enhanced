
import requests
import os

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY") or "pat-na2-22972c68-0743-4115-8cb2-fca63f103b45"

def push_lead_to_hubspot(company, linkedin_url, ai_score):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUBSPOT_API_KEY}"
    }
    data = {
        "properties": {
            "email": f"{company.lower().replace(' ', '')}@example.com",
            "firstname": company,
            "website": linkedin_url,
            "company": company,
            "score": str(ai_score),
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"✅ Lead {company} added to HubSpot.")
    else:
        print(f"❌ Failed to push {company}: {response.text}")
        

