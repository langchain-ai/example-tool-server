import httpx
import re

# Only allow [a-zA-Z0-9_-] in the owner and repo parameters
SANITIZE = re.compile(r"[^a-zA-Z0-9_-]")


async def get_github_issues(owner: str, repo: str) -> str:
    """Retrieve open issues from a specified GitHub repository.

    This tool queries the GitHub API to fetch the top 50 open issues for the repository.
    For example, to fetch issues from the 'python/cpython' repository, call:
        get_github_issues("python", "cpython")

    Args:
        owner: The owner of the repository.
        repo: The name of the repository.

    Returns:
        A string with the top 50 open issues in the repository.
    """
    owner = SANITIZE.sub("", owner)
    repo = SANITIZE.sub("", repo)

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        return f"Error: Received {response.status_code} from the GitHub API."

    issues = response.json()
    if not issues:
        return "No issues found."

    results = []
    for issue in issues[:50]:
        title = issue.get("title", "No title")
        number = issue.get("number", "N/A")
        issue_url = issue.get("html_url", "No URL")
        results.append(f"Issue #{number}: {title} - {issue_url}")

    return "\n".join(results)
