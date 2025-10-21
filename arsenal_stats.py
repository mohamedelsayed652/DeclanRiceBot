from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Final, Optional

import aiohttp

BASE_URL: Final = "https://www.thesportsdb.com/api/v1/json/3"
ARSENAL_TEAM_ID: Final = "133604"
PREMIER_LEAGUE_ID: Final = "4328"
USER_AGENT: Final = "DeclanRiceBot/1.0 (+https://github.com/)"
TIMEOUT: Final = aiohttp.ClientTimeout(total=15)


@dataclass(slots=True)
class StandingsRow:
    rank: int
    played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int


async def build_arsenal_stats_report() -> str:
    try:
        async with aiohttp.ClientSession(
            headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT
        ) as session:
            standings = await _fetch_standings(session)
            last_event = await _fetch_event(session, "eventslast", "Last match data unavailable.")
            next_event = await _fetch_event(session, "eventsnext", "Upcoming fixture not listed.")
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        return (
            "Couldn't reach the stats service right now. Please try again shortly."
            f" (details: {error.__class__.__name__})"
        )

    lines = ["**Arsenal live update**"]

    if standings:
        lines.extend(
            [
                f"Premier League position: {standings.rank} ({standings.points} pts)",
                f"Record: {standings.wins}-{standings.draws}-{standings.losses}"
                f" (Played {standings.played}, GD {standings.goal_difference:+})",
            ]
        )
    else:
        lines.append("Premier League position: unavailable right now.")

    lines.append(_summarise_event("Last match", last_event))
    lines.append(_summarise_event("Next match", next_event))

    return "\n".join(lines)


async def _fetch_standings(session: aiohttp.ClientSession) -> Optional[StandingsRow]:
    season = _current_season()
    payload = {"l": PREMIER_LEAGUE_ID, "s": season}
    data = await _get_json(session, "lookuptable", payload)

    table = data.get("table") if isinstance(data, dict) else None
    if not table:
        return None

    for entry in table:
        if isinstance(entry, dict) and entry.get("strTeam") == "Arsenal":
            try:
                return StandingsRow(
                    rank=int(entry.get("intRank", 0)),
                    played=int(entry.get("intPlayed", 0)),
                    wins=int(entry.get("intWin", 0)),
                    draws=int(entry.get("intDraw", 0)),
                    losses=int(entry.get("intLoss", 0)),
                    goals_for=int(entry.get("intGoalsFor", 0)),
                    goals_against=int(entry.get("intGoalsAgainst", 0)),
                    goal_difference=int(entry.get("intGoalDifference", 0)),
                    points=int(entry.get("intPoints", 0)),
                )
            except (TypeError, ValueError):
                return None
    return None


async def _fetch_event(
    session: aiohttp.ClientSession, endpoint: str, fallback: str
) -> dict[str, Any]:
    data = await _get_json(session, endpoint, {"id": ARSENAL_TEAM_ID})

    events = data.get("events") or data.get("results")
    if isinstance(events, list) and events:
        first = events[0]
        if isinstance(first, dict):
            return first
    return {"fallback": fallback}


async def _get_json(
    session: aiohttp.ClientSession, endpoint: str, params: dict[str, Any]
) -> dict[str, Any]:
    url = f"{BASE_URL}/{endpoint}.php"
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


def _current_season(reference: Optional[datetime] = None) -> str:
    ref = reference or datetime.now(timezone.utc)
    year = ref.year
    if ref.month >= 7:
        return f"{year}-{year + 1}"
    return f"{year - 1}-{year}"


def _summarise_event(prefix: str, event: dict[str, Any]) -> str:
    if not event:
        return f"{prefix}: data unavailable."

    fallback = event.get("fallback")
    if fallback:
        return f"{prefix}: {fallback}"

    home = event.get("strHomeTeam")
    away = event.get("strAwayTeam")
    opponent = _identify_opponent(home, away)

    date_str = event.get("dateEvent") or "TBD"
    time_str = event.get("strTimeLocal") or event.get("strTime")
    kickoff = _format_datetime(date_str, time_str)

    home_score = event.get("intHomeScore")
    away_score = event.get("intAwayScore")

    if home_score is not None and away_score is not None:
        try:
            home_score = int(home_score)
            away_score = int(away_score)
            result = f"{home_score}-{away_score}"
        except (TypeError, ValueError):
            result = "score unavailable"
        location = "home" if home == "Arsenal" else "away"
        return f"{prefix}: vs {opponent} ({location}) on {kickoff} | Result {result}"

    venue = event.get("strVenue") or "venue TBC"
    location = "home" if home == "Arsenal" else "away"
    return f"{prefix}: vs {opponent} ({location}, {venue}) on {kickoff}"


def _identify_opponent(home: Any, away: Any) -> str:
    if home == "Arsenal" and away:
        return str(away)
    if away == "Arsenal" and home:
        return str(home)
    if home:
        return str(home)
    if away:
        return str(away)
    return "Unknown opponent"


def _format_datetime(date_str: str, time_str: Optional[str]) -> str:
    if not date_str or date_str == "TBD":
        return "TBD"

    if time_str:
        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S%z"]
        for fmt in formats:
            try:
                dt = datetime.strptime(f"{date_str} {time_str}", fmt)
                return dt.strftime("%d %b %Y %H:%M")
            except ValueError:
                continue

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except ValueError:
        return date_str
