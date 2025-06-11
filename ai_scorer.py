# ai_scorer.py
import openai

openai.api_key = "your-openai-key"  # Replace with your actual key or use environment variable

def gpt_lead_reason(company, linkedin, score):
    prompt = f"Why might this be a valuable lead? Company: {company}, LinkedIn: {linkedin}, Score: {score}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT Error: {e}"
        
