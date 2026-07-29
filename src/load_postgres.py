"""Load validated NBA playoff data into PostgreSQL."""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "league_game_log_2026_playoffs.csv"

DATABASE_URL = "postgresql+psycopg://localhost/nba_playoffs_2026"


def load_raw_data() -> pd.DataFrame:
    """Load the cached playoff dataset."""
    return pd.read_csv(
        RAW_DATA_PATH,
        dtype={
            "GAME_ID": "string",
        },
    )


def build_dim_team(games: pd.DataFrame) -> pd.DataFrame:
    """Create one unique row per playoff team."""
    dim_team = (
        games[
            [
                "TEAM_ID",
                "TEAM_ABBREVIATION",
                "TEAM_NAME",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "TEAM_ID": "team_id",
                "TEAM_ABBREVIATION": "team_abbreviation",
                "TEAM_NAME": "team_name",
            }
        )
        .sort_values("team_id")
        .reset_index(drop=True)
    )

    return dim_team


def build_dim_game(games: pd.DataFrame) -> pd.DataFrame:
    """Create one unique row per playoff game."""
    dim_game = (
        games[
            [
                "GAME_ID",
                "GAME_DATE",
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "GAME_ID": "game_id",
                "GAME_DATE": "game_date",
            }
        )
        .sort_values("game_date")
        .reset_index(drop=True)
    )

    dim_game["game_date"] = pd.to_datetime(
        dim_game["game_date"]
    ).dt.date

    return dim_game

def build_fact_team_game(games: pd.DataFrame) -> pd.DataFrame:
    """Create one row per team in each playoff game."""
    fact_team_game = (
        games[
            [
                "GAME_ID",
                "TEAM_ID",
                "WL",
                "FGM",
                "FGA",
                "FG3M",
                "FG3A",
                "FTM",
                "FTA",
                "OREB",
                "DREB",
                "AST",
                "TOV",
                "PTS",
                "PLUS_MINUS",
            ]
        ]
        .rename(
            columns={
                "GAME_ID": "game_id",
                "TEAM_ID": "team_id",
                "WL": "wl",
                "FGM": "fgm",
                "FGA": "fga",
                "FG3M": "fg3m",
                "FG3A": "fg3a",
                "FTM": "ftm",
                "FTA": "fta",
                "OREB": "oreb",
                "DREB": "dreb",
                "AST": "ast",
                "TOV": "tov",
                "PTS": "pts",
                "PLUS_MINUS": "plus_minus",
            }
        )
        .reset_index(drop=True)
    )

    return fact_team_game


def load_tables(
    engine,
    dim_team: pd.DataFrame,
    dim_game: pd.DataFrame,
    fact_team_game: pd.DataFrame,
) -> None:
    """Load dimension and fact tables into PostgreSQL."""

    with engine.begin() as connection:
        dim_team.to_sql(
            "dim_team",
            connection,
            if_exists="append",
            index=False,
        )

        dim_game.to_sql(
            "dim_game",
            connection,
            if_exists="append",
            index=False,
        )

        fact_team_game.to_sql(
            "fact_team_game",
            connection,
            if_exists="append",
            index=False,
        )

    print("Database load complete.")


def main() -> None:
    """Build and load playoff tables into PostgreSQL."""
    games = load_raw_data()

    engine = create_engine(DATABASE_URL)

    print(f"Rows loaded from CSV: {len(games)}")

    with engine.connect():
        print("PostgreSQL connection successful.")

    dim_team = build_dim_team(games)
    dim_game = build_dim_game(games)
    fact_team_game = build_fact_team_game(games)

    load_tables(
    engine,
    dim_team,
    dim_game,
    fact_team_game,
    )




if __name__ == "__main__":
    main()