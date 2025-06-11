import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_linkedin_urls(query, num_results=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    urls = []
    for i in range(0, num_results, 10):
        url = f"https://www.google.com/search?q={query}+site%3Alinkedin.com&start={i}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        for g in soup.find_all("div", class_="tF2Cxc"):
            link = g.find("a", href=True)
            if link:
                urls.append(link["href"])
    return urls

# Example usage
if __name__ == "__main__":
    companies = ["AI consulting", "Machine learning SaaS", "Healthcare SaaS"]
    results = []
    for company in companies:
        links = get_linkedin_urls(company)
        for link in links:
            results.append({"company": company, "linkedin": link})
    pd.DataFrame(results).to_csv("leads_100.csv", index=False)
  
