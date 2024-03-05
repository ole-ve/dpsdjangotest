import json
from django.http import HttpResponse
from gnews import GNews

google_news = GNews()


def gnews(request):
    query = request.GET.get('query')
    if len(query) == 0:
        return HttpResponse("Set a query as param.")

    articles = google_news.get_news(query)

    # TODO: Execute in parallel
    for article in articles:
        article['fullArticle'] = google_news.get_full_article(article['url']).text

    #with open('fixtures/data.json', 'w') as f:
    #    json.dump(articles, f)

    return HttpResponse(articles)


def test(request):
    with open('fixtures/data.json', 'r') as f:
        data = json.load(f)
        counter = 0
        print(len(data))
        for article in data:
            if len(article.get('fullArticle')) == 0:
                print(article.get("title"))
                if article.get('title') == article.get('description'):
                    counter += 1
        print(counter)
    return HttpResponse(data)
