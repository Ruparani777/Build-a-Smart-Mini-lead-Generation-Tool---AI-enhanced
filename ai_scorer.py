import pandas as pd
import random

def simple_ai_scoring(company_name, description):
    # Simulated scoring logic for demo purposes
    keywords = ["AI", "machine learning", "automation", "data", "cloud", "analytics"]
    score = 50  # base score

    if pd.notna(description):
        for word in keywords:
            if word.lower() in description.lower():
                score += 10

    score += random.randint(-5, 15)  # simulate some variance
    return min(score, 100)  # cap at 100

# Load leads CSV
input_file = "leads_100.csv"
df = pd.read_csv(input_file)

# Apply AI score
df["AI Score"] = df.apply(
    lambda row: simple_ai_scoring(row.get("Company", ""), row.get("Description", "")),
    axis=1
)

# Save to new file
output_file = "scored_leads_!00.csv"
df.to_csv(output_file, index=False)

print(f"✅ AI Scoring complete. File saved as '{output_file}'")

        
        
