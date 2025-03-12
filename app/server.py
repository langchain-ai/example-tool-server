"""Example tool server!"""

import hmac
import os

from langchain_core.tools import tool
from universal_tool_server import Server, Auth

from app.tools.exchange_rate import get_exchange_rate
from app.tools.github import get_github_issues
from app.tools.hackernews import search_hackernews
from app.tools.reddit import search_reddit_news

DISABLE_AUTH = os.environ.get("DISABLE_AUTH", "").lower() in ("true", "1")


def _get_app_secret() -> str:
    """Get the app secret from the environment.

    This is sufficient for a very simple authentication system that contains
    a single "user" with a single secret key.
    """
    secret = os.environ.get("APP_SECRET")

    if DISABLE_AUTH:
        if secret:
            raise ValueError("APP_SECRET is not needed when DISABLE_AUTH is enabled.")
        return ""

    if not secret:
        raise ValueError("APP_SECRET environment variable is required.")
    if secret != secret.strip():
        raise ValueError("APP_SECRET cannot have leading or trailing whitespace.")
    return secret


APP_SECRET = _get_app_secret()


app = Server()


@app.add_tool()
async def echo(msg: str) -> str:
    """Echo a message appended with an exclamation mark."""
    return msg + "!"


# Or add an existing langchain tool
@tool()
async def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is nice today with a high of 75°F."


app.add_tool(get_weather)

# Add some real tools
TOOLS = [
    search_hackernews,
    get_github_issues,
    get_exchange_rate,
    search_reddit_news,
]

for tool_ in TOOLS:
    app.add_tool(tool_)

# Add the authentication handler
auth = Auth()
app.add_auth(auth)


@auth.authenticate
async def authenticate(authorization: str) -> dict:
    """Authenticate the user based on the Authorization header."""
    if DISABLE_AUTH:
        return {
            "identity": "unauthenticated-user",
        }
    if not authorization or not hmac.compare_digest(authorization, APP_SECRET):
        raise Auth.exceptions.HTTPException(status_code=401, detail="Unauthorized")

    return {
        "identity": "authenticated-user",
    }
