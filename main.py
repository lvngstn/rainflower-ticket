import asyncio
from rainflower_ticket_agent.agent import root_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

session_service = InMemorySessionService()

initial_state = {
    "user_name": "Aiden Livingston",
    "interaction_history": [],
}

async def main_async():
    APP_NAME = "Rainflower Ticket"
    USER_ID = "aliving"

    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("\nWelcome to Rainflower Ticket Chat!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        add_user_query_to_history(session_service, APP_NAME, USER_ID, SESSION_ID, user_input)
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

if __name__ == "__main__":
    asyncio.run(main_async())