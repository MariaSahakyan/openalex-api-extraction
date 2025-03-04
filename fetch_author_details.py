import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

API_KEY = None  # Add API key if required
AUTHORS_FILE = "data/authors_basic.csv"

def fetch_author_details(author_id):
    """Fetch detailed information for a given author ID."""
    url = f"https://api.openalex.org/authors/{author_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else None
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def parse_author_data(author_data):
    """Parse detailed author metadata."""
    return {
        "Author ID": author_data.get("id"),
        "Name": author_data.get("display_name"),
        "Cited By Count": author_data.get("cited_by_count"),
        "H-Index": author_data.get("summary_stats", {}).get("h_index"),
        "i10-Index": author_data.get("summary_stats", {}).get("i10_index"),
        "Affiliations": author_data.get("affiliations"),
        "Topics": author_data.get("topics"),
        "Counts by Year": author_data.get("counts_by_year"),
        "Works API URL": author_data.get("works_api_url"),
    }

# Load authors from CSV
df_authors = pd.read_csv(AUTHORS_FILE)

# Fetch details in parallel
detailed_authors = []
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(tqdm(executor.map(fetch_author_details, df_authors["Author ID"]), total=len(df_authors)))

# Process and save results
detailed_authors = [parse_author_data(author) for author in results if author]
df_detailed = pd.DataFrame(detailed_authors)
df_detailed.to_csv("data/authors_detailed.csv", index=False)
print("Saved authors_detailed.csv")
