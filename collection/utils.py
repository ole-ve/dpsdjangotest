import json
from gnews import GNews

google_news = GNews()


def gnews_keyword_articles(query: str, fetch_full_article=False, write_to_file=False, use_existing_data=True):
    normalized_file_name = f'data/news_articles/{query.lower()}_{str(use_existing_data)}.json'
    if use_existing_data:
        try:
            with open(normalized_file_name, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            pass

    articles = google_news.get_news(query)

    if fetch_full_article:
        for article in articles:
            full_article = google_news.get_full_article(article['url'])
            if full_article:
                article['fullArticle'] = full_article.text

    if write_to_file:
        with open(normalized_file_name, 'w') as f:
            json.dump(articles, f)

    return articles
