# Weather and Europeana Explorer

## API Used

### Open-Meteo 
[Open-Meteo](https://open-meteo.com/) is a free, open-source weather API with no API key required and no usage limits.

Having worked with paid weather APIs before — like the Weather.com (Weather Channel) API — I know how extensive weather data can be. Paid services often offer dozens of endpoints covering everything from specific, local forecasts to historical climate archives, air quality indexes, and severe weather alerts. That itself is powerful, and there's a lot you can build on top of it. But for a project like this, it isn't necessary.

Open-Meteo is great because it exposes the same core data (current conditions, WMO weather codes, wind, temperature) without requiring an account, without rate limits, and without a billing relationship. 

## How It Works

1. Fetches current weather for Urbana, IL (temperature, wind speed, WMO code) via Open-Meteo
2. Maps the weather code to a search term (e.g., clear sky → `"sunshine landscape"`)
3. Searches Europeana for the top 3 matching image records
4. Fetches the full detail for the top result and displays it
5. Saves the item to a timestamped JSON file

## Setup

```bash
pip install requests rich
python weather_europeana_explorer.py
```

## Output
- A cyan panel with current weather conditions
- A list of the top 3 matching Europeana items
- A green panel with the full detail of the top result
- A JSON file named `europeana_item_<timestamp>.json`
