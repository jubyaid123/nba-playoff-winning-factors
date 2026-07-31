"""Run detailed data-quality checks on NBA playoff data."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "league_game_log_2026_playoffs.csv"


def load_raw_data() -> pd.DataFrame:
    """Load the cached playoff dataset with stable data types."""
    return pd.read_csv(
        RAW_DATA_PATH,
        dtype={
            "GAME_ID": "string",
        },
    )

def validate_shooting_totals(games: pd.DataFrame) -> None:
    """Verify that made shots do not exceed attempted shots."""
    invalid_checks = {
        "FGM greater than FGA": games["FGM"] > games["FGA"],
        "FG3M greater than FG3A": games["FG3M"] > games["FG3A"],
        "FTM greater than FTA": games["FTM"] > games["FTA"],
    }

    errors_found = False

    for message, invalid_rows in invalid_checks.items():
        invalid_count = invalid_rows.sum()

        if invalid_count > 0:
            errors_found = True
            print(f"{message}: {invalid_count} invalid rows")

    if errors_found:
        raise ValueError("Invalid shooting totals were found.")

    print("Shooting-total validation passed.")

def validate_box_score_consistency(games: pd.DataFrame) -> None:
    """Verify that related box-score statistics agree with each other."""
    invalid_checks = {
        "REB does not equal OREB + DREB": (
            games["REB"] != games["OREB"] + games["DREB"]
        ),
        "FG3M greater than total FGM": (
            games["FG3M"] > games["FGM"]
        ),
    }

    errors_found = False

    for message, invalid_rows in invalid_checks.items():
        invalid_count = invalid_rows.sum()

        if invalid_count > 0:
            errors_found = True
            print(f"{message}: {invalid_count} invalid rows")

    if errors_found:
        raise ValueError(
            "Inconsistent box-score statistics were found."
        )

    print("Box-score consistency validation passed.")

def validate_percentage_consistency(
    games: pd.DataFrame,
    tolerance: float = 0.001,
) -> None:
    """Verify reported shooting percentages match made and attempted totals."""

    calculated_fg_pct = games["FGM"] / games["FGA"]
    calculated_fg3_pct = games["FG3M"] / games["FG3A"]
    calculated_ft_pct = games["FTM"] / games["FTA"]

    invalid_checks = {
        "FG_PCT does not match FGM / FGA": (
            (games["FG_PCT"] - calculated_fg_pct).abs() > tolerance
        ),
        "FG3_PCT does not match FG3M / FG3A": (
            (games["FG3_PCT"] - calculated_fg3_pct).abs() > tolerance
        ),
        "FT_PCT does not match FTM / FTA": (
            (games["FT_PCT"] - calculated_ft_pct).abs() > tolerance
        ),
    }

    errors_found = False

    for message, invalid_rows in invalid_checks.items():
        invalid_count = invalid_rows.fillna(False).sum()

        if invalid_count > 0:
            errors_found = True
            print(f"{message}: {invalid_count} invalid rows")

    if errors_found:
        raise ValueError(
            "Inconsistent shooting percentages were found."
        )

    print("Percentage consistency validation passed.")


def validate_points_consistency(games: pd.DataFrame) -> None:
    """Verify that reported points match made field goals and free throws."""
    calculated_points = (
        2 * (games["FGM"] - games["FG3M"])
        + 3 * games["FG3M"]
        + games["FTM"]
    )

    invalid_rows = games["PTS"] != calculated_points
    invalid_count = invalid_rows.sum()

    if invalid_count > 0:
        print(f"PTS does not match shooting totals: {invalid_count} invalid rows")
        raise ValueError("Inconsistent point totals were found.")

    print("Points consistency validation passed.")

def validate_paired_games(games: pd.DataFrame) -> None:
    """Verify that opponent rows agree within each game."""
    plus_minus_sum = games.groupby("GAME_ID")["PLUS_MINUS"].sum()

    invalid_plus_minus = plus_minus_sum != 0
    invalid_count = invalid_plus_minus.sum()

    if invalid_count > 0:
        print(
            "Opponent PLUS_MINUS values do not sum to zero: "
            f"{invalid_count} invalid games"
        )
        raise ValueError("Inconsistent paired-game values were found.")

    print("Paired-game validation passed.")


def validate_matchup_format(games: pd.DataFrame) -> None:
    """Verify that matchup strings identify home or away status."""
    valid_matchups = (
        games["MATCHUP"].str.contains(" vs. ", regex=False)
        | games["MATCHUP"].str.contains(" @ ", regex=False)
    )

    invalid_count = (~valid_matchups).sum()

    if invalid_count > 0:
        print(f"Invalid MATCHUP format: {invalid_count} rows")
        raise ValueError("Invalid matchup values were found.")

    print("Matchup-format validation passed.")


def validate_home_away_structure(games: pd.DataFrame) -> None:
    """Verify that every game contains one home team and one away team."""
    home_away = games[["GAME_ID", "MATCHUP"]].copy()

    home_away["location"] = home_away["MATCHUP"].apply(
        lambda matchup: "home" if " vs. " in matchup else "away"
    )

    location_counts = (
        home_away.groupby(["GAME_ID", "location"])
        .size()
        .unstack(fill_value=0)
    )

    if "home" not in location_counts.columns:
        raise ValueError("No home-team records were found.")

    if "away" not in location_counts.columns:
        raise ValueError("No away-team records were found.")

    valid_structure = (
        (location_counts["home"] == 1)
        & (location_counts["away"] == 1)
    )

    invalid_count = (~valid_structure).sum()

    if invalid_count > 0:
        print(
            "Games without exactly one home and one away team: "
            f"{invalid_count}"
        )
        raise ValueError("Invalid home/away structure was found.")

    print("Home/away structure validation passed.")

def validate_nonnegative_stats(games: pd.DataFrame) -> None:
    """Verify that counting statistics do not contain negative values."""
    nonnegative_columns = [
        "FGM",
        "FGA",
        "FG3M",
        "FG3A",
        "FTM",
        "FTA",
        "OREB",
        "DREB",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TOV",
        "PF",
        "PTS",
    ]

    invalid_counts = (games[nonnegative_columns] < 0).sum()
    invalid_counts = invalid_counts[invalid_counts > 0]

    if not invalid_counts.empty:
        print("\nNegative values found:")
        print(invalid_counts)
        raise ValueError("Negative counting statistics were found.")

    print("Nonnegative-stat validation passed.")




def main() -> None:
    """Load the dataset and summarize missing values."""
    games = load_raw_data()

    print(f"Rows: {len(games)}")
    print(f"Columns: {len(games.columns)}")

    missing_values = games.isna().sum()
    missing_values = missing_values[missing_values > 0]

    if missing_values.empty:
        print("No missing values found.")
    else:
        print("\nMissing values by column:")
        print(missing_values)

    
    validate_shooting_totals(games)
    validate_box_score_consistency(games)
    validate_percentage_consistency(games)
    validate_points_consistency(games)
    validate_paired_games(games)
    validate_matchup_format(games)
    validate_home_away_structure(games)
    validate_nonnegative_stats(games)

if __name__ == "__main__":
    main()