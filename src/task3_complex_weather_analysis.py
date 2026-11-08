from typing import Dict, List, Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30, 
                          wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    precipitation = day["precipitation"]
    if precipitation <= 0:
        rain_severity = "none"
    elif precipitation <= 5:
        rain_severity = "light"
    elif precipitation <= 15:
        rain_severity = "moderate"
    else:
        rain_severity = "heavy"
    swing = round(day["max_temperature"] - day["min_temperature"], 1)
    return {
        "date": day["date"],
        "weather_description": day.get("weather_description", ""),
        "max_temperature": day["max_temperature"],
        "min_temperature": day["min_temperature"],
        "temperature_swing": swing,
        "is_significant_swing": swing > 10,
        "is_hot_day": day["max_temperature"] > temp_threshold,
        "wind_speed": day["wind_speed"],
        "is_windy_day": day["wind_speed"] > wind_threshold,
        "humidity": day["humidity"],
        "is_uncomfortable_day": day["humidity"] > humidity_threshold,
        "precipitation": precipitation,
        "is_rainy_day": precipitation > 0,
        "rain_severity": rain_severity,
    }


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    lines = [
        f"Date: {analysis['date']}",
        f"Weather: {analysis.get('weather_description', '')}",
        f"Temperature: Max {analysis['max_temperature']}°C, Min {analysis['min_temperature']}°C "
        f"(Swing: {analysis['temperature_swing']}°C)",
    ]
    if analysis["is_hot_day"]:
        lines.append("It was a hot day.")
    if analysis.get("is_significant_swing"):
        lines.append("There was a significant temperature swing.")
    if analysis["is_windy_day"]:
        lines.append("It was a windy day.")
    if analysis["is_uncomfortable_day"]:
        lines.append("The humidity made the day uncomfortable.")
    if analysis["is_rainy_day"]:
        severity = analysis.get("rain_severity")
        lines.append(f"It was a rainy day ({severity} rain)." if severity else "It was a rainy day.")
    else:
        lines.append("There was no precipitation.")
    return "\n".join(lines) + "\n"


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    hottest = max(analyses, key=lambda a: a["max_temperature"])
    windiest = max(analyses, key=lambda a: a["wind_speed"])
    most_humid = max(analyses, key=lambda a: a["humidity"])
    rainiest = max(analyses, key=lambda a: a["precipitation"])
    return (
        "Weather Summary:\n"
        f"Hottest day: {hottest['date']} with a maximum temperature of {hottest['max_temperature']}°C\n"
        f"Windiest day: {windiest['date']} with wind speeds of {windiest['wind_speed']} km/h\n"
        f"Most humid day: {most_humid['date']} with a humidity level of {most_humid['humidity']}%\n"
        f"Rainiest day: {rainiest['date']} with {rainiest['precipitation']} mm of precipitation"
    )


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Analyze the weather data for each day
        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        # Generate and print daily reports
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        # Generate and print a summary report
        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")
