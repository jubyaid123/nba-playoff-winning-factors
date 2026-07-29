CREATE TABLE dim_team (
    team_id BIGINT PRIMARY KEY,
    team_abbreviation VARCHAR(3) NOT NULL,
    team_name VARCHAR(100) NOT NULL
);

CREATE TABLE dim_game (
    game_id VARCHAR(20) PRIMARY KEY,
    game_date DATE NOT NULL
);

CREATE TABLE fact_team_game (
    game_id VARCHAR(20) NOT NULL,
    team_id BIGINT NOT NULL,
    wl CHAR(1) NOT NULL,
    fgm INTEGER NOT NULL,
    fga INTEGER NOT NULL,
    fg3m INTEGER NOT NULL,
    fg3a INTEGER NOT NULL,
    ftm INTEGER NOT NULL,
    fta INTEGER NOT NULL,
    oreb INTEGER NOT NULL,
    dreb INTEGER NOT NULL,
    ast INTEGER NOT NULL,
    tov INTEGER NOT NULL,
    pts INTEGER NOT NULL,
    plus_minus INTEGER,

    PRIMARY KEY (game_id, team_id),

    FOREIGN KEY (game_id)
        REFERENCES dim_game(game_id),

    FOREIGN KEY (team_id)
        REFERENCES dim_team(team_id)
);