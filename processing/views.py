from django.http import HttpResponse

from collection.utils import gnews_keyword_articles
from processing.utils import get_sentiment


def get_news_article_predictions(request):
    query = request.GET.get('query')
    if query is None or len(query) == 0:
        return HttpResponse("No Query Param.")
    articles = gnews_keyword_articles(query, fetch_full_article=True, write_to_file=True)
    classified_sentiments = get_sentiment(articles, query=query, write_to_file=True)
    return HttpResponse(classified_sentiments)

