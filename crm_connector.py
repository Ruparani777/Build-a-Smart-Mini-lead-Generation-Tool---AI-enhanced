# crm_connector.py
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput

hubspot_client = HubSpot(access_token="pat-na2-22972c68-0743-4115-8cb2-fca63f103b45")

def push_lead_to_hubspot(company_name, linkedin_url, score):
    properties = {
        "firstname": "Lead",
        "lastname": company_name,
        "website": linkedin_url,
        "company": company_name,
        "jobtitle": f"Score: {score}"
    }
    input_data = SimplePublicObjectInput(properties=properties)
    try:
        response = hubspot_client.crm.contacts.basic_api.create(simple_public_object_input=input_data)
        return response
    except Exception as e:
        return f"HubSpot Error: {e}"
