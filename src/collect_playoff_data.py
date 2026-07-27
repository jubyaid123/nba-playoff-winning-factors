"""Collect 2026 NBA playoff team-game data."""

from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import leaguegamelog


SEASON = "2025-26"
SEASON_TYPE = "Playoffs"
REQUIRED_COLUMNS = {
    "TEAM_ID",
    "TEAM_ABBREVIATION",
    "TEAM_NAME",
    "GAME_ID",
    "GAME_DATE",
    "MATCHUP",
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
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "league_game_log_2026_playoffs.csv"


def fetch_playoff_data() -> pd.DataFrame:
    """Fetch team-game records for the 2026 NBA Playoffs."""
    playoff_log = leaguegamelog.LeagueGameLog(
        season=SEASON,
        season_type_all_star=SEASON_TYPE,
    )

    return playoff_log.get_data_frames()[0]


def save_raw_data(games: pd.DataFrame) -> None:
    """Save the raw playoff data locally without modifying it."""
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    games.to_csv(
        RAW_DATA_PATH,
        index=False,
    )
    print(f"Raw data saved to: {RAW_DATA_PATH}")


def load_raw_data() -> pd.DataFrame:
    """Load the existing raw playoff dataset from disk."""
    return pd.read_csv(RAW_DATA_PATH)


def validate_playoff_data(games: pd.DataFrame) -> None:
    """Validate the basic structure of the playoff dataset."""

    # Make sure the dataset contains data.
    if games.empty:
        raise ValueError("Dataset is empty.")

    # Make sure all columns required for the project are available.
    missing_columns = REQUIRED_COLUMNS - set(games.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    # Calculate basic game-level structure.
    unique_games = games["GAME_ID"].nunique()
    rows_per_game = games.groupby("GAME_ID").size()
    teams_per_game = games.groupby("GAME_ID")["TEAM_ID"].nunique()

    # Every NBA game should have exactly two team-game rows.
    if not (rows_per_game == 2).all():
        raise ValueError(
            "At least one game does not have exactly two team rows."
        )

    # Those two rows must represent two different teams.
    if not (teams_per_game == 2).all():
        raise ValueError(
            "At least one game does not contain two different teams."
        )

    # A team should only appear once within the same game.
    duplicate_team_games = games.duplicated(
        subset=["GAME_ID", "TEAM_ID"]
    ).any()

    if duplicate_team_games:
        raise ValueError(
            "Duplicate team-game records were found."
        )

    # Every game should contain exactly one winner and one loser.
    wl_counts = (
        games.groupby(["GAME_ID", "WL"])
        .size()
        .unstack(fill_value=0)
    )

    if "W" not in wl_counts.columns or "L" not in wl_counts.columns:
        raise ValueError(
            "Win/loss values are missing."
        )

    if not ((wl_counts["W"] == 1) & (wl_counts["L"] == 1)).all():
        raise ValueError(
            "At least one game does not have exactly one winner and one loser."
        )

    # The winning team must have scored more points than the losing team.
    point_check = games.pivot(
        index="GAME_ID",
        columns="WL",
        values="PTS",
    )

    if not (point_check["W"] > point_check["L"]).all():
        raise ValueError(
            "At least one winning team did not score more points than the loser."
        )

    print("Validation passed.")
    print(
        f"Validated {unique_games} games and {len(games)} team-game rows."
    )

def main() -> None:
    """Run the collection workflow."""
    if RAW_DATA_PATH.exists():
        print("Raw data already exists. Loading cached file.")
        games = load_raw_data()
    else:
        print("Raw data not found. Fetching from NBA API.")
        games = fetch_playoff_data()
        save_raw_data(games)

    print(f"Rows available: {len(games)}")
    print(f"Unique games: {games['GAME_ID'].nunique()}")

    validate_playoff_data(games)



if __name__ == "__main__":
    main()