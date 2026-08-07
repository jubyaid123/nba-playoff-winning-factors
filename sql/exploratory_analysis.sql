-- ============================================================
-- EXPLORATORY ANALYSIS
-- League-wide winner/loser analysis, team comparisons,
-- Knicks case-study queries, and a final symmetry check.
-- ============================================================


-- ------------------------------------------------------------
-- Analysis 1: Compare average metric differentials between
-- winning and losing teams across the full playoff dataset.
-- ------------------------------------------------------------
SELECT
wl,

ROUND(AVG(efg_diff), 4) AS avg_efg_diff,
ROUND(AVG(tov_rate_advantage), 4) AS avg_tov_rate_advantage,
ROUND(AVG(oreb_pct_diff), 4) AS avg_oreb_pct_diff,
ROUND(AVG(ft_rate_diff), 4) AS avg_ft_rate_diff,
ROUND(AVG(fg3_attempt_rate_diff), 4) AS avg_fg3_attempt_rate_diff,
ROUND(AVG(ast_to_tov_ratio_diff), 4) AS avg_ast_to_tov_ratio_diff

FROM v_team_game_differentials
GROUP BY wl
ORDER BY wl DESC;


-- ------------------------------------------------------------
-- Analysis 2: Calculate how often winners held a positive
-- advantage in each metric across the 85 playoff games.
-- ------------------------------------------------------------
SELECT
ROUND(
100.0 * AVG(
CASE WHEN efg_diff > 0 THEN 1 ELSE 0 END
),
1
) AS pct_winners_with_efg_advantage,

ROUND(
    100.0 * AVG(
        CASE WHEN tov_rate_advantage > 0 THEN 1 ELSE 0 END
    ),
    1
) AS pct_winners_with_tov_advantage,

ROUND(
    100.0 * AVG(
        CASE WHEN oreb_pct_diff > 0 THEN 1 ELSE 0 END
    ),
    1
) AS pct_winners_with_oreb_advantage,

ROUND(
    100.0 * AVG(
        CASE WHEN ft_rate_diff > 0 THEN 1 ELSE 0 END
    ),
    1
) AS pct_winners_with_ft_rate_advantage,

ROUND(
    100.0 * AVG(
        CASE WHEN fg3_attempt_rate_diff > 0 THEN 1 ELSE 0 END
    ),
    1
) AS pct_winners_with_fg3_attempt_advantage,

ROUND(
    100.0 * AVG(
        CASE WHEN ast_to_tov_ratio_diff > 0 THEN 1 ELSE 0 END
    ),
    1
) AS pct_winners_with_ast_tov_advantage

FROM v_team_game_differentials
WHERE wl = 'W';


-- ------------------------------------------------------------
-- Analysis 3: Compare average playoff performance by team.
-- ------------------------------------------------------------
SELECT
team_abbreviation,
COUNT(*) AS games_played,
SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) AS wins,

ROUND(AVG(efg_diff), 4) AS avg_efg_diff,
ROUND(AVG(tov_rate_advantage), 4) AS avg_tov_rate_advantage,
ROUND(AVG(oreb_pct_diff), 4) AS avg_oreb_pct_diff,
ROUND(AVG(ft_rate_diff), 4) AS avg_ft_rate_diff,
ROUND(AVG(ast_to_tov_ratio_diff), 4) AS avg_ast_to_tov_ratio_diff

FROM v_team_game_differentials
GROUP BY team_abbreviation
ORDER BY wins DESC, avg_efg_diff DESC;


-- ------------------------------------------------------------
-- Analysis 4: Rank all playoff teams by each average metric.
-- ------------------------------------------------------------
WITH team_averages AS (
SELECT
team_abbreviation,
COUNT(*) AS games_played,
SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) AS wins,
ROUND(AVG(efg_diff), 4) AS avg_efg_diff,
ROUND(AVG(tov_rate_advantage), 4) AS avg_tov_rate_advantage,
ROUND(AVG(oreb_pct_diff), 4) AS avg_oreb_pct_diff,
ROUND(AVG(ft_rate_diff), 4) AS avg_ft_rate_diff,
ROUND(AVG(ast_to_tov_ratio_diff), 4) AS avg_ast_to_tov_ratio_diff
FROM v_team_game_differentials
GROUP BY team_abbreviation
)

