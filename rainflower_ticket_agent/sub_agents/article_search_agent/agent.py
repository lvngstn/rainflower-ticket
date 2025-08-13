from google.adk.agents import Agent
from .instruction import article_search_instruction
from .tools import get_articles, get_article

article_search_agent = Agent(
    name="article_search_agent",
    model="gemini-2.0-flash",
    description="Article search agent",
    instruction=article_search_instruction,
    tools=[get_articles, get_article],
)
