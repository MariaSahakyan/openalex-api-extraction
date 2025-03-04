# OpenAlex Scientists Extraction
This project provides Python scripts for fetching and processing author and work data from the OpenAlex API, specifically for scientists affiliated with institutions in Saudi Arabia (SA), UAE (AE), and Qatar (QA). The scripts allow users to retrieve and analyze metadata directly from OpenAlex, following their licensing terms.

No extracted data is included in this repository. Users must run the scripts themselves to obtain data. The OpenAlex API and its terms of use can be accessed at https://openalex.org/.


##  Features
- **Fetches author metadata** from OpenAlex
- **Retrieves detailed author information** (citations, H-index, affiliations)
- **Extracts works (articles, books, preprints)**
- **Uses pagination & rate-limit handling**
- **Stores outputs in CSV & JSONL formats**

##  Installation
Clone the repository and install dependencies:

```sh
git clone https://github.com/yourusername/openalex-scientists.git
cd openalex-scientists
pip install -r requirements.txt
