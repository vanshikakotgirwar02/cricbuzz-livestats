
PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO teams (team_name, country) VALUES
('India', 'India'),
('Australia', 'Australia'),
('England', 'England'),
('New Zealand', 'New Zealand'),
('South Africa', 'South Africa');

INSERT INTO players
    (full_name, team_id, playing_role, batting_style, bowling_style)
SELECT 'Virat Kohli', team_id, 'Batsman', 'Right-hand bat', 'Right-arm medium'
FROM teams WHERE team_name = 'India'
AND NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Virat Kohli');

INSERT INTO players
    (full_name, team_id, playing_role, batting_style, bowling_style)
SELECT 'Rohit Sharma', team_id, 'Batsman', 'Right-hand bat', 'Right-arm offbreak'
FROM teams WHERE team_name = 'India'
AND NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Rohit Sharma');

INSERT INTO players
    (full_name, team_id, playing_role, batting_style, bowling_style)
SELECT 'Jasprit Bumrah', team_id, 'Bowler', 'Right-hand bat', 'Right-arm fast'
FROM teams WHERE team_name = 'India'
AND NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Jasprit Bumrah');

INSERT INTO players
    (full_name, team_id, playing_role, batting_style, bowling_style)
SELECT 'Steve Smith', team_id, 'Batsman', 'Right-hand bat', 'Right-arm legbreak'
FROM teams WHERE team_name = 'Australia'
AND NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Steve Smith');

INSERT INTO players
    (full_name, team_id, playing_role, batting_style, bowling_style)
SELECT 'Pat Cummins', team_id, 'Bowler', 'Right-hand bat', 'Right-arm fast'
FROM teams WHERE team_name = 'Australia'
AND NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Pat Cummins');

INSERT OR IGNORE INTO venues (venue_name, city, country, capacity)
VALUES
('Wankhede Stadium', 'Mumbai', 'India', 33000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100000),
('Lord''s Cricket Ground', 'London', 'England', 30000);

INSERT INTO matches
    (match_description, match_format, match_date,
     team1_id, team2_id, venue_id, match_status,
     toss_winner_id, toss_decision, winner_id,
     victory_margin, victory_type)
SELECT
    'India vs Australia - Sample ODI',
    'ODI',
    '2026-10-10',
    india.team_id,
    aus.team_id,
    venue.venue_id,
    'Completed',
    india.team_id,
    'bat',
    india.team_id,
    25,
    'runs'
FROM teams india
JOIN teams aus ON aus.team_name = 'Australia'
JOIN venues venue ON venue.venue_name = 'Wankhede Stadium'
WHERE india.team_name = 'India'
AND NOT EXISTS (
    SELECT 1 FROM matches
    WHERE match_description = 'India vs Australia - Sample ODI'
);

INSERT INTO player_match_stats
    (match_id, player_id, innings_number, runs_scored,
     balls_faced, fours, sixes, wickets_taken,
     runs_conceded, overs_bowled, batting_position)
SELECT
    m.match_id, p.player_id, 1, 75, 60, 8, 2, 0, 0, 0, 3
FROM matches m
JOIN players p ON p.full_name = 'Virat Kohli'
WHERE m.match_description = 'India vs Australia - Sample ODI'
AND NOT EXISTS (
    SELECT 1 FROM player_match_stats s
    WHERE s.match_id = m.match_id
    AND s.player_id = p.player_id
    AND s.innings_number = 1
);

INSERT INTO player_match_stats
    (match_id, player_id, innings_number, runs_scored,
     balls_faced, fours, sixes, wickets_taken,
     runs_conceded, overs_bowled, batting_position)
SELECT
    m.match_id, p.player_id, 1, 40, 35, 4, 1, 0, 0, 0, 1
FROM matches m
JOIN players p ON p.full_name = 'Rohit Sharma'
WHERE m.match_description = 'India vs Australia - Sample ODI'
AND NOT EXISTS (
    SELECT 1 FROM player_match_stats s
    WHERE s.match_id = m.match_id
    AND s.player_id = p.player_id
    AND s.innings_number = 1
);

INSERT INTO player_match_stats
    (match_id, player_id, innings_number, runs_scored,
     balls_faced, fours, sixes, wickets_taken,
     runs_conceded, overs_bowled, batting_position)
SELECT
    m.match_id, p.player_id, 1, 10, 12, 1, 0, 3, 35, 10, 9
FROM matches m
JOIN players p ON p.full_name = 'Jasprit Bumrah'
WHERE m.match_description = 'India vs Australia - Sample ODI'
AND NOT EXISTS (
    SELECT 1 FROM player_match_stats s
    WHERE s.match_id = m.match_id
    AND s.player_id = p.player_id
    AND s.innings_number = 1
);


-- Additional sample matches for analytics filter testing

INSERT INTO matches
    (match_description, match_format, match_date,
     team1_id, team2_id, venue_id, match_status)
SELECT
    'England vs New Zealand - Sample T20',
    'T20',
    '2026-10-12',
    england.team_id,
    nz.team_id,
    venue.venue_id,
    'Completed'
FROM teams england
JOIN teams nz ON nz.team_name = 'New Zealand'
JOIN venues venue ON venue.venue_name = 'Lord''s Cricket Ground'
WHERE england.team_name = 'England'
AND NOT EXISTS (
    SELECT 1 FROM matches
    WHERE match_description = 'England vs New Zealand - Sample T20'
);

INSERT INTO matches
    (match_description, match_format, match_date,
     team1_id, team2_id, venue_id, match_status)
SELECT
    'South Africa vs Australia - Sample Test',
    'Test',
    '2026-10-14',
    sa.team_id,
    aus.team_id,
    venue.venue_id,
    'Completed'
FROM teams sa
JOIN teams aus ON aus.team_name = 'Australia'
JOIN venues venue ON venue.venue_name = 'Melbourne Cricket Ground'
WHERE sa.team_name = 'South Africa'
AND NOT EXISTS (
    SELECT 1 FROM matches
    WHERE match_description = 'South Africa vs Australia - Sample Test'
);

INSERT INTO matches
    (match_description, match_format, match_date,
     team1_id, team2_id, venue_id, match_status)
SELECT
    'India vs England - Sample ODI',
    'ODI',
    '2026-10-16',
    india.team_id,
    england.team_id,
    venue.venue_id,
    'Completed'
FROM teams india
JOIN teams england ON england.team_name = 'England'
JOIN venues venue ON venue.venue_name = 'Wankhede Stadium'
WHERE india.team_name = 'India'
AND NOT EXISTS (
    SELECT 1 FROM matches
    WHERE match_description = 'India vs England - Sample ODI'
);
