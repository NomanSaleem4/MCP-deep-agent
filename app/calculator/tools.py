from langchain_core.tools import tool


@tool
async def get_weather(location: str) -> str:
    """Get weather for location. If location is provided."""
    return "It's always sunny in New York"


@tool
def add(a: int, b: int) -> int:
    """Add two numbers, make sure numbers or equations are given by the user"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers, make sure numbers or equations are given by the user"""
    return a * b


tools = [get_weather, add, multiply]
