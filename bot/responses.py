import requests
from bs4 import BeautifulSoup


def search_muse(query:str) -> str:
    """
    This function takes a user str request and returns Statmuse query

    Parameters
    ----------
    str: query
        text from user in discord server
    
    Returns
    -------
    str: result
        text of query response
    """

    URL = f'https://www.statmuse.com/nfl/ask/{query}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    if page.status_code != 200:
        raise Exception(f"Failed to retrieve data from {URL}")

    h1_tag = soup.find("h1")
    if h1_tag is None:
        raise ValueError("Could not find h1")
    
    span_tag = h1_tag.find("span")
    if span_tag is None:
        raise ValueError("Could not find span")
    
    return span_tag.text
