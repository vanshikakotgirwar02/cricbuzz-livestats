
from api.cricbuzz_client import get_live_matches


def get_live_match_data():
    """Return the complete live-match API response."""
    return get_live_matches()


def extract_matches():
    """Extract match records from the Cricbuzz API response."""
    data = get_live_match_data()

    if not isinstance(data, dict):
        return []

    type_matches = data.get("typeMatches", [])

    matches = []

    for match_type in type_matches:
        series_matches = match_type.get("seriesMatches", [])

        for series in series_matches:
            series_data = series.get("seriesAdWrapper", {})
            match_list = series_data.get("matches", [])

            for item in match_list:
                match_info = item.get("matchInfo", {})
                match_score = item.get("matchScore", {})

                matches.append({
                    "match_id": match_info.get("matchId"),
                    "description": match_info.get("matchDesc", "Match"),
                    "series": match_info.get("seriesName", "Unknown series"),
                    "format": match_info.get("matchFormat", "Unknown"),
                    "status": match_info.get("status", "Status unavailable"),
                    "state": match_info.get("state", "Unknown"),
                    "team1": match_info.get("team1", {}).get("teamName", "Team 1"),
                    "team2": match_info.get("team2", {}).get("teamName", "Team 2"),
                    "team1_score": match_score.get("team1Score", {}),
                    "team2_score": match_score.get("team2Score", {}),
                    "venue": match_info.get("venueInfo", {}).get("ground", "Unknown venue"),
                    "city": match_info.get("venueInfo", {}).get("city", ""),
                })

    return matches
