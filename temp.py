import urllib.request
import urllib.parse
import feedparser
from datetime import datetime, timedelta

def fetch_daily_papers(date):
  base_url = 'http://export.arxiv.org/api/query?'
  
  # Format the date as required by arXiv API
  date_str = date.strftime('%Y%m%d')
  
  # Create the query parameters
  search_query = f'submittedDate:[{date_str}000000 TO {date_str}235959]'
  params = {
      'search_query': search_query,
      'start': 0,
      'max_results': 100  # Adjust as needed
  }
  
  # Encode the parameters and create the full URL
  query = urllib.parse.urlencode(params)
  url = base_url + query
  
  # Fetch the results
  with urllib.request.urlopen(url) as response:
      parse = feedparser.parse(response.read())
  
  # Process and return the results
  papers = []
  for entry in parse.entries:
      papers.append({
          'title': entry.title,
          'authors': [author.name for author in entry.authors],
          'summary': entry.summary,
          'link': entry.link
      })
  
  return papers

# Example usage
today = datetime.now()
yesterday = today - timedelta(days=1)
papers = fetch_daily_papers(yesterday)

for paper in papers:
  print(f"Title: {paper['title']}")
  print(f"Authors: {', '.join(paper['authors'])}")
  print(f"Link: {paper['link']}")
  print("---")