import json
import os
import sys
import urllib.request
from html import escape
from pathlib import Path

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount } }
      }
    }
  }
}
"""


def fetch(login: str, token: str) -> dict:
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-stats-card"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def rows(user: dict) -> list[tuple[str, int]]:
    calendar = user["contributionsCollection"]["contributionCalendar"]
    days = [day["contributionCount"] for week in calendar["weeks"] for day in week["contributionDays"]]
    return [
        ("Contributions (last year)", calendar["totalContributions"]),
        ("Active days (last year)", sum(1 for count in days if count)),
        ("Busiest day", max(days, default=0)),
    ]


def render(title: str, data: list[tuple[str, int]]) -> str:
    width, row_height, top = 460, 26, 64
    height = top + row_height * len(data) + 14
    lines = "\n".join(
        f'  <text class="label" x="24" y="{top + i * row_height}">{escape(label)}</text>'
        f'<text class="value" x="{width - 24}" y="{top + i * row_height}" text-anchor="end">{value:,}</text>'
        for i, (label, value) in enumerate(data)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
  <style>
    .card {{ fill: #ffffff; stroke: #d0d7de; }}
    .title {{ fill: #0e75b6; font: 600 17px -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .label {{ fill: #424a53; font: 400 14px -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .value {{ fill: #1f2328; font: 600 14px -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    @media (prefers-color-scheme: dark) {{
      .card {{ fill: #0d1117; stroke: #30363d; }}
      .title {{ fill: #58a6ff; }}
      .label {{ fill: #9198a1; }}
      .value {{ fill: #f0f6fc; }}
    }}
  </style>
  <rect class="card" x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="6"/>
  <text class="title" x="24" y="34">{escape(title)}</text>
{lines}
</svg>
"""


def main() -> None:
    login, output = sys.argv[1], Path(sys.argv[2])
    user = fetch(login, os.environ["GITHUB_TOKEN"])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render("David's GitHub activity", rows(user)))


if __name__ == "__main__":
    main()
