import googlesearch

def search(query, lang="es", num_results=3):
    results = googlesearch.search(query, lang=lang, num_results=num_results)
    return list(dict.fromkeys(results))