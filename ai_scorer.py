import openai
import pandas as pd
import time

openai.api_key = "your_openai_api_key"

def score_company(description):
    prompt = f"Score the following company on how AI-ready they are from 1 to 10:\n\n{description}\n\nScore:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=10,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error:", e)
        return "N/A"

def enrich_leads(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df["ai_score"] = df["linkedin"].apply(lambda url: score_company(url))  # Simulated
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    enrich_leads("leads_100.csv", "scored_leads_100.csv")
  
