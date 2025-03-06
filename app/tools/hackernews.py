import httpx


async def search_hackernews(query: str) -> str:
    """Search HackerNews for a given query and return the top 5 results."""
    url = f"https://hn.algolia.com/api/v1/search"
    params = {
        "query": query,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    if response.status_code != 200:
        return f"Error: Received {response.status_code} from HackerNews API."

    data = response.json()
    hits = data.get("hits", [])
    if not hits:
        return "No results found."

    results = []
    for hit in hits[:5]:
        # Prefer "title" but fall back to "story_title"
        title = hit.get("title") or hit.get("story_title") or "No title"
        # Get the URL from either "url" or "story_url"
        link = hit.get("url") or hit.get("story_url") or "No url"
        results.append(f"{title} - {link}")
    return "\n".join(results)
