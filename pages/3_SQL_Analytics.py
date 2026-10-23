
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="SQL Analytics | Cricbuzz LiveStats",
    page_icon="📊",
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
    max-width: 1450px;
}
.analytics-hero {
    background: linear-gradient(120deg, #123b35, #172554);
    border: 1px solid #28564e;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 25px;
}
.analytics-hero h1 {
    color: white;
    font-size: 34px;
}
.analytics-hero p {
    color: #cbd5e1;
}
.metric-card {
    background: #121e31;
    border: 1px solid #293b55;
    border-radius: 16px;
    padding: 20px;
    min-height: 110px;
}
.metric-label {
    color: #94a3b8;
    font-size: 12px;
}
.metric-value {
    color: white;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="analytics-hero">
    <h1>📊 SQL Analytics Studio</h1>
    <p>Turn cricket data into meaningful insights using SQL, Python and interactive charts.</p>
</div>
""", unsafe_allow_html=True)


def load_query(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)


if not DB_PATH.exists():
    st.error("Database not found. Please initialize data/cricbuzz.db first.")
    st.stop()

try:
    # KPI calculations using SQL
    overview = load_query("""
        SELECT
            (SELECT COUNT(*) FROM teams) AS teams,
            (SELECT COUNT(*) FROM players) AS players,
            (SELECT COUNT(*) FROM matches) AS matches,
            (SELECT COALESCE(SUM(runs_scored), 0)
             FROM player_match_stats) AS runs
    """)

    teams_count = int(overview.loc[0, "teams"])
    players_count = int(overview.loc[0, "players"])
    matches_count = int(overview.loc[0, "matches"])
    runs_count = int(overview.loc[0, "runs"])

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "🌍 TEAMS", teams_count),
        (c2, "👥 PLAYERS", players_count),
        (c3, "🏟️ MATCHES", matches_count),
        (c4, "🏏 RECORDED RUNS", runs_count),
    ]

    for col, label, value in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🔍 Analytics Filters")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        teams = load_query("SELECT team_name FROM teams ORDER BY team_name")
        team_options = ["All Teams"] + teams["team_name"].tolist()
        selected_team = st.selectbox("Select team", team_options)

    with filter_col2:
        formats = load_query("""
            SELECT DISTINCT match_format
            FROM matches
            WHERE match_format IS NOT NULL
            ORDER BY match_format
        """)
        format_options = ["All Formats"] + formats["match_format"].tolist()
        selected_format = st.selectbox("Match format", format_options)

    conditions = []
    params = []

    if selected_team != "All Teams":
        conditions.append(
            "(t1.team_name = ? OR t2.team_name = ?)"
        )
        params.extend([selected_team, selected_team])

    if selected_format != "All Formats":
        conditions.append("m.match_format = ?")
        params.append(selected_format)

    where_clause = (
        "WHERE " + " AND ".join(conditions)
        if conditions else ""
    )

    # Filtered match data
    match_data = load_query(f"""
        SELECT
            m.match_description AS Match,
            m.match_date AS Date,
            m.match_format AS Format,
            m.match_status AS Status,
            t1.team_name AS Team_1,
            t2.team_name AS Team_2
        FROM matches m
        LEFT JOIN teams t1 ON m.team1_id = t1.team_id
        LEFT JOIN teams t2 ON m.team2_id = t2.team_id
        {where_clause}
        ORDER BY m.match_date DESC
    """, tuple(params))

    st.markdown("### 🏟️ Match Data Explorer")
    st.dataframe(match_data, use_container_width=True, hide_index=True)

    # Top run scorers, applying the selected team filter
    player_conditions = []
    player_params = []

    if selected_team != "All Teams":
        player_conditions.append("t.team_name = ?")
        player_params.append(selected_team)

    if selected_format != "All Formats":
        player_conditions.append("m.match_format = ?")
        player_params.append(selected_format)

    player_where = (
        "WHERE " + " AND ".join(player_conditions)
        if player_conditions else ""
    )

    top_scorers = load_query(f"""
        SELECT
            p.full_name AS Player,
            t.team_name AS Team,
            SUM(s.runs_scored) AS Runs
        FROM player_match_stats s
        JOIN players p ON s.player_id = p.player_id
        JOIN matches m ON s.match_id = m.match_id
        LEFT JOIN teams t ON p.team_id = t.team_id
        {player_where}
        GROUP BY p.player_id, p.full_name, t.team_name
        ORDER BY Runs DESC
        LIMIT 10
    """, tuple(player_params))

    st.markdown("### 🥇 Top Run Scorers")

    if not top_scorers.empty:
        fig = px.bar(
            top_scorers.sort_values("Runs"),
            x="Runs",
            y="Player",
            color="Team",
            orientation="h",
            title="Runs by Player",
            template="plotly_dark",
        )
        fig.update_layout(
            paper_bgcolor="#0b1120",
            plot_bgcolor="#121e31",
            font_color="#f1f5f9",
            legend_title_text="Team",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top_scorers, use_container_width=True, hide_index=True)
    else:
        st.info("No player statistics match the selected filters.")

    # SQL learning section
    st.markdown("### 💻 Learn from SQL")

    with st.expander("View the SQL query used for top run scorers"):
        st.code("""
SELECT
    p.full_name AS Player,
    t.team_name AS Team,
    SUM(s.runs_scored) AS Runs
FROM player_match_stats s
JOIN players p ON s.player_id = p.player_id
JOIN matches m ON s.match_id = m.match_id
LEFT JOIN teams t ON p.team_id = t.team_id
GROUP BY p.player_id, p.full_name, t.team_name
ORDER BY Runs DESC
LIMIT 10;
        """, language="sql")

    st.caption(
        "Insights are generated from your local SQLite database. "
        "Results depend on the match and player records stored."
    )

except Exception as error:
    st.error(f"Unable to load analytics: {error}")
    st.caption("Check your database tables and column names.")

