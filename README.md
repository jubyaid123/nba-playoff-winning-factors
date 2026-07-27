# Winning the 2026 NBA Playoffs

## Analytical Question

Which game-level performance differences were most strongly associated with winning during the 2026 NBA Playoffs, and how did the New York Knicks perform in those areas during their playoff run?

## Project Objective

This project will analyze all NBA playoff games from the first round through the NBA Finals.

The analysis will compare winning and losing teams across a focused set of team-performance metrics, then use the New York Knicks as a case study to understand how their performance compared with the rest of the playoff field.

The goal is to demonstrate practical skills expected in entry-level Data Analyst and BI Analyst roles, including SQL, Python, Pandas, PostgreSQL, data cleaning, validation, statistical analysis, visualization, Tableau, Git, GitHub, and stakeholder communication.

## Core Scope

* Season: 2025–26
* Competition: 2026 NBA Playoffs
* Games: First round through NBA Finals
* Play-In Tournament: Excluded
* Main unit of analysis: One team in one playoff game
* League-wide comparison: Winners versus losers
* Case study: New York Knicks
* Primary data level: Team box scores

## Planned Core Metrics

* Effective field-goal percentage
* Turnover rate
* Offensive-rebound percentage
* Free-throw rate
* Three-point-attempt rate
* Assist-to-turnover ratio

Metric definitions may be refined after the source data is evaluated.

## Planned Deliverables

* Python data-collection scripts
* Data-cleaning and validation workflow
* PostgreSQL relational database
* SQL analysis
* Python and Pandas exploratory analysis
* Basic statistical analysis
* Knicks case study
* Tableau dashboard
* Executive summary
* Short presentation
* Technical documentation

## Planned Tools

* Python
* Pandas
* Jupyter
* PostgreSQL
* SQL
* Matplotlib
* Tableau Public
* Git
* GitHub

## Data Source

The planned primary data source is NBA.com, accessed through NBA statistics endpoints using the community-maintained `nba_api` Python package.

The 2026 playoff LeagueGameLog source was successfully validated with 170 team-game records representing 85 playoff games.

This is an independent, noncommercial educational project and is not affiliated with or endorsed by the National Basketball Association.

Raw NBA data will not be republished as a comprehensive public database.

## Repository Structure

* `data/` — raw, intermediate, and processed project data
* `docs/` — project scope, methodology, data dictionary, and limitations
* `notebooks/` — exploratory and statistical analysis
* `src/` — reusable Python scripts
* `sql/` — database schema and analytical SQL queries
* `dashboard/` — Tableau workbook and dashboard images
* `reports/` — executive summary, figures, and presentation
* `tests/` — automated validation and code tests

## Reproduction

Detailed reproduction instructions will be added after the data source and collection method are confirmed in Sprint 1.
