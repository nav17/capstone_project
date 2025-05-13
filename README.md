# Capstone Project

An ETL & Streamlit Project.

### Dataset

https://api.tfl.gov.uk/

## Installation

### Prerequisites

Requires Python 3.13 or above

### Setup

To setup this project:

```zsh
pip install -r requirements-setup.txt
pip install -e .
```


To run (during development):

```zsh
python3 -m scripts.run_etl dev
```

To run tests:

```zsh
pytest
```

To run streamlit app:

```zsh
streamlit run streamlit/main.py
```

### Troubleshooting

If tests don't run

```zsh
pip install psycopg_binary
```
