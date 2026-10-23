
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Top Players | Cricbuzz LiveStats",
    page_icon="🏆",
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
.player-hero {
    background: linear-gradient(120deg, #123b35, #172554);
    border: 1px solid #28564e;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 25px;
}
.player-hero h1 {
    color: white;
    font-size: 34px;
}
.player-hero p {
    color: #cbd5e1;
}
.metric-card {
    background: #121e31;
    border: 1px solid #293b55;
    border-radius: 16px;
    padding: 20px;
    min-height: 115px;
}
.metric-label {
    color: #94a3b8;
    font-size: 12px;
}
.metric-value {
    color: #ffffff;
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="player-hero">
    <h1>🏆 Top Player Insights</h1>
    <p>Explore batting, bowling and all-round performance using your cricket database.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def load_players():
    if not DB_PATH.exists():
        return pd.DataFrame()

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("""
            SELECT
                p.player_id,
                p.full_name AS Player,
                COALESCE(t.team_name, 'Unknown') AS Team,
                COALESCE(p.playing_role, 'Not specified') AS Role,
                COALESCE(SUM(s.runs_scored), 0) AS Runs,
                COALESCE(SUM(s.wickets_taken), 0) AS Wickets,
                COALESCE(SUM(s.fours), 0) AS Fours,
                COALESCE(SUM(s.sixes), 0) AS Sixes
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            LEFT JOIN player_match_stats s ON p.player_id = s.player_id
            GROUP BY p.player_id, p.full_name, t.team_name, p.playing_role
            ORDER BY Runs DESC, Wickets DESC
        """, conn)


try:
    players = load_players()

    if players.empty:
        st.warning("No player data found. Add players to your database first.")
        st.stop()

    total_players = len(players)
    top_run_scorer = players.iloc[0]["Player"]
    total_runs = int(players["Runs"].sum())
    total_wickets = int(players["Wickets"].sum())

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "👥 PLAYERS", total_players),
        (c2, "🏏 TOTAL RUNS", total_runs),
        (c3, "🎯 TOTAL WICKETS", total_wickets),
        (c4, "⭐ TOP RUN SCORER", top_run_scorer),
    ]

    for col, label, value in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🔎 Find a Player")

    search = st.text_input(
        "Search by player name",
        placeholder="Type a name, e.g. Virat Kohli"
    )

    filtered = players[
        players["Player"].str.contains(search, case=False, na=False)
    ]

    team_options = ["All Teams"] + sorted(filtered["Team"].unique().tolist())
    selected_team = st.selectbox("Filter by team", team_options)

    if selected_team != "All Teams":
        filtered = filtered[filtered["Team"] == selected_team]

    st.markdown("### 🥇 Player Performance Rankings")

    display_columns = [
        "Player", "Team", "Role", "Runs", "Wickets", "Fours", "Sixes"
    ]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### 📊 Compare Player Runs")

    if not filtered.empty:
        chart_data = filtered.set_index("Player")[["Runs"]]
        st.bar_chart(chart_data, y="Runs")
    else:
        st.info("No players match your search.")

    st.caption(
        "Statistics are calculated from your local database and depend on the data entered."
    )

except Exception as error:
    st.error(f"Unable to load player statistics: {error}")
    st.caption("Check that data/cricbuzz.db and its tables exist.")

