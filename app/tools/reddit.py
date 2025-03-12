"""Search a specific reddit topic."""

import httpx


async def search_reddit_news(topic: str) -> str:
    """Search Reddit's news subreddit for posts related to a given topic using Reddit's JSON API.

    Args:
        topic: The topic to search for within the news subreddit.

    Returns:
        A string listing the top 5 news post titles and URLs related to the topic,
        or an error message if the request fails.
    """
    # Build URL to search within the 'news' subreddit (restrict_sr=1 limits the search to this subreddit)
    url = "https://www.reddit.com/r/news/search.json"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RedditNewsBot/0.1)"}

    params = {"q": topic, "restrict_sr": "1", "sort": "new"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return f"Error: Received {response.status_code} from the Reddit API."

    data = response.json()
    posts = data.get("data", {}).get("children", [])
    if not posts:
        return f"No news found for topic '{topic}'."

    results = []
    for post in posts[:5]:
        post_data = post.get("data", {})
        title = post_data.get("title", "No title")
        permalink = post_data.get("permalink", "")
        post_url = f"https://reddit.com{permalink}"
        results.append(f"{title} - {post_url}")

    return "\n".join(results)
