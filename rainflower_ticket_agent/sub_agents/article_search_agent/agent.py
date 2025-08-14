from google.adk.agents import Agent
from .instruction import article_search_instruction
from .tools import get_articles, get_article

article_search_agent = Agent(
    name="article_search_agent",
    model="gemini-2.0-flash",
    description="retrieves relevant information and procedures for IT support tickets.",
    instruction=article_search_instruction,
    tools=[get_articles, get_article],
)
