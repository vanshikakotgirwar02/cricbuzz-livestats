
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.theme import apply_theme

apply_theme()

DB_PATH = Path(__file__).resolve().parent / "data" / "cricbuzz.db"

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1120;
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #101a2d;
    border-right: 1px solid #24334c;
}

[data-testid="stSidebar"] p {
    color: #cbd5e1;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

.hero {
    background: linear-gradient(120deg, #123b35, #102b35 55%, #172554);
    border: 1px solid #28564e;
    border-radius: 22px;
    padding: 32px;
    margin-bottom: 25px;
}

.eyebrow {
    color: #5eead4;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 800;
}

.hero h1 {
    color: #ffffff;
    font-size: 38px;
    margin: 10px 0;
    font-weight: 800;
}

.hero p {
    color: #cbd5e1;
    font-size: 15px;
    margin-bottom: 0;
}

.section-title {
    color: #f8fafc;
    font-size: 21px;
    font-weight: 800;
    margin: 24px 0 14px 0;
}

.metric-card {
    background: linear-gradient(145deg, #17243a, #111c2e);
    border: 1px solid #293b55;
    border-radius: 16px;
    padding: 20px;
    min-height: 130px;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #ffffff;
    font-size: 32px;
    font-weight: 800;
    margin-top: 9px;
}

.metric-icon {
    font-size: 23px;
}

.info-card {
    background: #121e31;
    border: 1px solid #263750;
    border-radius: 16px;
    padding: 20px;
    min-height: 150px;
}

.info-card h3 {
    color: #f8fafc;
    font-size: 17px;
}

.info-card p {
    color: #a9b8cc;
    font-size: 13px;
    line-height: 1.7;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #263750;
    border-radius: 12px;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- DATABASE HELPERS ----------------
def fetch_data(query):
    if not DB_PATH.exists():
        return pd.DataFrame()

    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(query, connection)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">🏆 YOUR CRICKET COMMAND CENTER</div>
    <h1>Cricbuzz LiveStats</h1>
    <p>Explore match insights, player performance and SQL-powered cricket analytics — all in one place.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- LOAD DATABASE COUNTS ----------------
try:
    teams_df = fetch_data("SELECT COUNT(*) AS total FROM teams")
    players_df = fetch_data("SELECT COUNT(*) AS total FROM players")
    matches_df = fetch_data("SELECT COUNT(*) AS total FROM matches")

    total_teams = int(teams_df.iloc[0]["total"]) if not teams_df.empty else 0
    total_players = int(players_df.iloc[0]["total"]) if not players_df.empty else 0
    total_matches = int(matches_df.iloc[0]["total"]) if not matches_df.empty else 0

    stats_available = True

except Exception as error:
    total_teams = total_players = total_matches = 0
    stats_available = False
    st.error(f"Could not load database statistics: {error}")


# ---------------- KPI CARDS ----------------
st.markdown('<div class="section-title">📊 Your Cricket Overview</div>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

metrics = [
    (c1, "🌍", "TEAMS", total_teams),
    (c2, "🏏", "PLAYERS", total_players),
    (c3, "🏟️", "MATCHES IN DATABASE", total_matches),
    (c4, "⚡", "DATA STATUS", "Ready" if stats_available else "Check DB"),
]

for column, emoji, label, value in metrics:
    with column:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{emoji}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)


# ---------------- RECENT MATCHES ----------------
st.markdown('<div class="section-title">🏟️ Matches in Your Database</div>',
            unsafe_allow_html=True)

try:
    recent_matches = fetch_data("""
        SELECT
            m.match_description AS Match,
            m.match_format AS Format,
            m.match_date AS Date,
            m.match_status AS Status,
            t1.team_name AS Team_1,
            t2.team_name AS Team_2
        FROM matches m
        LEFT JOIN teams t1 ON m.team1_id = t1.team_id
        LEFT JOIN teams t2 ON m.team2_id = t2.team_id
        ORDER BY m.match_date DESC
        LIMIT 5
    """)

    if not recent_matches.empty:
        st.dataframe(
            recent_matches,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No matches found yet. Add match records to your database.")

except Exception as error:
    st.warning(f"Match information is not available: {error}")


# ---------------- PLAYER LEADERBOARD ----------------
st.markdown('<div class="section-title">⭐ Top Run Scorers</div>',
            unsafe_allow_html=True)

try:
    top_players = fetch_data("""
        SELECT
            p.full_name AS Player,
            t.team_name AS Team,
            SUM(s.runs_scored) AS Runs
        FROM player_match_stats s
        JOIN players p ON s.player_id = p.player_id
        LEFT JOIN teams t ON p.team_id = t.team_id
        GROUP BY p.player_id, p.full_name, t.team_name
        ORDER BY Runs DESC
        LIMIT 5
    """)

    if not top_players.empty:
        st.dataframe(
            top_players,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Player statistics will appear here when available.")

except Exception as error:
    st.warning(f"Player statistics are not available: {error}")


# ---------------- FEATURE CARDS ----------------
st.markdown('<div class="section-title">🚀 Explore Your Dashboard</div>',
            unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="info-card">
        <h3>⚡ Live Match Center</h3>
        <p>Explore current cricket scores and match details through your Cricbuzz API integration.</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="info-card">
        <h3>🏆 Player Insights</h3>
        <p>Explore runs, wickets and player performance using data stored in your database.</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="info-card">
        <h3>📈 SQL Analytics</h3>
        <p>Discover cricket trends with SQL queries, summaries and interactive analytics.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("Cricbuzz LiveStats · Built with Python, Streamlit, SQLite and SQL")
