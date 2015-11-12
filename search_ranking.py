from operator import itemgetter

def create_blob(this_dict):
    blob = ""
    for key in this_dict:
        if ((key != 'id') and (key != 'score')):
            blob += ' ' + this_dict[key] + ' '
    return blob.lower()

def search_ranking(results, keywords, limit):
    for result in results:
        blob = create_blob(result)
        print(blob)
        for keyword in keywords:
            if keyword.lower() in blob:
                result['score'] +=  20

            if keyword.lower() in result['name'].lower():
                result['score'] += 10
            if keyword.lower() in result['employer'].lower():
                result['score'] += 5
            if keyword.lower() in result['role'].lower():
                result['score'] += 5

            result['score'] += blob.count(' ' + keyword.lower() + ' ')

            result['score'] += blob.count(keyword)

    results = sorted(results, key=itemgetter('score'), reverse=True)
    if len(results) > int(limit):
        results = results[0:int(limit)]
    return results
