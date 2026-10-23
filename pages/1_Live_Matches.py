
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from api.cricbuzz_client import get_live_matches

st.set_page_config(
    page_title="Live Matches | Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
)

from utils.theme import apply_theme

apply_theme()


live_data = get_live_matches()

if live_data is None:
    st.warning("Unable to fetch live matches from Cricbuzz API.")
else:
    st.success("Cricbuzz API connected successfully!")

    st.subheader("🌐 Live Matches from Cricbuzz API")

    api_matches = []

    for match_type in live_data.get("typeMatches", []):
        for series in match_type.get("seriesMatches", []):
            series_data = series.get("seriesAdWrapper", {})

            for match in series_data.get("matches", []):
                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                team1 = info.get("team1", {}).get("teamName", "Team 1")
                team2 = info.get("team2", {}).get("teamName", "Team 2")

                api_matches.append({
                    "Match": info.get("matchDesc", "Match"),
                    "Team 1": team1,
                    "Team 2": team2,
                    "Format": info.get("matchFormat", "N/A"),
                    "Status": info.get("status", info.get("state", "N/A")),
                    "Score Data": score,
                })

if api_matches:
 for match in api_matches:
        with st.container(border=True):
            st.markdown(f"### 🏏 {match['Team 1']} vs {match['Team 2']}")
            st.write(f"**Match:** {match['Match']} · **Format:** {match['Format']}")
            st.write(f"**Status:** {match['Status']}")

            score_data = match["Score Data"]

            col1, col2 = st.columns(2)

for col, key, team_key in [
    (col1, "Team 1", "team1Score"),
    (col2, "Team 2", "team2Score"),
]:
    innings = score_data.get(team_key, {})

    with col:
        st.markdown(f"**{match[key]}**")

        if innings:
            for details in innings.values():
                runs = details.get("runs", 0)
                wickets = details.get("wickets", 0)
                overs = details.get("overs", 0)

                st.metric(
                    label=f"Innings {details.get('inningsId', '')}",
                    value=f"{runs}/{wickets}",
                    help=f"Overs: {overs}",
                )
        else:
            st.caption("Score unavailable")


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
.match-hero {
    background: linear-gradient(120deg, #123b35, #172554);
    border: 1px solid #28564e;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 25px;
}
.match-hero h1 {
    color: white;
    font-size: 34px;
}
.match-hero p {
    color: #cbd5e1;
}
.score-card {
    background: #121e31;
    border: 1px solid #293b55;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 15px;
}
.team-name {
    font-size: 19px;
    font-weight: 800;
    color: #f8fafc;
}
.score-label {
    color: #94a3b8;
    font-size: 12px;
}
.status {
    color: #5eead4;
    font-weight: 700;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="match-hero">
    <h1>🏏 Live Match Center</h1>
    <p>Explore cricket match records and scorecard statistics.</p>
</div>
""", unsafe_allow_html=True)

if not DB_PATH.exists():
    st.error("Database not found. Check that data/cricbuzz.db exists.")
    st.stop()

with sqlite3.connect(DB_PATH) as conn:
    matches = pd.read_sql_query("""
        SELECT
            m.match_id,
            m.match_description,
            m.match_format,
            m.match_date,
            m.match_status,
            t1.team_name AS team1,
            t2.team_name AS team2
        FROM matches m
        LEFT JOIN teams t1 ON m.team1_id = t1.team_id
        LEFT JOIN teams t2 ON m.team2_id = t2.team_id
        ORDER BY m.match_date DESC, m.match_id DESC
    """, conn)

    scores = pd.read_sql_query("""
        SELECT
            s.match_id,
            p.team_id,
            SUM(s.runs_scored) AS runs,
            SUM(s.wickets_taken) AS wickets
        FROM player_match_stats s
        JOIN players p ON s.player_id = p.player_id
        GROUP BY s.match_id, p.team_id
    """, conn)

st.subheader("⚡ Match Feed")

formats = ["All Formats"] + sorted(
    matches["match_format"].dropna().unique().tolist()
)
selected_format = st.selectbox("Filter by match format", formats)

if selected_format != "All Formats":
    matches = matches[matches["match_format"] == selected_format]

if matches.empty:
    st.info("No matches found for this format.")
else:
    st.caption(
        "Demo database records are shown below. Scores are calculated "
        "from stored player statistics; missing scores are labelled unavailable."
    )

    for _, match in matches.iterrows():
        team1 = match["team1"] or "Team 1"
        team2 = match["team2"] or "Team 2"
        match_id = match["match_id"]

        score1 = scores[
            (scores["match_id"] == match_id) &
            (scores["team_id"] == (
                conn.execute if False else -999
            ))
        ] if False else scores.iloc[0:0]

        # Get scores for each team from the database.
        with sqlite3.connect(DB_PATH) as score_conn:
            team_ids = score_conn.execute(
                "SELECT team1_id, team2_id FROM matches WHERE match_id = ?",
                (int(match_id),)
            ).fetchone()

        score_text = {}
        for team_id, team_name in zip(team_ids, [team1, team2]):
            row = scores[
                (scores["match_id"] == match_id) &
                (scores["team_id"] == team_id)
            ]
            if not row.empty:
                score_text[team_name] = (
                    f"{int(row.iloc[0]['runs'])}/"
                    f"{int(row.iloc[0]['wickets'])}"
                )
            else:
                score_text[team_name] = "Score unavailable"

        st.markdown(f"""
        <div class="score-card">
            <div class="status">● {match['match_format']} · {match['match_status'] or 'Status unavailable'}</div>
            <br>
            <div class="team-name">{team1}</div>
            <h2 style="color:white;">{score_text[team1]}</h2>
            <br>
            <div class="team-name">{team2}</div>
            <h2 style="color:white;">{score_text[team2]}</h2>
            <div class="score-label">
                {match['match_description']} · {match['match_date']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.caption(
    "These are database-based demo statistics, not verified live scores. "
    "Connect the Cricbuzz API for real-time match scores."
)
