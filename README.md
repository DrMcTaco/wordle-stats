## Setup 
To use this package first create a virtual environment to isolate its dependencies from your system's python.

    python -m venv .venv

Then activate the new virtualenv

    source .venv/bin/activate

Then install the package 

    pip install -e .

## Load some wordle data
To ingest the worde scores stats run:

    python src/wordle-stats/main.py


## Check the score distribution
You can display the score distribution by running the sql in `distribution.sql`:

    sqlite3 -header -column data/wordle.db < distribution.sql