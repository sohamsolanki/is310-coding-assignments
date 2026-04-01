# Weather + Europeana Explorer
## Soham Solanki (ssolan24)

A Python script that combines live weather data with cultural heritage records from the Europeana collection.

## API Used
### Open-Meteo
[Open-Meteo](https://open-meteo.com/) is a free, open-source weather API with no API key required and no usage limits.

Having worked with paid weather APIs before, like the Weather.com (The Weather Channel) API, I know firsthand how extensive weather data can be. Paid services often offer dozens of endpoints covering everything from local and very specific forecasts to historical climate archives, air quality indexes, and severe weather alerts. That is very powerful, and there's a lot you can build on top of it. But for a project like this, that isn't necessary.

Open-Meteo is great as it exposes the same core data (current conditions, hourly forecasts, WMO weather codes, wind, humidity, precipitation) without requiring an account, without rate limits, and without a billing relationship. 

It's also open-source and uses publicly available meteorological models like NOAA GFS and the European ECMWF, so the data quality is legitimate, not a more restricted free tier.

## How It Works

1. Fetches current weather and a 6-hour hourly forecast for Urbana, IL via Open-Meteo
2. Derives a thematic search term from the current WMO weather code (e.g., clear sky → `"sunshine landscape"`, snow → `"snow winter landscape"`)
3. Searches Europeana for image-type records matching that theme
4. Fetches the full record detail for the top result
5. Saves the item data to a timestamped JSON file

## Setup

```bash
pip install requests rich
python weather_europeana_explorer.py
```

## Output

- Rich-formatted terminal output with weather panels, hourly forecast table, and Europeana item detail
- A JSON file named `europeana_item_<timestamp>.json` containing the full Europeana record