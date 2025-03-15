import argparse
import csv
import logging
import requests
from typing import List, Dict, Optional
from xml.etree import ElementTree
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_pubmed_papers(query: str) -> List[Dict[str, str]]:
    """
    Fetches papers from PubMed API based on the user query.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 10,
        "usehistory": "y",
        "retmode": "json"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    search_results = response.json()
    pmids = search_results.get("esearchresult", {}).get("idlist", [])
    return fetch_paper_details(pmids)

def fetch_paper_details(pmids: List[str]) -> List[Dict[str, str]]:
    """
    Retrieves paper details from PubMed given a list of PMIDs.
    """
    if not pmids:
        return []
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return parse_pubmed_response(response.content)

def parse_pubmed_response(xml_data: str) -> List[Dict[str, str]]:
    """
    Parses the XML response from PubMed to extract relevant details.
    """
    root = ElementTree.fromstring(xml_data)
    papers = []
    
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle", default="Unknown Title")
        pub_date = article.findtext(".//PubDate/Year", default="Unknown Date")
        
        authors = []
        companies = []
        emails = []
        
        for author in article.findall(".//Author"):
            last_name = author.findtext("LastName", default="")
            first_name = author.findtext("ForeName", default="")
            affiliation = author.findtext("..//Affiliation", default="")
            email = author.findtext("..//Email", default="")
            
            if affiliation and any(word in affiliation.lower() for word in ["pharma", "biotech", "corporation", "inc.", "ltd"]):
                authors.append(f"{first_name} {last_name}")
                companies.append(affiliation)
            
            if email:
                emails.append(email)
        
        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(authors) if authors else "None",
            "Company Affiliation(s)": ", ".join(companies) if companies else "None",
            "Corresponding Author Email": emails[0] if emails else "None"
        })
    return papers

def save_to_csv(papers: List[Dict[str, str]], filename: str):
    """
    Saves the extracted data to a CSV file.
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(papers)

def main():
    """
    Main function to handle command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with industry-affiliated authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file name")
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info("Fetching papers...")
    papers = fetch_pubmed_papers(args.query)
    
    if args.file:
        save_to_csv(papers, args.file)
        logging.info(f"Results saved to {args.file}")
    else:
        logging.info("Results:")
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()

# Poetry pyproject.toml file
pyproject_toml = """
[tool.poetry]
name = "fetch-pubmed-papers"
version = "0.1.0"
description = "A tool to fetch research papers from PubMed and filter non-academic authors."
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.31.0"

[tool.poetry.scripts]
get-papers-list = "fetch_pubmed_papers:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

# README.md file
readme_md = """
# Fetch PubMed Papers

This tool fetches research papers from PubMed based on a user query and extracts industry-affiliated authors.

## Installation

```sh
poetry install
```

## Usage

```sh
poetry run get-papers-list "cancer treatment" -f output.csv
```

## Features
- Fetches research papers from PubMed.
- Identifies non-academic authors affiliated with pharmaceutical or biotech companies.
- Saves results as a CSV file.

## Dependencies
- Python 3.8+
- Poetry
- Requests

## Publishing to TestPyPI
To publish the package to TestPyPI:

```sh
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry publish --build -r test-pypi
```

"""

# Writing the files to disk
with open("pyproject.toml", "w") as f:
    f.write(pyproject_toml)

with open("README.md", "w") as f:
    f.write(readme_md)
