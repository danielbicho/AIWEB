from bingv2 import bing_search

def search(query, advanced_operators):
    # TODO make usage of the search engine more loosely coupled
    results = bing_search(query, advanced_operators,'Web')
    return results