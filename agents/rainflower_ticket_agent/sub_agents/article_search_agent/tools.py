from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_article(article_name: str) -> dict:
    """
    Return the HTML content of the article with the given name.
    """
    url = os.getenv("HUDU_URL") + "/articles?name=" + article_name
    headers = {"x-api-key": os.getenv("HUDU_API_KEY")}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "HTML Content": data["articles"][0]["content"]
        }
    else:
        return {
            "Error": f"Error {response.status_code}: {response.text}"
        }

def get_articles() -> dict:
    """
    Returns a dictionary of every article in the knowledge base.
    """
    names = []
    url = os.getenv("HUDU_URL") + "/articles"
    headers = {"x-api-key": os.getenv("HUDU_API_KEY")}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for article in data["articles"]:
            names.append(article["name"])
    else:
        return {
            "Error": f"Error {response.status_code}: {response.text}"
        }

    return {
        "names": names
    }