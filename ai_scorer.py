# ai_scorer.py
def gpt_lead_reason(company, linkedin_url, score):
    if score >= 8:
        return f"{company} appears to be a strong lead based on our AI analysis. High LinkedIn presence: {linkedin_url}"
    elif score >= 5:
        return f"{company} has moderate potential. Further research recommended. See: {linkedin_url}"
    else:
        return f"{company} currently scores low. Consider revisiting after a few months."
        
        
