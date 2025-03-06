import httpx
from bs4 import BeautifulSoup


async def get_current_events() -> str:
    """Search Wikipedia for current events and return a summary of the events.

    This function queries the Wikipedia API for the "Portal:Current events" page,
    parses the HTML content, and extracts a brief summary of current events.

    Returns:
        A string containing a summary of current events, or an error message if the
        retrieval fails.
    """
    url = f"https://es.wikipedia.org/w/api.php?action=parse&page=Portal:Current_events&format=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        return f"Error: Received {response.status_code} from the Wikipedia API."

    data = response.json()
    html_content = data.get("parse", {}).get("text", {}).get("*", "")
    if not html_content:
        return "Error: Could not retrieve current events content."

    soup = BeautifulSoup(html_content, "html.parser")
    # Extract list items that likely represent individual events.
    event_items = soup.find_all("li")
    if not event_items:
        return "No current events found."

    # Extract text from the events; here we choose the first 5 events as a summary.
    events = [
        item.get_text(strip=True) for item in event_items if item.get_text(strip=True)
    ]
    if not events:
        return "No current events found."

    summary = "\n".join(events[:5])
    return summary
