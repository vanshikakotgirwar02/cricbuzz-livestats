
from utils.db_connection import fetch_all, execute_query


def create_player(full_name, team_id, playing_role, batting_style="", bowling_style=""):
    """Add a new player."""
    query = """
        INSERT INTO players
            (full_name, team_id, playing_role, batting_style, bowling_style)
        VALUES (?, ?, ?, ?, ?);
    """
    return execute_query(
        query,
        (full_name.strip(), team_id, playing_role, batting_style, bowling_style),
    )


def get_player_by_id(player_id):
    """Retrieve one player by ID."""
    query = """
        SELECT p.*, t.team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        WHERE p.player_id = ?;
    """
    rows = fetch_all(query, (player_id,))
    return rows[0] if rows else None


def update_player(player_id, full_name, team_id, playing_role, batting_style="", bowling_style=""):
    """Update an existing player's details."""
    query = """
        UPDATE players
        SET full_name = ?, team_id = ?, playing_role = ?,
            batting_style = ?, bowling_style = ?
        WHERE player_id = ?;
    """
    return execute_query(
        query,
        (full_name.strip(), team_id, playing_role, batting_style, bowling_style, player_id),
    )


def delete_player(player_id):
    """Delete a player if no match statistics reference them."""
    return execute_query(
        "DELETE FROM players WHERE player_id = ?;",
        (player_id,),
    )


def get_all_teams():
    """Retrieve teams for dropdown menus."""
    return fetch_all(
        "SELECT team_id, team_name FROM teams ORDER BY team_name;"
    )
