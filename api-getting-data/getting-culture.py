import json
import os
import sys
from datetime import datetime, timezone

import requests
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule

EUROPEANA_API_KEY = ""

# Urbana coordinates
LATITUDE  = 40.1164
LONGITUDE = -88.2434
LOCATION  = "Urbana, IL"

console = Console()

def fetch_weather() -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":  LATITUDE,
        "longitude": LONGITUDE,
        "current":   "temperature_2m,wind_speed_10m,relative_humidity_2m,precipitation,weather_code",
        "hourly":    "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit":  "mph",
        "forecast_days": 1,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


WMO_DESCRIPTIONS = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ hail", 99: "Thunderstorm w/ heavy hail",
}

def wmo_to_text(code: int) -> str:
    return WMO_DESCRIPTIONS.get(code, f"Weather code {code}")

def derive_search_term(code: int, temp_f: float) -> str:
    """Turn current weather into a Europeana search keyword."""
    if code in (0, 1):
        return "sunshine landscape"
    elif code in (2, 3):
        return "cloudy sky painting"
    elif code in (45, 48):
        return "fog mist painting"
    elif code in range(51, 70):
        return "rain storm painting"
    elif code in range(71, 78):
        return "snow winter landscape"
    elif code in range(80, 83):
        return "rain shower watercolor"
    elif code >= 95:
        return "lightning thunderstorm"
    elif temp_f < 32:
        return "frost ice winter"
    else:
        return "spring landscape"

