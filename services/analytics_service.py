
from utils.db_connection import fetch_all
from sql.queries import (
    TOTAL_TEAMS,
    TOTAL_PLAYERS,
    PLAYERS_WITH_TEAMS,
    TOP_RUN_SCORERS,
    TOP_WICKET_TAKERS,
    MATCH_RESULTS,
    AVERAGE_RUNS,
)


def get_total_teams():
    return fetch_all(TOTAL_TEAMS)[0]["total_teams"]


def get_total_players():
    return fetch_all(TOTAL_PLAYERS)[0]["total_players"]


def get_players_with_teams():
    return fetch_all(PLAYERS_WITH_TEAMS)


def get_top_run_scorers():
    return fetch_all(TOP_RUN_SCORERS)


def get_top_wicket_takers():
    return fetch_all(TOP_WICKET_TAKERS)


def get_match_results():
    return fetch_all(MATCH_RESULTS)


def get_average_runs():
    return fetch_all(AVERAGE_RUNS)
