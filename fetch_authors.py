import requests
import pandas as pd
import time

API_URL = "https://api.openalex.org/authors"
COUNTRY_FILTER = "affiliations.institution.country_code:SA|AE|QA"
PER_PAGE = 100  # Number of results per request
API_KEY = None  # Add API key if needed: "your_api_key"

def fetch_all_authors():
    """Fetch authors from OpenAlex API based on country filter."""
    all_results = []
    base_url = API_URL
    params = {"filter": COUNTRY_FILTER, "per_page": PER_PAGE}
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else None

    while base_url:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.url}")
            break
        data = response.json()
        all_results.extend(data.get("results", []))
        base_url = data.get("meta", {}).get("next")  # Get next page
        time.sleep(1)  # Respect rate limits

    return all_results

# Fetch authors and save to CSV
authors = fetch_all_authors()

if authors:
    df = pd.DataFrame([
        {
            "Author ID": author.get("id"),
            "Name": author.get("display_name"),
            "ORCID": author.get("orcid"),
            "Works Count": author.get("works_count"),
            "Affiliations": author.get("affiliations"),
        }
        for author in authors
    ])
    df.to_csv("data/authors_basic.csv", index=False)
    print("Saved authors_basic.csv")
else:
    print("No authors found")
