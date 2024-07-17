import requests
import xml.etree.ElementTree as ET

# Set the API endpoint URL
base_url = 'http://export.arxiv.org/api/query?'

# anguage models,rationales,token,text generation,model prediction,sampling algorithm,learnable tokens,thought,teacher forcin
key_words = ["Knowledge Distillation","CNN","Semantic Segmentation"]

# Set the search query parameters
search_query = 'cs:' + ' '.join(key_words)  # search for papers that contain any of the keywords
start = 0                     # start at the first result
max_results = 10              # return a maximum of 10 results

# Construct the API request URL
query = f'{base_url}search_query={search_query}&start={start}&max_results={max_results}'

# Send the API request
response = requests.get(query)
cnt = 0
# Check if the request was successful
if response.status_code == 200:
  # Parse the XML response
    root = ET.fromstring(response.text)
    # Extract the search results
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        cnt += 1
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        print(f'Title: {title}')
        print(f'ArXiv ID: {arxiv_id}')
        print(f'Summary: {summary}')
        print(f'Authors: {", ".join(authors)}')
        print('---')
    print(f'共有 {cnt} 筆資料')
else:
  print('Error:', response.status_code, response.text)