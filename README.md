<<<<<<< HEAD

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

=======
# fetch-pubmed-papers
A Python command-line tool that fetches research papers from PubMed based on a user query and identifies industry-affiliated authors. The results can be saved as a CSV file or displayed in the console. Built with Poetry for dependency management and easy deployment.
>>>>>>> c3d4051b6e5069b69d31ba43ff14e85cd4f8d65d
