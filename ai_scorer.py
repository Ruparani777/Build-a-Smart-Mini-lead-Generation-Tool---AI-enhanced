import pandas as pd
import random

# This function can now be imported into your main app
def simple_ai_scoring(company_name, description=""):
    keywords = ["AI", "machine learning", "automation", "data", "cloud", "analytics"]
    score = 50
    if pd.notna(description):
        for word in keywords:
            if word.lower() in description.lower():
                score += 10
    score += random.randint(-5, 15)
    return min(score, 100)
        
        
