import requests
import time
import json
import pandas as pd
from tqdm import tqdm

# API Configuration
BASE_URL = "https://api.openalex.org/works"
RESULTS_PER_PAGE = 200
SAVE_INTERVAL = 100  # Save results every X requests
REQUESTS_PER_SECOND = 10
OUTPUT_FILE = "data/works_detailed.jsonl"
AUTHORS_FILE = "data/authors_basic.csv"  # Read author IDs from this file

# Load author IDs from `authors_basic.csv`
def load_author_ids():
    """Reads author IDs from the CSV file."""
    df = pd.read_csv(AUTHORS_FILE)
    return df["Author ID"].dropna().unique().tolist()  # Ensure unique IDs

# Function to fetch work data from OpenAlex API
def fetch_data(api_url, cursor=None):
    """Handles API requests with retries and pagination."""
    params = {"per_page": RESULTS_PER_PAGE}
    if cursor:
        params["cursor"] = cursor

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                return response.json()
            print(f"Error {response.status_code}: {response.url}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        time.sleep(2 ** attempt)  # Exponential backoff (1s, 2s, 4s)

    print(f"Failed to fetch data after {retries} attempts: {api_url}")
    return None

# Function to extract relevant work details
def extract_work_details(work, author_id):
    """Extracts structured work metadata including authors, topics, and affiliations."""
    primary_location = work.get("primary_location", {}) or {}
    source = primary_location.get("source", {}) or {}
    authorships = work.get("authorships", []) or []

    # Skip works with more than 10 authors
    if len(authorships) > 10:
        return {
            "id": work.get("id"),
            "publication_year": work.get("publication_year"),
            "number_of_authors": len(authorships),
        }

    # Extract author details
    author_details = [
        {
            "author_id": auth.get("author", {}).get("id"),
            "author_name": auth.get("author", {}).get("display_name"),
            "author_position": auth.get("author_position"),
            "is_corresponding": auth.get("is_corresponding"),
            "raw_affiliation": auth.get("raw_affiliation_strings", ["N/A"])[0],
            "affiliations": [
                {
                    "institution_id": inst.get("id"),
                    "institution_name": inst.get("display_name"),
                    "institution_country": inst.get("country_code"),
                }
                for inst in auth.get("institutions", [])
            ],
        }
        for auth in authorships
    ]

    # Extract topics
    topics = [
        {
            "topic_id": topic.get("id"),
            "topic_name": topic.get("display_name"),
            "topic_score": topic.get("score"),
        }
        for topic in work.get("topics", [])
    ]

    return {
        "id": work.get("id"),
        "author_id": author_id,
        "publication_year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "language": work.get("language"),
        "journal_name": source.get("display_name"),
        "source_type": source.get("type"),
        "is_open_access": work.get("open_access", {}).get("is_oa"),
        "authors": author_details,
        "topics": topics,
        "citation_counts_by_year": work.get("counts_by_year"),
    }

# Function to process dataset and store results
def process_dataset():
    """Iterates through author IDs from CSV and retrieves their works."""
    results = []
    total_requests = 0
    start_time = time.time()
    
    author_ids = load_author_ids()  # Load author IDs dynamically

    for author_id in tqdm(author_ids, desc="Processing Authors"):
        api_url = f"{BASE_URL}?filter=author.id:{author_id},type:article|preprint|book-chapter|book|paratext"
        cursor = "*"

        while cursor:
            # Stop if max requests per second is exceeded
            elapsed_time = time.time() - start_time
            if total_requests / elapsed_time > REQUESTS_PER_SECOND:
                time.sleep(1 / REQUESTS_PER_SECOND)

            # Fetch data
            data = fetch_data(api_url, cursor)
            if not data:
                break

            # Process works
            for work in data["results"]:
                if work.get("publication_year", 0) >= 1945:
                    work_details = extract_work_details(work, author_id)
                    work_details["number_of_works"] = data["meta"]["count"]
                    work_details["source_link"] = api_url  # Track source link
                    results.append(work_details)

            total_requests += 1

            # Save periodically
            if total_requests % SAVE_INTERVAL == 0:
                save_results(results)
                results = []  # Clear after saving

            # Pagination
            cursor = data.get("meta", {}).get("next_cursor")
            if not cursor:
                break

    # Final save
    if results:
        save_results(results)

# Function to save results to JSONL file
def save_results(results):
    """Saves data in JSONL format."""
    with open(OUTPUT_FILE, "a") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
    print(f"Saved {len(results)} results to {OUTPUT_FILE}")

# Run the script
if __name__ == "__main__":
    process_dataset()
    print("Work extraction completed.")
