# Source Audit

## Primary Source

NBA.com statistics accessed through the community-maintained `nba_api` Python package.

## Endpoint Tested

`LeagueGameLog`

Season:

`2025-26`

Season type:

`Playoffs`

## Purpose

The purpose of this source audit was to confirm that the selected NBA data source provides the team-level game statistics required for the core project.

## Results

The endpoint returned:

* 170 team-game rows
* 85 unique playoff games
* 29 columns
* Exactly two team-game rows per game
* Exactly one winning team and one losing team per game

## Important Available Fields

The endpoint includes the fields required for the planned core analysis:

* Game ID
* Game date
* Team ID
* Team abbreviation
* Team name
* Matchup
* Win/loss result
* Field goals made and attempted
* Three-point field goals made and attempted
* Free throws made and attempted
* Offensive and defensive rebounds
* Assists
* Turnovers
* Points
* Plus-minus

## Sample Validation

New York Knicks vs. Atlanta Hawks on April 18, 2026 was used as a test game.

Game ID:

`0042500121`

The API returned exactly two team-game rows for the game.

The Knicks were identified as the winner with 113 points.

The Hawks were identified as the loser with 102 points.

The result matched the official NBA game result.

## Validation Checks

The following checks were performed:

1. Every game ID appeared exactly twice.
2. Every game contained exactly one winner.
3. Every game contained exactly one loser.
4. The raw dataset contained 170 team-game rows for 85 unique games.
5. The saved local CSV had the same shape as the original API DataFrame.

## Core Metric Availability

The current source provides enough information to calculate:

* Effective field-goal percentage
* Turnover rate
* Offensive-rebound percentage
* Free-throw rate
* Three-point-attempt rate
* Assist-to-turnover ratio

Offensive-rebound percentage will require combining each team row with the opponent's defensive rebounds from the same game.

## Source Decision

`LeagueGameLog` is sufficient as the primary source for the required team-level core project.

Additional player, lineup, play-by-play, or advanced box-score endpoints are not required for the current project scope.

## Limitations

* `nba_api` is a community-maintained wrapper rather than an official NBA-supported Python SDK.
* NBA endpoints may change or occasionally fail.
* Raw responses should therefore be cached locally.
* The project should not depend on repeatedly downloading the same historical data.
* Data should be validated before analysis rather than assumed to be correct.
