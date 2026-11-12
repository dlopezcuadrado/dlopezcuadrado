import json
import os
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""

THEMES = {
    "light": {
        "card": "#ffffff", "border": "#d0d7de", "label": "#59636e", "value": "#1f2328", "tile": "#f6f8fa",
        "levels": ["#eff2f5", "#aceebb", "#4ac26b", "#2da44e", "#116329"],
    },
    "dark": {
        "card": "#0d1117", "border": "#30363d", "label": "#9198a1", "value": "#f0f6fc", "tile": "#151b23",
        "levels": ["#151b23", "#033a16", "#196c2e", "#2ea043", "#56d364"],
    },
}

LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
CELL, GAP, PAD = 11, 3, 24


def fetch(login: str, token: str) -> dict:
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-activity-card"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def streaks(days: list[dict], today: date) -> tuple[int, int]:
    counts = {date.fromisoformat(day["date"]): day["contributionCount"] for day in days}
    longest = run = 0
    for day in sorted(counts):
        run = run + 1 if counts[day] else 0
        longest = max(longest, run)
    cursor = today if counts.get(today) else today - timedelta(days=1)
    current = 0
    while counts.get(cursor):
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


def days_label(n: int) -> str:
    return f"{n} {'day' if n == 1 else 'days'}"


def metrics(calendar: dict, today: date) -> list[tuple[str, str]]:
    days = [day for week in calendar["weeks"] for day in week["contributionDays"]]
    current, longest = streaks(days, today)
    return [
        ("Contributions", f"{calendar['totalContributions']:,}"),
        ("Active days", f"{sum(1 for day in days if day['contributionCount']):,}"),
        ("Busiest day", f"{max((day['contributionCount'] for day in days), default=0):,}"),
        ("Current streak", days_label(current)),
        ("Longest streak", days_label(longest)),
    ]


def render(calendar: dict, stats: list[tuple[str, str]], theme: dict) -> str:
    weeks = calendar["weeks"]
    grid_width = len(weeks) * (CELL + GAP) - GAP
    width = grid_width + 2 * PAD
    grid_top = PAD + 22
    tiles_top = grid_top + 7 * (CELL + GAP) + 14
    tile_gap = 10
    tile_width = (grid_width - tile_gap * (len(stats) - 1)) / len(stats)
    height = tiles_top + 58 + PAD

    cells = []
    for x, week in enumerate(weeks):
        for day in week["contributionDays"]:
            y = date.fromisoformat(day["date"]).isoweekday() % 7
            fill = theme["levels"][LEVELS.index(day["contributionLevel"])]
            cells.append(
                f'<rect x="{PAD + x * (CELL + GAP)}" y="{grid_top + y * (CELL + GAP)}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}">'
                f'<title>{day["date"]}: {day["contributionCount"]}</title></rect>'
            )

    tiles = []
    for i, (label, value) in enumerate(stats):
        x = PAD + i * (tile_width + tile_gap)
        tiles.append(
            f'<rect x="{x:.1f}" y="{tiles_top}" width="{tile_width:.1f}" height="58" rx="6" fill="{theme["tile"]}"/>'
            f'<text x="{x + 12:.1f}" y="{tiles_top + 22}" font-size="12" fill="{theme["label"]}">{label}</text>'
            f'<text x="{x + 12:.1f}" y="{tiles_top + 45}" font-size="18" font-weight="600" fill="{theme["value"]}">{value}</text>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'font-family="{FONT}" role="img" aria-label="GitHub activity over the last year">\n'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="8" fill="{theme["card"]}" stroke="{theme["border"]}"/>\n'
        f'<text x="{PAD}" y="{PAD + 6}" font-size="13" fill="{theme["label"]}">Last 12 months, private work included</text>\n'
        + "\n".join(cells) + "\n" + "\n".join(tiles) + "\n</svg>\n"
    )


def main() -> None:
    login, output_dir = sys.argv[1], Path(sys.argv[2])
    calendar = fetch(login, os.environ["GITHUB_TOKEN"])
    stats = metrics(calendar, date.today())
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (output_dir / f"activity-{name}.svg").write_text(render(calendar, stats, theme))


if __name__ == "__main__":
    main()
