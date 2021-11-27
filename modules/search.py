import googlesearch

black_list_urls = [
    "tripadvisor"
]

def search(query, lang="es", num_results=4):
    results = googlesearch.search(query, lang=lang, num_results=10)
    results = list(dict.fromkeys(results))
    urls = []
    for result in results:
        for blu in black_list_urls:
            if blu not in result:
                urls.append(result)
    return urls[:num_results]