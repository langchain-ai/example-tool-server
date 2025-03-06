import httpx
import re

SANITIZE = re.compile(r"[^a-zA-Z0-9_-]")


async def get_exchange_rate(base: str, target: str) -> str:
    """Retrieve the current exchange rate between two currencies using the Currency Exchange API.

    Args:
        base: The base currency code (e.g. "USD").
        target: The target currency code (e.g. "EUR").

    Returns:
        A string with the current exchange rate between the base and target currencies.
    """
    base = SANITIZE.sub("", base)
    target = SANITIZE.sub("", target)
    url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        return f"Error: Received {response.status_code} from the Currency Exchange API."

    data = response.json()
    rates = data.get("rates", {})
    if target.upper() not in rates:
        return f"Error: Exchange rate for {target.upper()} not found."

    rate = rates[target.upper()]
    return (
        f"The current exchange rate from {base.upper()} to {target.upper()} is {rate}."
    )