def search_europeana(query: str, rows: int = 5) -> dict:
    url = "https://api.europeana.eu/record/v2/search.json"
    params = {
        "wskey":  EUROPEANA_API_KEY,
        "query":  query,
        "rows":   rows,
        "profile": "rich",
        "qf":     "TYPE:IMAGE", 
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_europeana_item(record_id: str) -> dict:
    url = f"https://api.europeana.eu/record/v2{record_id}.json"
    params = {"wskey": EUROPEANA_API_KEY}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def display_weather(data: dict):
    cur = data["current"]
    code = cur.get("weather_code", 0)
    desc = wmo_to_text(code)
    temp = cur["temperature_2m"]
    wind = cur["wind_speed_10m"]
    rh   = cur.get("relative_humidity_2m", "—")
    prec = cur.get("precipitation", 0)

    console.print(Rule(f"[bold cyan]🌤  Current Weather — {LOCATION}[/bold cyan]"))
    panel_text = (
        f"[bold]{desc}[/bold]\n\n"
        f"🌡  Temperature:  [yellow]{temp} °F[/yellow]\n"
        f"💨  Wind Speed:   [blue]{wind} mph[/blue]\n"
        f"💧  Humidity:     {rh} %\n"
        f"🌧  Precipitation: {prec} mm\n"
        f"🕐  Time:         {cur['time']}"
    )
    console.print(Panel(panel_text, title="Open-Meteo API", border_style="cyan"))

    # Hourly table (first 6 hours)
    hourly = data["hourly"]
    table = Table(title="Hourly Forecast (first 6 h)", border_style="dim")
    table.add_column("Time",        style="dim")
    table.add_column("Temp (°F)",   justify="right", style="yellow")
    table.add_column("Humidity (%)", justify="right", style="blue")
    table.add_column("Wind (mph)",  justify="right", style="green")
    for i in range(6):
        table.add_row(
            hourly["time"][i],
            str(hourly["temperature_2m"][i]),
            str(hourly["relative_humidity_2m"][i]),
            str(hourly["wind_speed_10m"][i]),
        )
    console.print(table)


def display_europeana_results(results: dict, query: str):
    items = results.get("items", [])
    console.print(Rule(f'[bold magenta]🏛  Europeana Search — "{query}"[/bold magenta]'))
    console.print(f"[dim]Total results: {results.get('totalResults', '?')}  |  Showing top {len(items)}[/dim]\n")

    for i, item in enumerate(items, 1):
        title = item.get("title", ["(no title)"])[0]
        creator = (item.get("dcCreator") or ["Unknown"])[0]
        provider = (item.get("dataProvider") or ["—"])[0]
        year = (item.get("year") or ["—"])[0]
        link = "https://www.europeana.eu/item" + item.get("id", "")
        console.print(f"  [bold]{i}.[/bold] [cyan]{title}[/cyan]")
        console.print(f"     Artist: {creator}  |  Source: {provider}  |  Year: {year}")
        console.print(f"     🔗 {link}\n")


def display_item_detail(item_data: dict):
    obj = item_data.get("object", {})
    title_list = obj.get("title", ["(no title)"])
    title = title_list[0] if title_list else "(no title)"

    proxies = obj.get("proxies", [{}])
    proxy = proxies[0] if proxies else {}
    desc_map = proxy.get("dcDescription", {})
    desc = list(desc_map.values())[0][0] if desc_map else "No description available."

    agg = (obj.get("aggregations") or [{}])[0]
    thumbnail = agg.get("edmPreview", "—")
    rights = agg.get("edmRights", {})
    rights_url = list(rights.values())[0][0] if rights else "—"

    console.print(Rule("[bold green]📄  Selected Europeana Item Detail[/bold green]"))
    detail_text = (
        f"[bold]{title}[/bold]\n\n"
        f"[italic]{desc[:300]}{'...' if len(desc) > 300 else ''}[/italic]\n\n"
        f"🖼  Thumbnail:  {thumbnail}\n"
        f"⚖️  Rights:     {rights_url}"
    )
    console.print(Panel(detail_text, title="Europeana Record API", border_style="green"))

def save_item_json(item_data: dict, query: str):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"europeana_item_{ts}.json"
    output = {
        "source_api":   "Europeana",
        "search_query": query,
        "retrieved_at": ts,
        "item":         item_data,
    }

    def redact_keys(obj):
        if isinstance(obj, dict):
            return {k: redact_keys(v) for k, v in obj.items() if k not in ("apikey", "wskey", "api_key")}
        if isinstance(obj, list):
            return [redact_keys(i) for i in obj]
        return obj

    output = redact_keys(output)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    return filename


def main():
    console.print(Panel.fit(
        "[bold]Weather × Europeana Explorer[/bold]\n"
        "[dim]Open-Meteo  +  Europeana Cultural Heritage API[/dim]",
        border_style="bold white",
    ))

    console.print("\n[bold]Step 1:[/bold] Fetching weather data from Open-Meteo…")
    try:
        weather = fetch_weather()
    except requests.RequestException as e:
        console.print(f"[red]Error fetching weather:[/red] {e}")
        sys.exit(1)

    display_weather(weather)

    cur_code = weather["current"].get("weather_code", 0)
    cur_temp = weather["current"]["temperature_2m"]
    search_term = derive_search_term(cur_code, cur_temp)
    console.print(f"\n[dim]→ Derived search term from current conditions: [italic]\"{search_term}\"[/italic][/dim]\n")

    console.print("[bold]Step 2:[/bold] Searching Europeana collection…")
    try:
        euro_results = search_europeana(search_term)
    except requests.RequestException as e:
        console.print(f"[red]Error querying Europeana:[/red] {e}")
        sys.exit(1)

    items = euro_results.get("items", [])
    if not items:
        console.print("[yellow]No Europeana results found. Try a different query.[/yellow]")
        sys.exit(0)

    display_europeana_results(euro_results, search_term)

    top_id = items[0]["id"]
    console.print(f"[bold]Step 3:[/bold] Fetching full record for top item [dim]{top_id}[/dim]…")
    try:
        item_detail = fetch_europeana_item(top_id)
    except requests.RequestException as e:
        console.print(f"[red]Error fetching item detail:[/red] {e}")
        sys.exit(1)

    display_item_detail(item_detail)

    console.print("\n[bold]Step 4:[/bold] Saving item data to JSON…")
    fname = save_item_json(item_detail, search_term)
    console.print(f"[green]✓ Saved:[/green] [bold]{fname}[/bold]")
    console.print(f"[dim]  (Contains full Europeana record JSON for item {top_id})[/dim]\n")


if __name__ == "__main__":
    main()