SELECT
team_abbreviation,
games_played,
wins,

avg_efg_diff,
RANK() OVER (
    ORDER BY avg_efg_diff DESC
) AS efg_rank,

avg_tov_rate_advantage,
RANK() OVER (
    ORDER BY avg_tov_rate_advantage DESC
) AS tov_rank,

avg_oreb_pct_diff,
RANK() OVER (
    ORDER BY avg_oreb_pct_diff DESC
) AS oreb_rank,

avg_ft_rate_diff,
RANK() OVER (
    ORDER BY avg_ft_rate_diff DESC
) AS ft_rate_rank,

avg_ast_to_tov_ratio_diff,
RANK() OVER (
    ORDER BY avg_ast_to_tov_ratio_diff DESC
) AS ast_tov_rank

FROM team_averages
ORDER BY wins DESC, team_abbreviation;


-- ------------------------------------------------------------
-- Analysis 5: Compare Knicks wins versus Knicks losses.
-- ------------------------------------------------------------
SELECT
wl,
COUNT(*) AS games,

ROUND(AVG(efg_diff), 4) AS avg_efg_diff,
ROUND(AVG(tov_rate_advantage), 4) AS avg_tov_rate_advantage,
ROUND(AVG(oreb_pct_diff), 4) AS avg_oreb_pct_diff,
ROUND(AVG(ft_rate_diff), 4) AS avg_ft_rate_diff,
ROUND(AVG(fg3_attempt_rate_diff), 4) AS avg_fg3_attempt_rate_diff,
ROUND(AVG(ast_to_tov_ratio_diff), 4) AS avg_ast_to_tov_ratio_diff

FROM v_team_game_differentials
WHERE team_abbreviation = 'NYK'
GROUP BY wl
ORDER BY wl DESC;


-- ------------------------------------------------------------
-- Analysis 6: Inspect each Knicks playoff loss individually.
-- ------------------------------------------------------------
SELECT
game_date,
opponent_abbreviation,
pts,
opponent_pts,
plus_minus,

ROUND(efg_diff, 4) AS efg_diff,
ROUND(tov_rate_advantage, 4) AS tov_rate_advantage,
ROUND(oreb_pct_diff, 4) AS oreb_pct_diff,
ROUND(ft_rate_diff, 4) AS ft_rate_diff,
ROUND(fg3_attempt_rate_diff, 4) AS fg3_attempt_rate_diff,
ROUND(ast_to_tov_ratio_diff, 4) AS ast_to_tov_ratio_diff

FROM v_team_game_differentials
WHERE team_abbreviation = 'NYK'
AND wl = 'L'
ORDER BY game_date;


-- ------------------------------------------------------------
-- Validation: Confirm differential symmetry.
-- Each team's differential should be the exact opposite of its
-- opponent's differential within the same game.
-- Expected result: invalid_games = 0.
-- ------------------------------------------------------------
SELECT
COUNT(*) AS invalid_games
FROM (
SELECT
game_id,
SUM(efg_diff) AS efg_diff_sum,
SUM(tov_rate_advantage) AS tov_advantage_sum,
SUM(oreb_pct_diff) AS oreb_diff_sum,
SUM(ft_rate_diff) AS ft_rate_diff_sum,
SUM(fg3_attempt_rate_diff) AS fg3_attempt_diff_sum,
SUM(ast_to_tov_ratio_diff) AS ast_tov_diff_sum
FROM v_team_game_differentials
GROUP BY game_id
) AS game_checks
WHERE
ABS(efg_diff_sum) > 0.000001
OR ABS(tov_advantage_sum) > 0.000001
OR ABS(oreb_diff_sum) > 0.000001
OR ABS(ft_rate_diff_sum) > 0.000001
OR ABS(fg3_attempt_diff_sum) > 0.000001
OR ABS(ast_tov_diff_sum) > 0.000001;