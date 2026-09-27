import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from mcp import types
import urllib.parse
# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
PWD = os.getcwd()

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.prompt(title="formatted_summary", description="Create a formatted summary using structured output")
async def formatted_summary(question: str) -> str:
    return (
        "Your name is Claudia" 
        f"please create me a formatted summary using structured output: \n{question}"
        "use markdown to format the summary"
        "wish me great day at the end"
    )

@mcp.resource(uri="file://{file}", description="weather server implementation")
async def content_weather(file: str) -> str:
    return open(PWD + "/" + urllib.parse.unquote(file)).read()


@mcp.resource(uri="models://")
def get_models() -> str:
    """Get information about available AI models"""
    print("Retrieving available models")
    models_data = [
        {
            "id": "gpt-4", 
            "name": "GPT-4",
            "description": "OpenAI's GPT-4 large language model"
        },
        {
            "id": "llama-3-70b",
            "name": "LLaMA 3 (70B)",
            "description": "Meta's LLaMA 3 with 70 billion parameters"
        },
        {
            "id": "claude-3-sonnet",
            "name": "Claude 3 Sonnet",
            "description": "Anthropic's Claude 3 Sonnet model"
        }
    ]
    import json
    return json.dumps({"models": models_data})

# Define a greeting resource that dynamically constructs a personalized greeting
@mcp.resource(uri="greeting://{name}", description="greeting server implementation")
def get_greeting(name: str) -> str:
    """Return a greeting for the given name
    
    Args:
        name: The name to greet
        
    Returns:
        A personalized greeting message
    """
    # name: str = "Sergii"
    # Decode URL-encoded name
    decoded_name = urllib.parse.unquote(name)
    print(f"Generating greeting for {decoded_name}")
    return f"Hello, {decoded_name}!"


@mcp.resource(uri="greeting://", description="greeting server implementation")
def get_greeting_personal() -> str:
    """Return a greeting for the given name
    
    Args:
        name: The name to greet
        
    Returns:
        A personalized greeting message
    """
    name: str = "Sergii"
    # Decode URL-encoded name
    decoded_name = urllib.parse.unquote(name)
    print(f"Generating greeting for {decoded_name}")
    return f"Hello, {decoded_name}!"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')