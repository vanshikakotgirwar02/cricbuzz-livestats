
# 1. Total number of teams
TOTAL_TEAMS = """
SELECT COUNT(*) AS total_teams
FROM teams;
"""

# 2. Total number of players
TOTAL_PLAYERS = """
SELECT COUNT(*) AS total_players
FROM players;
"""

# 3. List all players with their team names
PLAYERS_WITH_TEAMS = """
SELECT p.full_name, p.playing_role, t.team_name
FROM players p
LEFT JOIN teams t ON p.team_id = t.team_id
ORDER BY t.team_name, p.full_name;
"""

# 4. Top run scorers
TOP_RUN_SCORERS = """
SELECT p.full_name, SUM(s.runs_scored) AS total_runs
FROM players p
JOIN player_match_stats s ON p.player_id = s.player_id
GROUP BY p.player_id, p.full_name
ORDER BY total_runs DESC
LIMIT 10;
"""

# 5. Top wicket takers
TOP_WICKET_TAKERS = """
SELECT p.full_name, SUM(s.wickets_taken) AS total_wickets
FROM players p
JOIN player_match_stats s ON p.player_id = s.player_id
GROUP BY p.player_id, p.full_name
ORDER BY total_wickets DESC
LIMIT 10;
"""

# 6. Match results
MATCH_RESULTS = """
SELECT
    m.match_description,
    m.match_format,
    m.match_date,
    t1.team_name AS team1,
    t2.team_name AS team2,
    winner.team_name AS winner,
    m.match_status
FROM matches m
LEFT JOIN teams t1 ON m.team1_id = t1.team_id
LEFT JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams winner ON m.winner_id = winner.team_id
ORDER BY m.match_date DESC;
"""

# 7. Average runs per player
AVERAGE_RUNS = """
SELECT p.full_name, ROUND(AVG(s.runs_scored), 2) AS average_runs
FROM players p
JOIN player_match_stats s ON p.player_id = s.player_id
GROUP BY p.player_id, p.full_name
ORDER BY average_runs DESC;
"""
