
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    team_id INTEGER,
    playing_role TEXT,
    batting_style TEXT,
    bowling_style TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT NOT NULL,
    city TEXT,
    country TEXT,
    capacity INTEGER CHECK (capacity IS NULL OR capacity >= 0)
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_description TEXT NOT NULL,
    match_format TEXT,
    match_date TEXT,
    team1_id INTEGER,
    team2_id INTEGER,
    venue_id INTEGER,
    match_status TEXT DEFAULT 'Scheduled',
    toss_winner_id INTEGER,
    toss_decision TEXT,
    winner_id INTEGER,
    victory_margin INTEGER,
    victory_type TEXT,
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS player_match_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    innings_number INTEGER DEFAULT 1,
    runs_scored INTEGER DEFAULT 0,
    balls_faced INTEGER DEFAULT 0,
    fours INTEGER DEFAULT 0,
    sixes INTEGER DEFAULT 0,
    wickets_taken INTEGER DEFAULT 0,
    runs_conceded INTEGER DEFAULT 0,
    overs_bowled REAL DEFAULT 0,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    batting_position INTEGER,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE (match_id, player_id, innings_number)
);

CREATE INDEX IF NOT EXISTS idx_players_team
ON players(team_id);

CREATE INDEX IF NOT EXISTS idx_matches_date
ON matches(match_date);

CREATE INDEX IF NOT EXISTS idx_matches_format
ON matches(match_format);

CREATE INDEX IF NOT EXISTS idx_stats_match
ON player_match_stats(match_id);

CREATE INDEX IF NOT EXISTS idx_stats_player
ON player_match_stats(player_id);
