from pprint import pprint
import requests

def get_metadata(doi):
    url = f'https://api.crossref.org/works/{doi}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['message']
    else:
        print(f'請求失敗,狀態碼: {response.status_code}')
        return None

def search_works(query):
    url = f'https://api.crossref.org/works?query={query}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['message']
    else:
        print(f'請求失敗,狀態碼: {response.status_code}')
        return None

# 使用關鍵字搜索作品
keyword = 'quantum computing and Convolutional Neural Networks'
results = search_works(keyword)
print(f'關鍵字: {keyword}')
# dict_keys(['facets', 'total-results', 'items', 'items-per-page', 'query'])
print(f'搜索到 {results["total-results"]} 筆作品')
print('前 5 筆作品:')
for item in results['items'][:5]:
    if 'title' not in item:
        continue
    print(f'作品標題: {item["title"][0]}')
    print(f'作品 DOI: {item["DOI"]}')
    print(f'作品 URL: {item["URL"]}')
    print('---')

# # 根據 DOI 獲取元數據
# doi = '10.1038/nature16961'
# metadata = get_metadata(doi)
# print(metadata)