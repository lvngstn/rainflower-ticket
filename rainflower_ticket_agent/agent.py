from google.adk.agents import SequentialAgent
from .sub_agents.ticket_finder_agent import ticket_finder_agent
from .sub_agents.article_search_agent import article_search_agent

root_agent = SequentialAgent(
    name="rainflower_ticket_agent",
    description="A pipeline that finds tickets from IT support software and searches an IT Knowledge Base for relevant information",
    sub_agents=[ticket_finder_agent, article_search_agent]
)
