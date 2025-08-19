from rainflower_ticket_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def main(query):
    session_service = InMemorySessionService()

    initial_state = {
        "author" : "lvngstn",
        "chat_history" : [] 
    }
    USER_ID = "aiden"
    APP_NAME = "rainflower_ticket"

    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )
    SESSION_ID = new_session.id

    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service
    )

    response = await call_agent_async(runner, USER_ID, SESSION_ID, query)
    print(response[-1])
    return response[-1]

async def call_agent_async(runner, user_id, session_id, query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    response = []
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.content.parts[0].text:
            response.append(event.content.parts[0].text)

    return response