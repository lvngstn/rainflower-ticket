from datetime import datetime
from google.genai import types

async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = None
    agent_name = None

    print("test0")
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):        
        if event.author:
            agent_name = event.author
        
        response = await process_agent_response(event)
        if response:
            final_response_text = response

    if final_response_text and agent_name:
        add_agent_response_to_history(
            runner.session_service, 
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    return final_response_text

async def process_agent_response(event):
    """Process and display agent response events."""
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  AI: '{part.text.strip()}'")

    final_response = None

    if not has_specific_part and event.is_final_response():
        if event.content and event.content.parts and hasattr(event.content.parts[0], "text") and event.content.parts[0].text:
            final_response = event.content.parts[0].text.strip()

    return final_response

def add_user_query_to_history(session_service, app_name, user_id, session_id, query):
    """Add a user query to the interaction history."""
    update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "user_query",
            "query": query,
        },
    )

def add_agent_response_to_history(session_service, app_name, user_id, session_id, agent_name, response):
    """Add an agent response to the interaction history."""
    update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response,
        },
    )

def update_interaction_history(session_service, app_name, user_id, session_id, entry):
    """Add an entry to the interaction history in state.

    Args:
        session_service: The session service instance
        app_name: The application name
        user_id: The user ID
        session_id: The session ID
        entry: A dictionary containing the interaction data
            - requires 'action' key (e.g., 'user_query', 'agent_response')
            - other keys are flexible depending on the action type
    """
    session = session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    interaction_history = session.state.get("interaction_history", [])

    if "timestamp" not in entry:
        entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    interaction_history.append(entry)

    updated_state = session.state.copy()
    updated_state["interaction_history"] = interaction_history

    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state=updated_state,
    )