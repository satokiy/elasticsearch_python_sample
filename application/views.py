from flask import request, redirect, url_for, render_template, flash, session
from application import app, settings
from elasticsearch import Elasticsearch
#import application.settings

@app.route('/', methods=['GET', 'POST'])
def show_results():
    es = Elasticsearch(http_auth=('elastic',settings.ES_PASS))
    
    # ESの検索フォーマット
    body = {
        "query" : {
            "bool": {
                "must": [
                ]            
            }
        },
        "highlight": {
            "fields": {
                "itemCaption": {}
            }
        }
    }
    # search_wordに入力した値がタイトル or キャプションに含まれているかを検索
    if request.form.get('search_word'):
        body['query']['bool']['must'].append(
            { 
                "bool": {
                    "should": [
                        { "match": { "title": request.form.get('search_word') } },
                        { "match": { "itemCaption": request.form.get('search_word') } }
                    ]
                }
            }
        )
    # 価格の最小値で検索
    if request.form.get('price_min'):
        body['query']['bool']['must'].append({ "range": { "itemPrice": { "gte": request.form.get('price_min') } } })

    # 価格の最大値で検索
    if request.form.get('price_max'):
        body['query']['bool']['must'].append({ "range": { "itemPrice": { "lte": request.form.get('price_max') } } })

    result = es.search(index='book', body=body, size=1000)
    result_num = result['hits']['total']['value']
    books = result['hits']['hits']

    return render_template('index.html', result_num=result_num, books=books, request_form=request.form)
