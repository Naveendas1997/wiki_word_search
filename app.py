from typing import Union

from fastapi import FastAPI, HTTPException, Query
import requests
from collections import Counter
import re

app = FastAPI()
class WikipediaSearch:
    def __init__(self):
        self.search_history = []

search_instance = WikipediaSearch()

@app.get("/wordFrequency")
def word_frequency(topic: str, top_n: int):
        base_url = "https://en.wikipedia.org/w/api.php"
        params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": topic,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        # Extract relevant information from the API response
        search_results = data.get("query", {}).get("search", [])

        if not search_results:
            print(f"No results found for '{topic}' on Wikipedia.")
            return

        # Concatenate search results snippets for word frequency analysis
        snippets = " ".join(result["snippet"] for result in search_results)

        # Tokenize and count word frequencies
        words = re.findall(r'\b\w+\b', snippets.lower())  # Tokenize using regex
        #to remove html snippet common keywords span, class, searchmatch  
        filtered_words = [word.strip(",.!?") for word in words if word.lower() not in ["span","class","searchmatch"]]
        word_counter = Counter(filtered_words)

        # Display top N frequent words, 3 is default because search operation contains html snippet which contains span, class, searchmatch
        top_words = word_counter.most_common(3+top_n)
        print(f"\nTop {top_n} frequent words:")
        freq={}
        for word, frequency in top_words:
            freq[word]= f"{frequency} occurrences"
        
        search_result_entry = {
            "topic": topic,
            "search_results": search_results,
            "top_frequent_words": word_counter.most_common(top_n)
        }
        search_instance.search_history.append(search_result_entry)
        
        return freq



@app.get("/searchHistory")
def search_history():
    print("\nSearch History:")
    
    return search_instance.search_history



