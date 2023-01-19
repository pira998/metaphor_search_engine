from elasticsearch import Elasticsearch

INDEX = 'songs_new'
client = Elasticsearch("https://localhost:9200", verify_certs=False,
                   http_auth=['elastic', 'juFxrPmD*c1jp-_NYRUx'],)

def fundamental_search(query):
    # result = client. (index=INDEX,body=standard_analyzer(query))
    # keywords = result ['tokens']['token']
    # print(keywords)

    # query_body= process(query)
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        }
    }
    query_body = q
    print('Making Basic Search ')
    res = client.search(index=INDEX, body=query_body)
    print(res)
    return res

def basic_multiple_filter_search(fields):
    """
    example of query
    {
        "query": {
            "bool" : {
            "must" : [
                {"term" : { "Composer" : "ஏ. ஆர். ரஹ்மான்" }},
                {"term" : { "Lyricist" : "வாலி" }},
                {"term":{"Star":"மாதவன்"}},
                {"range" : {"Year" : { "gte" : 2000, "lte" : 2010 }}}
            ]
            }
        }
        }
    """
    q = {}
    q["query"] = {}
    q["query"]["bool"] = {}
    q["query"]["bool"]["must"] = []

    print(fields)
    
    for field in fields:
        if field == 'Year':
            q["query"]["bool"]["must"].append({"range":{field:fields[field]}})
        else:
            q["query"]["bool"]["must"].append({"match":{field:fields[field]}})

    print(q)

    res = client.search(index=INDEX, body=q)
    return res


def search_advanced_query(query):
    qus = {
       "query": {
            "wildcard": {
                "Metaphor": "*"+query+"*"
            }
        }
    }

    res = client.search(index=INDEX, body=qus)
    print(res)

    return res

def basic_search(query):
    # import pdb
    # pdb.set_trace()
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        }
    }
    return q


def multi_match(query, fields=['Song Name', 'Album'], operator='or'):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    return q


def agg_target_domain(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "aggs": {
            "target_domain": {
                "terms": {
                    "field": "Target Domain",
                    "size": 100
                }
            }
        }
    }
    return q