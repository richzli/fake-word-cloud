import json
import requests
import re

API = "https://en.wikipedia.org/w/api.php"
QUERY_PARAMS = {
    "action": "query",
    "format": "json",
    "prop": "extracts",
    "explaintext": 1,
    "exsectionformat": "plain"
}
RANDOM_PARAMS = {
    "action": "query",
    "format": "json",
    "list": "random",
    "rnnamespace": 0
}
LOWERCASE = re.compile("^[a-z]*$")

def get_random_pages(count=5):
    params = { **RANDOM_PARAMS, "rnlimit": count }
    res = requests.get(url=API, params=params).json()
    return [page["title"] for page in res["query"]["random"]]

def query(pages=get_random_pages()):
    extracts = []
    for page in pages:
        params = { **QUERY_PARAMS, "titles": page }
        res = requests.get(url=API, params=params).json()
        for i in res["query"]["pages"]:
            extracts.append(res["query"]["pages"][i]["extract"])
    return extracts

def words(extracts):
    words = []
    for text in extracts:
        words.extend(filter(lambda w: LOWERCASE.match(w) and len(w)>5, re.split("\W+", text.lower())))
    return words