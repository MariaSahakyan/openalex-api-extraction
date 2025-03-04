# OpenAlex Scientists Extraction
This project fetches, processes, and analyzes author data from OpenAlex API for scientists affiliated with institutions in Saudi Arabia (SA), UAE (AE), and Qatar (QA). The processed dataset is derived from publicly available OpenAlex data and follows their licensing terms. The extracted metadata is shared in compliance with OpenAlex’s terms of use. The original source can be accessed at https://openalex.org/.

##  Features
- **Fetches** authors from OpenAlex API
- **Retrieves** detailed metadata (citations, affiliations, H-index, topics)
- **Saves** results as structured CSV files

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/openalex-scientists.git
   cd openalex-scientists
2. Install dependencies:
   pip install pandas requests tqdm
3. Run the scripts:
   python fetch_authors.py
   python fetch_author_details.py
