
from utils.db_connection import fetch_all


def get_all_players():
    """Return all players with their team names."""
    query = """
        SELECT
            p.player_id,
            p.full_name,
            p.playing_role,
            p.batting_style,
            p.bowling_style,
            t.team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        ORDER BY p.full_name;
    """
    return fetch_all(query)


def get_top_run_scorers(limit=10):
    """Return players ranked by total runs in recorded match statistics."""
    query = """
        SELECT
            p.full_name,
            t.team_name,
            SUM(s.runs_scored) AS total_runs
        FROM player_match_stats s
        JOIN players p ON s.player_id = p.player_id
        LEFT JOIN teams t ON p.team_id = t.team_id
        GROUP BY p.player_id, p.full_name, t.team_name
        ORDER BY total_runs DESC
        LIMIT ?;
    """
    return fetch_all(query, (limit,))


def get_top_wicket_takers(limit=10):
    """Return players ranked by total wickets in recorded match statistics."""
    query = """
        SELECT
            p.full_name,
            t.team_name,
            SUM(s.wickets_taken) AS total_wickets
        FROM player_match_stats s
        JOIN players p ON s.player_id = p.player_id
        LEFT JOIN teams t ON p.team_id = t.team_id
        GROUP BY p.player_id, p.full_name, t.team_name
        ORDER BY total_wickets DESC
        LIMIT ?;
    """
    return fetch_all(query, (limit,))
