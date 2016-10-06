from bingv2 import BingSearchEngine


class SearchWeb(object):
    def __init__(self, search_engine=BingSearchEngine()):
        self.search_engine = search_engine

    def search(self, query, advanced_operators):
        # TODO make usage of the search engine more loosely coupled
        results = self.search_engine.search(query, advanced_operators)
        return results
