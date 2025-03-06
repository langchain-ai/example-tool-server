from langchain_core.tools import tool

@tool()
async def echo(msg: str) -> str:
    return msg + "!"


