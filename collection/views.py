import json
from django.http import HttpResponse
from gnews import GNews

from collection.utils import gnews_keyword_articles

google_news = GNews()


def gnews(request):
    query = request.GET.get('query')
    articles = gnews_keyword_articles(query, fetch_full_article=True, write_to_file=True)
    return HttpResponse(articles)


def test(request):
    with open('data/news_articles/turkey steel price_True.json', 'r') as f:
        data = json.load(f)
        counter = 0
        print(str(True))
        print(len(data))
        for article in data:
            if len(article.get('fullArticle')) == 0:
                counter += 1
        print(counter)
    return HttpResponse(data)
