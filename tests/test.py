import pytest
from main import fetch_pubmed_papers

def test_fetch_pubmed_papers():
    query = "cancer"
    result = fetch_pubmed_papers(query)
    assert isinstance(result, list)