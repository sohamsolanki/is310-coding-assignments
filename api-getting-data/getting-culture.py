import json
import sys
from datetime import datetime, timezone

import requests
from rich.console import Console
from rich.panel import Panel

EUROPEANA_KEY = ""
console = Console()

def fetch_weather():
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 40.1164, "longitude": -88.2434,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["current"]

def weather_to_query(code, temp):
    if code in (0, 1):   return "sunshine landscape"
    if code in (2, 3):   return "cloudy sky painting"
    if code in (45, 48): return "fog mist painting"
    if code >= 95:       return "lightning thunderstorm"
    if code >= 71:       return "snow winter landscape"
    if code >= 51:       return "rain storm painting"
    if temp < 32:        return "frost ice winter"
    return "spring landscape"

def search_europeana(query):
    resp = requests.get(
        "https://api.europeana.eu/record/v2/search.json",
        params={"wskey": EUROPEANA_KEY, "query": query, "rows": 3, "qf": "TYPE:IMAGE"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("items", [])


def fetch_item(record_id):
    resp = requests.get(
        f"https://api.europeana.eu/record/v2{record_id}.json",
        params={"wskey": EUROPEANA_KEY},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def save_json(item, query):
    def redact(obj):
        if isinstance(obj, dict):
            return {k: redact(v) for k, v in obj.items() if k not in ("wskey", "apikey", "api_key")}
        if isinstance(obj, list):
            return [redact(i) for i in obj]
        return obj

    filename = f"europeana_item_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    with open(filename, "w") as f:
        json.dump(redact({"search_query": query, "item": item}), f, indent=2)
    return filename


try:
    current = fetch_weather()
    console.print(Panel(
        f"[bold]Weather Code:[/bold] {current['weather_code']}\n"
        f"[bold]Temperature:[/bold]  {current['temperature_2m']} °F\n"
        f"[bold]Wind Speed:[/bold]   {current['wind_speed_10m']} mph",
        title="[cyan]Open-Meteo — Urbana, IL[/cyan]", border_style="cyan"
    ))

    query = weather_to_query(current["weather_code"], current["temperature_2m"])
    console.print(f"\n[dim]Searching Europeana for: \"{query}\"…[/dim]\n")

    items = search_europeana(query)
    if not items:
        console.print("[yellow]No Europeana results found.[/yellow]")
        sys.exit(0)

    for i, item in enumerate(items, 1):
        title = (item.get("title") or ["(no title)"])[0]
        creator = (item.get("dcCreator") or ["Unknown"])[0]
        console.print(f"  [bold]{i}.[/bold] [cyan]{title}[/cyan] — {creator}")

    top = fetch_item(items[0]["id"])
    obj = top.get("object", {})
    title = (obj.get("title") or ["(no title)"])[0]
    desc_map = (obj.get("proxies") or [{}])[0].get("dcDescription", {})
    desc = list(desc_map.values())[0][0] if desc_map else "No description available."

    console.print(Panel(
        f"[bold]{title}[/bold]\n\n[italic]{desc[:300]}[/italic]",
        title="[green]Top Europeana Item[/green]", border_style="green"
    ))

    fname = save_json(top, query)
    console.print(f"\n[green]✓ Saved:[/green] {fname}")

except requests.RequestException as e:
    console.print(f"[red]Request error:[/red] {e}")
    sys.exit(1)
