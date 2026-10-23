
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CRUD Operations | Cricbuzz LiveStats",
    page_icon="🛠️",
    layout="wide",
)

from utils.theme import apply_theme

apply_theme()

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "cricbuzz.db"

st.markdown("""
<style>
.stApp {
    background: #0b1120;
    color: #f1f5f9;
}
.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}
.crud-hero {
    background: linear-gradient(120deg, #123b35, #172554);
    border: 1px solid #28564e;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 25px;
}
.crud-hero h1 {
    color: white;
    font-size: 34px;
}
.crud-hero p {
    color: #cbd5e1;
}
.crud-card {
    background: #121e31;
    border: 1px solid #293b55;
    border-radius: 16px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="crud-hero">
    <h1>🛠️ Cricket Data Management</h1>
    <p>Add, view, edit and delete player records using database operations.</p>
</div>
""", unsafe_allow_html=True)

if not DB_PATH.exists():
    st.error("Database not found. Initialize the database first.")
    st.stop()


def load_players():
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("""
            SELECT
                p.player_id,
                p.full_name,
                t.team_name,
                p.playing_role,
                p.batting_style,
                p.bowling_style
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            ORDER BY p.player_id
        """, conn)


def load_teams():
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT team_id, team_name FROM teams ORDER BY team_name",
            conn,
        )


def run_write(query, parameters=()):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(query, parameters)
        conn.commit()


tab_add, tab_view, tab_edit, tab_delete = st.tabs([
    "➕ Add Player",
    "📋 View Players",
    "✏️ Edit Player",
    "🗑️ Delete Player",
])

teams = load_teams()

# CREATE
with tab_add:
    st.subheader("➕ Register a New Player")
    st.write("Enter the player's information below.")

    with st.form("add_player_form"):
        full_name = st.text_input("Full name")
        team_names = teams["team_name"].tolist()

        selected_team = st.selectbox("Team", team_names)
        role = st.selectbox(
            "Playing role",
            ["Batsman", "Bowler", "All-rounder", "Wicketkeeper"],
        )
        batting_style = st.text_input("Batting style")
        bowling_style = st.text_input("Bowling style")

        submitted = st.form_submit_button("Add Player")

        if submitted:
            if not full_name.strip():
                st.error("Please enter the player's name.")
            else:
                team_id = int(
                    teams.loc[
                        teams["team_name"] == selected_team, "team_id"
                    ].iloc[0]
                )

                try:
                    run_write("""
                        INSERT INTO players
                        (full_name, team_id, playing_role, batting_style, bowling_style)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        full_name.strip(),
                        team_id,
                        role,
                        batting_style.strip() or None,
                        bowling_style.strip() or None,
                    ))

                    st.success(f"{full_name} added successfully!")
                    st.rerun()

                except sqlite3.IntegrityError as error:
                    st.error(f"Could not add player: {error}")

# READ
with tab_view:
    st.subheader("📋 Player Directory")

    players = load_players()

    search = st.text_input(
        "Search players",
        placeholder="Enter a player name or team",
        key="view_search",
    )

    if search:
        mask = (
            players["full_name"].str.contains(
                search, case=False, na=False
            )
            | players["team_name"].str.contains(
                search, case=False, na=False
            )
        )
        players = players[mask]

    st.dataframe(players, use_container_width=True, hide_index=True)
    st.caption(f"{len(players)} player record(s) displayed.")

# UPDATE
with tab_edit:
    st.subheader("✏️ Update Player Details")

    players = load_players()

    if players.empty:
        st.info("No players available to edit.")
    else:
        player_options = {
            f'{row.full_name} (ID: {row.player_id})': int(row.player_id)
            for row in players.itertuples()
        }

        chosen_player = st.selectbox(
            "Select player to edit",
            list(player_options.keys()),
        )
        player_id = player_options[chosen_player]

        current = players[players["player_id"] == player_id].iloc[0]

        with st.form("edit_player_form"):
            new_name = st.text_input(
                "Full name",
                value=current["full_name"],
            )

            team_names = teams["team_name"].tolist()
            current_team = current["team_name"]

            default_team_index = (
                team_names.index(current_team)
                if current_team in team_names else 0
            )

            new_team = st.selectbox(
                "Team",
                team_names,
                index=default_team_index,
            )

            roles = [
                "Batsman", "Bowler", "All-rounder", "Wicketkeeper"
            ]
            current_role = current["playing_role"]
            role_index = (
                roles.index(current_role)
                if current_role in roles else 0
            )

            new_role = st.selectbox(
                "Playing role",
                roles,
                index=role_index,
            )

            new_batting = st.text_input(
                "Batting style",
                value=current["batting_style"] or "",
            )
            new_bowling = st.text_input(
                "Bowling style",
                value=current["bowling_style"] or "",
            )

            update_clicked = st.form_submit_button("Save Changes")

            if update_clicked:
                if not new_name.strip():
                    st.error("Player name cannot be empty.")
                else:
                    new_team_id = int(
                        teams.loc[
                            teams["team_name"] == new_team,
                            "team_id",
                        ].iloc[0]
                    )

                    run_write("""
                        UPDATE players
                        SET full_name = ?, team_id = ?, playing_role = ?,
                            batting_style = ?, bowling_style = ?
                        WHERE player_id = ?
                    """, (
                        new_name.strip(),
                        new_team_id,
                        new_role,
                        new_batting.strip() or None,
                        new_bowling.strip() or None,
                        player_id,
                    ))

                    st.success("Player updated successfully!")
                    st.rerun()

# DELETE
with tab_delete:
    st.subheader("🗑️ Remove a Player")
    st.warning(
        "Deleting a player also removes their associated player-match "
        "statistics. This action cannot be undone."
    )

    players = load_players()

    if players.empty:
        st.info("No players available to delete.")
    else:
        delete_options = {
            f'{row.full_name} (ID: {row.player_id})': int(row.player_id)
            for row in players.itertuples()
        }

        delete_choice = st.selectbox(
            "Select player to delete",
            list(delete_options.keys()),
        )

        confirm = st.checkbox(
            "I understand this deletion is permanent."
        )

        if st.button("Delete Player", type="primary"):
            if not confirm:
                st.error("Please confirm before deleting.")
            else:
                delete_id = delete_options[delete_choice]

                try:
                    run_write(
                        "DELETE FROM player_match_stats WHERE player_id = ?",
                        (delete_id,),
                    )
                    run_write(
                        "DELETE FROM players WHERE player_id = ?",
                        (delete_id,),
                    )

                    st.success("Player deleted successfully!")
                    st.rerun()

                except sqlite3.Error as error:
                    st.error(f"Unable to delete player: {error}")

st.divider()
st.caption("Cricbuzz LiveStats · CRUD operations powered by SQLite")
