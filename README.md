
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

