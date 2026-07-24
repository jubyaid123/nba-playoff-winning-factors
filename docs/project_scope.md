# Project Scope

## Working Title

Winning the 2026 NBA Playoffs: A League-Wide Analysis with the New York Knicks as a Case Study

## Primary Analytical Question

Which game-level performance differences were most strongly associated with winning during the 2026 NBA Playoffs, and how did the New York Knicks perform in those areas during their playoff run?

## Intended Audience

The project is designed for a basketball operations, coaching, strategy, or analytics audience that wants an understandable explanation of the statistical differences between playoff wins and losses.

The final presentation must also be understandable to recruiters and hiring managers without advanced basketball knowledge.

## Population

All games in the 2026 NBA Playoffs from the first round through the NBA Finals.

Play-In Tournament games are excluded.

## Unit of Analysis

The main analytical table will contain one row for one team in one playoff game.

Each game should therefore produce exactly two team-game records.

## Outcome

The main outcome is whether the team won or lost the game.

## Required Analytical Questions

1. Which selected team metrics differed most between winners and losers?
2. How large and consistent were those differences?
3. How did the Knicks rank among all 2026 playoff teams in those metrics?
4. How did the Knicks perform differently in wins and losses?
5. How did the Knicks' metric profile change across playoff series?
6. What evidence-based observations and recommendations can be communicated to a nontechnical basketball audience?

## Planned Core Metrics

1. Effective field-goal percentage
2. Turnover rate
3. Offensive-rebound percentage
4. Free-throw rate
5. Three-point-attempt rate
6. Assist-to-turnover ratio

Every metric must eventually have one documented formula used consistently in SQL, Python, and Tableau.

## Required Data

* Game ID
* Game date
* Playoff round
* Series and game number
* Team ID and team name
* Opponent team
* Home or away status
* Win or loss
* Traditional team box-score statistics

## Required Deliverables

* Reproducible collection script
* Unmodified local raw-data snapshot
* PostgreSQL database
* Data dictionary
* Validation report
* SQL analytical views and queries
* Exploratory-analysis notebook
* Statistical-analysis notebook
* Knicks case-study notebook
* Final charts
* Three-page Tableau dashboard
* Executive summary
* Six-to-eight-slide presentation
* Polished GitHub README

## Required Quality Standards

* Every game has exactly two team-game records.
* Primary keys are unique.
* Winners match official final scores.
* Made shots do not exceed attempted shots.
* Missing values are investigated before being replaced.
* SQL and Python metric calculations agree.
* Tableau values reconcile with SQL results.
* Conclusions use association language rather than causal language.
* No analytical result is written before it has been calculated and checked.

## Out of Scope for the Core Project

* Play-In Tournament analysis
* Player-level analysis
* Lineup analysis
* Play-by-play analysis
* Possession reconstruction
* Predictive modeling
* Real-time data
* Cloud deployment
* Streamlit
* dbt
* Spark
* Kafka
* Betting or gambling analysis

These items may not be started until the required project is complete.

## Definition of Project Success

The project is successful when:

1. Another analyst can understand and reproduce the workflow.
2. The database and Tableau dashboard contain validated playoff data.
3. The main question is answered using SQL, Python, and appropriate statistics.
4. The Knicks are compared with the complete playoff field rather than analyzed in isolation.
5. Findings and limitations are communicated clearly.
6. The project can be explained confidently in a Data Analyst interview.

## Data Attribution

The planned primary source is NBA.com.

Any public use of NBA statistics will include appropriate NBA.com attribution.

This project is independent, educational, and noncommercial.
