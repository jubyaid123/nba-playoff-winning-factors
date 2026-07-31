# Data Validation Report

## Dataset

2026 NBA Playoffs team-game dataset.

## Dataset Size

* 170 team-game rows
* 85 unique playoff games
* 29 source columns
* 16 playoff teams

## Validation Status

All implemented data-quality checks passed.

## Structural Checks

* Every game contains exactly two team-game rows.
* Every game contains two different teams.
* Every game contains exactly one winner and one loser.
* No duplicate game-team records were found.
* The winning team scored more points than the losing team.
* Every fact-table record links to a valid team.
* Every fact-table record links to a valid game.

## Missing-Value Check

No missing values were found in the source dataset.

No values were replaced, imputed, or removed.

## Shooting Checks

The following rules were validated across all 170 team-game rows:

* Field goals made do not exceed field goals attempted.
* Three-point field goals made do not exceed three-point field goals attempted.
* Free throws made do not exceed free throws attempted.
* Three-point field goals made do not exceed total field goals made.
* Reported shooting percentages agree with made and attempted totals within a rounding tolerance of 0.001.

## Box-Score Consistency Checks

* Total rebounds equal offensive rebounds plus defensive rebounds.
* Reported points match the points calculated from two-point field goals, three-point field goals, and free throws.
* Opposing plus-minus values sum to zero within every game.
* Counting statistics do not contain invalid negative values.

`PLUS_MINUS` was excluded from the nonnegative-value check because negative values are valid for teams that were outscored.

## Matchup Checks

* Every matchup contains either `vs.` or `@`.
* Every game contains exactly one home-team record.
* Every game contains exactly one away-team record.

## Sample Manual Validation

Game ID `0042500121`, Atlanta Hawks at New York Knicks on April 18, 2026, was manually checked.

The dataset recorded:

* New York Knicks: win, 113 points, plus-minus of 11
* Atlanta Hawks: loss, 102 points, plus-minus of -11

The values matched the official result used during the source audit.

## Conclusion

The dataset passed all implemented structural, completeness, scoring, shooting, matchup, and relational-integrity checks.

No records were removed or modified as a result of validation.

The data is suitable for transformation, metric engineering, SQL analysis, and exploratory analysis.

These checks establish internal consistency but do not prove that every source value is free from upstream reporting errors. The project therefore retains source attribution and documents its validation limitations.
