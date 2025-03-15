import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the directory containing main.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import fetch_pubmed_papers, fetch_paper_details

class TestMain(unittest.TestCase):
    @patch('main.requests.get')
    def test_fetch_pubmed_papers(self, mock_get):
        # Mock the API response for the search query
        mock_response = Mock()
        mock_response.json.return_value = {
            "esearchresult": {
                "idlist": ["12345678", "87654321"]
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = fetch_pubmed_papers("cancer")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    @patch('main.requests.get')
    def test_fetch_paper_details(self, mock_get):
        # Mock the API response for fetching paper details
        mock_response = Mock()
        mock_response.content = b"""
        <PubmedArticleSet>
            <PubmedArticle>
                <MedlineCitation>
                    <PMID>12345678</PMID>
                    <ArticleTitle>Sample Title</ArticleTitle>
                    <PubDate>
                        <Year>2025</Year>
                    </PubDate>
                    <AuthorList>
                        <Author>
                            <LastName>Smith</LastName>
                            <ForeName>John</ForeName>
                            <Affiliation>Pharma Inc.</Affiliation>
                            <Email>john.smith@pharma.com</Email>
                        </Author>
                    </AuthorList>
                </MedlineCitation>
            </PubmedArticle>
        </PubmedArticleSet>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = fetch_paper_details(["12345678"])
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]["PubmedID"], "12345678")
        self.assertEqual(result[0]["Title"], "Sample Title")

if __name__ == '__main__':
    unittest.main()