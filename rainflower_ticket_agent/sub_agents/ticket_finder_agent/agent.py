from google.adk.agents import Agent
from .instruction import ticket_finder_instruction
from .tools import find_ticket

ticket_finder_agent = Agent(
    name="ticket_finder_agent",
    model="gemini-2.0-flash",
    description="Ticket finder agent",
    instruction=ticket_finder_instruction,
    tools=[find_ticket],
)
