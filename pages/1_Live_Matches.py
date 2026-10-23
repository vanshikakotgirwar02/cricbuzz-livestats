import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from api.cricbuzz_client import get_live_matches
from utils.theme import apply_theme


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Live Matches | Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
)

apply_theme()


# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "cricbuzz.db"


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="match-hero">
        <h1>🏏 Live Match Center</h1>
        <p>Explore cricket matches, live scores, and scorecard statistics.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LIVE MATCHES FROM CRICBUZZ API
# --------------------------------------------------
st.subheader("🌐 Live Matches from Cricbuzz API")

api_matches = []

try:
    live_data = get_live_matches()
except Exception as error:
    live_data = None
    st.warning(f"Unable to fetch live matches: {error}")

if not isinstance(live_data, dict):
    st.warning(
        "Live match data is currently unavailable. "
        "Check your API credentials and try again."
    )
else:
    for match_type in live_data.get("typeMatches", []):
        for series in match_type.get("seriesMatches", []):
            series_data = series.get("seriesAdWrapper", {})

            for item in series_data.get("matches", []):
                info = item.get("matchInfo", {})
                score = item.get("matchScore", {})

                team1 = info.get("team1", {}).get(
                    "teamName", "Team 1"
                )
                team2 = info.get("team2", {}).get(
                    "teamName", "Team 2"
                )

                api_matches.append(
                    {
                        "Match": info.get("matchDesc", "Match"),
                        "Team 1": team1,
                        "Team 2": team2,
                        "Format": info.get("matchFormat", "N/A"),
                        "Status": info.get(
                            "status",
                            info.get("state", "Status unavailable"),
                        ),
                        "Score Data": score,
                    }
                )

    if api_matches:
        st.success("Cricbuzz API data received successfully.")

        for match in api_matches:
            with st.container(border=True):
                st.markdown(
                    f"### 🏏 {match['Team 1']} vs {match['Team 2']}"
                )

                st.write(
                    f"**Match:** {match['Match']} · "
                    f"**Format:** {match['Format']}"
                )
                st.write(f"**Status:** {match['Status']}")

                score_data = match["Score Data"]

                col1, col2 = st.columns(2)

                for col, key, team_key in [
                    (col1, "Team 1", "team1Score"),
                    (col2, "Team 2", "team2Score"),
                ]:
                    with col:
                        st.markdown(f"**{match[key]}**")

                        innings = score_data.get(team_key, {})

                        if innings:
                            for details in innings.values():
                                runs = details.get("runs", 0)
                                wickets = details.get("wickets", 0)
                                overs = details.get("overs", 0)
                                innings_id = details.get(
                                    "inningsId", ""
                                )

                                st.metric(
                                    label=f"Innings {innings_id}",
                                    value=f"{runs}/{wickets}",
                                    help=f"Overs: {overs}",
                                )
                        else:
                            st.caption("Score unavailable")

    else:
        st.info("No live matches were returned by the API.")


if st.button("🔄 Refresh Live Matches"):
    st.rerun()


# --------------------------------------------------
# DATABASE MATCH FEED
# --------------------------------------------------
st.divider()
st.subheader("⚡ Match Feed — Database Records")

if not DB_PATH.exists():
    st.error(
        "Database not found. Check that data/cricbuzz.db exists."
    )
    st.stop()

with sqlite3.connect(DB_PATH) as conn:
    matches = pd.read_sql_query(
        """
        SELECT
            m.match_id,
            m.match_description,
            m.match_format,
            m.match_date,
            m.match_status,
            t1.team_name AS team1,
            t2.team_name AS team2,
            m.team1_id,
            m.team2_id
        FROM matches m
        LEFT JOIN teams t1 ON m.team1_id = t1.team_id
        LEFT JOIN teams t2 ON m.team2_id = t2.team_id
        ORDER BY m.match_date DESC, m.match_id DESC
        """,
        conn,
    )

    scores = pd.read_sql_query(
        """
        SELECT
            s.match_id,
            p.team_id,
            SUM(s.runs_scored) AS runs,
            SUM(s.wickets_taken) AS wickets
        FROM player_match_stats s
        JOIN players p ON s.player_id = p.player_id
        GROUP BY s.match_id, p.team_id
        """,
        conn,
    )


# --------------------------------------------------
# MATCH FORMAT FILTER
# --------------------------------------------------
if matches.empty:
    st.info("No database match records are available.")
else:
    formats = ["All Formats"] + sorted(
        matches["match_format"].dropna().unique().tolist()
    )

    selected_format = st.selectbox(
        "Filter by match format",
        formats,
    )

    if selected_format != "All Formats":
        matches = matches[
            matches["match_format"] == selected_format
        ]

    if matches.empty:
        st.info("No matches found for this format.")

    else:
        st.caption(
            "These are database records. Scores are calculated from "
            "stored player statistics and may not represent live scores."
        )

        for _, match in matches.iterrows():
            team1 = (
                match["team1"]
                if pd.notna(match["team1"])
                else "Team 1"
            )
            team2 = (
                match["team2"]
                if pd.notna(match["team2"])
                else "Team 2"
            )
            match_id = match["match_id"]

            team_ids = [
                match["team1_id"],
                match["team2_id"],
            ]

            score_text = {}

            for team_id, team_name in zip(
                team_ids, [team1, team2]
            ):
                row = scores[
                    (scores["match_id"] == match_id)
                    & (scores["team_id"] == team_id)
                ]

                if not row.empty:
                    runs = int(row.iloc[0]["runs"] or 0)
                    wickets = int(row.iloc[0]["wickets"] or 0)

                    score_text[team_name] = f"{runs}/{wickets}"
                else:
                    score_text[team_name] = "Score unavailable"

            match_format = (
                match["match_format"]
                if pd.notna(match["match_format"])
                else "Format unavailable"
            )
            match_status = (
                match["match_status"]
                if pd.notna(match["match_status"])
                else "Status unavailable"
            )
            match_description = (
                match["match_description"]
                if pd.notna(match["match_description"])
                else "Match details unavailable"
            )
            match_date = (
                match["match_date"]
                if pd.notna(match["match_date"])
                else "Date unavailable"
            )

            st.markdown(
                f"""
                <div class="score-card">
                    <div class="status">
                        ● {match_format} · {match_status}
                    </div>
                    <br>
                    <div class="team-name">{team1}</div>
                    <h2 style="color:white;">
                        {score_text[team1]}
                    </h2>
                    <br>
                    <div class="team-name">{team2}</div>
                    <h2 style="color:white;">
                        {score_text[team2]}
                    </h2>
                    <div class="score-label">
                        {match_description} · {match_date}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption(
    "Live scores are provided by the Cricbuzz API when available. "
    "Database match records are separate demo/project data."
)