-- ============================================================
-- ANALYTICAL VIEWS
-- Creates reusable views for opponent matching, calculated
-- metrics, opponent-relative differentials, and winner summaries.
-- ============================================================


-- ------------------------------------------------------------
-- View 1: Match each team-game row with its opponent.
-- One row still represents one team in one game.
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_team_game_opponent AS
SELECT
team_game.game_id,
game.game_date,

team_game.team_id,
team.team_abbreviation,
team.team_name,

opponent_game.team_id AS opponent_team_id,
opponent.team_abbreviation AS opponent_abbreviation,
opponent.team_name AS opponent_name,

team_game.wl,
team_game.pts,
opponent_game.pts AS opponent_pts,
team_game.plus_minus,

team_game.fgm,
team_game.fga,
team_game.fg3m,
team_game.fg3a,
team_game.ftm,
team_game.fta,
team_game.oreb,
team_game.dreb,
team_game.ast,
team_game.tov,

opponent_game.fgm AS opponent_fgm,
opponent_game.fga AS opponent_fga,
opponent_game.fg3m AS opponent_fg3m,
opponent_game.fg3a AS opponent_fg3a,
opponent_game.ftm AS opponent_ftm,
opponent_game.fta AS opponent_fta,
opponent_game.oreb AS opponent_oreb,
opponent_game.dreb AS opponent_dreb,
opponent_game.ast AS opponent_ast,
opponent_game.tov AS opponent_tov

FROM fact_team_game AS team_game

JOIN fact_team_game AS opponent_game
ON team_game.game_id = opponent_game.game_id
AND team_game.team_id <> opponent_game.team_id

JOIN dim_team AS team
ON team_game.team_id = team.team_id

JOIN dim_team AS opponent
ON opponent_game.team_id = opponent.team_id

JOIN dim_game AS game
ON team_game.game_id = game.game_id;


-- ------------------------------------------------------------
-- View 2: Calculate team and opponent metrics for each game.
-- Metrics include eFG%, turnover rate, offensive rebound
-- percentage, free-throw rate, three-point attempt rate,
-- and assist-to-turnover ratio.
-- NULLIF prevents division-by-zero errors.
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_team_game_metrics AS
SELECT
game_id,
game_date,
team_id,
team_abbreviation,
team_name,
opponent_team_id,
opponent_abbreviation,
opponent_name,
wl,
pts,
opponent_pts,
plus_minus,

(fgm + 0.5 * fg3m) / NULLIF(fga, 0)::numeric
    AS efg_pct,

tov / NULLIF(fga + 0.44 * fta + tov, 0)::numeric
    AS tov_rate,

oreb / NULLIF(oreb + opponent_dreb, 0)::numeric
    AS oreb_pct,

fta / NULLIF(fga, 0)::numeric
    AS ft_rate,

fg3a / NULLIF(fga, 0)::numeric
    AS fg3_attempt_rate,

ast / NULLIF(tov, 0)::numeric
    AS ast_to_tov_ratio,

(opponent_fgm + 0.5 * opponent_fg3m)
    / NULLIF(opponent_fga, 0)::numeric
    AS opponent_efg_pct,

opponent_tov
    / NULLIF(
        opponent_fga + 0.44 * opponent_fta + opponent_tov,
        0
    )::numeric
    AS opponent_tov_rate,

opponent_oreb
    / NULLIF(opponent_oreb + dreb, 0)::numeric
    AS opponent_oreb_pct,

opponent_fta / NULLIF(opponent_fga, 0)::numeric
    AS opponent_ft_rate,

opponent_fg3a / NULLIF(opponent_fga, 0)::numeric
    AS opponent_fg3_attempt_rate,

opponent_ast / NULLIF(opponent_tov, 0)::numeric
    AS opponent_ast_to_tov_ratio

FROM v_team_game_opponent;


-- ------------------------------------------------------------
-- View 3: Calculate opponent-relative metric differentials.
-- Positive values generally mean the team performed better
-- than its opponent in that metric.
-- Turnover rate is reversed so a positive value means the team
-- had the lower (better) turnover rate.
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_team_game_differentials AS
SELECT
*,

efg_pct - opponent_efg_pct
    AS efg_diff,

opponent_tov_rate - tov_rate
    AS tov_rate_advantage,

oreb_pct - opponent_oreb_pct
    AS oreb_pct_diff,

ft_rate - opponent_ft_rate
    AS ft_rate_diff,

fg3_attempt_rate - opponent_fg3_attempt_rate
    AS fg3_attempt_rate_diff,

ast_to_tov_ratio - opponent_ast_to_tov_ratio
    AS ast_to_tov_ratio_diff

FROM v_team_game_metrics;


-- ------------------------------------------------------------
-- View 4: Summarize the average winner-side metric advantages
-- and how often the winner held a positive advantage in each
-- metric across all playoff games.
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_winner_metric_summary AS
SELECT
COUNT(*) AS games,

AVG(efg_diff) AS avg_efg_diff,
AVG(tov_rate_advantage) AS avg_tov_rate_advantage,
AVG(oreb_pct_diff) AS avg_oreb_pct_diff,
AVG(ft_rate_diff) AS avg_ft_rate_diff,
AVG(fg3_attempt_rate_diff) AS avg_fg3_attempt_rate_diff,
AVG(ast_to_tov_ratio_diff) AS avg_ast_to_tov_ratio_diff,

AVG(CASE WHEN efg_diff > 0 THEN 1.0 ELSE 0.0 END)
    AS pct_with_efg_advantage,

AVG(CASE WHEN tov_rate_advantage > 0 THEN 1.0 ELSE 0.0 END)
    AS pct_with_tov_advantage,

AVG(CASE WHEN oreb_pct_diff > 0 THEN 1.0 ELSE 0.0 END)
    AS pct_with_oreb_advantage,

AVG(CASE WHEN ft_rate_diff > 0 THEN 1.0 ELSE 0.0 END)
    AS pct_with_ft_rate_advantage,

AVG(CASE WHEN fg3_attempt_rate_diff > 0 THEN 1.0 ELSE 0.0 END)
    AS pct_with_fg3_attempt_advantage,

AVG(CASE WHEN ast_to_tov_ratio_diff > 0 THEN 1.0 ELSE 0.0 END)
    AS pct_with_ast_tov_advantage

FROM v_team_game_differentials
WHERE wl = 'W';