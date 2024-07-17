import selfarxiv
key_words = ["anguage models","rationales","token","text generation","model prediction","sampling algorithm","learnable tokens","thought","teacher forcin"]

keywords_str = " ".join(key_words)
related_works = selfarxiv.Search_paper(keywords_str)
from pprint import pprint
pprint(related_works)
print(f'共有 {len(related_works)} 筆資料')