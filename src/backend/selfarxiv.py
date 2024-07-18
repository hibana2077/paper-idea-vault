import requests
import time
from fake_useragent import UserAgent
import xml.etree.ElementTree as ET

# Set the API endpoint URL
BASE_URL = 'http://export.arxiv.org/api/query?'

def Search_paper(keywords:str,start=0) -> list[dict]:
    """
    Search for papers on arXiv based on the given keywords.

    Args:
        keywords (str): The keywords to search for.

    Returns:
        list[dict]: A list of dictionaries representing the found papers. Each dictionary contains the following keys:
            - 'title': The title of the paper.
            - 'summary': The summary of the paper.
            - 'arxiv_id': The arXiv ID of the paper.
            - 'authors': A list of authors of the paper.
    """
    search_query = 'cs:' + keywords
    # all -> all fields
    # cs.AI -> Computer Science - Artificial Intelligence
    start = start
    max_results = 15
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    query = f'{BASE_URL}search_query={search_query}&start={start}&max_results={max_results}'
    response = requests.get(query, headers=headers)
    papers = []
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
            papers.append({'title': title, 'summary': summary, 'arxiv_id': arxiv_id, 'authors': authors})
    return papers