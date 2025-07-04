from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("bhbus")

# Constants
BHTRANS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_bus_request(url: str) -> dict[str, Any] | None:
    """Make a request to the BHTrans API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_bus(state: str) -> str:
    """Get single bus position.

    Args:
        buh_code: Number BUS code (e.g. 9250, 205)
    """
    url = f"{BHTRANS_API_BASE}/path/to/endpint/{state}"
    data = await make_bus_request(url)

    if not data or "position" not in data:
        return "Unable to fetch positions or no bus found."

    if not data["position"]:
        return "No active positions for this bus."

    alerts = [str(position) for position in data["positions"]]
    return "\n---\n".join(alerts)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')