# OpenAlex Scientists Extraction
This project fetches, processes, and analyzes author data from OpenAlex API for scientists affiliated with institutions in Saudi Arabia (SA), UAE (AE), and Qatar (QA). The processed dataset is derived from publicly available OpenAlex data and follows their licensing terms. The extracted metadata is shared in compliance with OpenAlex’s terms of use. The original source can be accessed at https://openalex.org/.


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
