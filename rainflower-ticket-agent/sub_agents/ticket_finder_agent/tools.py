from dotenv import load_dotenv
import requests
import os

load_dotenv()

def find_ticket(ticket_id: str) -> dict:
    url = os.getenv("ATERA_URL") + "/api/v3/tickets/" + ticket_id
    headers = {"x-api-key": os.getenv("ATERA_API_KEY")}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "Ticket": data
        }
    else:
        return {
            "Error": f"Error {response.status_code}: {response.text}"
        }