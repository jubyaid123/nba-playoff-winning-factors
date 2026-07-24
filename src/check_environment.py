"""Verify that the project's main Python packages are installed correctly."""

import sys

import matplotlib
import numpy as np
import pandas as pd
import psycopg
import requests
import scipy
import sqlalchemy
import statsmodels
from nba_api.stats.endpoints import leaguegamelog


def main() -> None:
    """Print package versions and confirm that imports succeed."""
    print(f"Python: {sys.version.split()[0]}")
    print(f"pandas: {pd.__version__}")
    print(f"NumPy: {np.__version__}")
    print(f"requests: {requests.__version__}")
    print(f"Matplotlib: {matplotlib.__version__}")
    print(f"SciPy: {scipy.__version__}")
    print(f"statsmodels: {statsmodels.__version__}")
    print(f"SQLAlchemy: {sqlalchemy.__version__}")
    print(f"psycopg: {psycopg.__version__}")
    print(f"nba_api endpoint import: {leaguegamelog.__name__}")
    print("Environment setup: OK")


if __name__ == "__main__":
    main()