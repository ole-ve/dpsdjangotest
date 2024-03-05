from django.urls import path

import processing.views

urlpatterns = [
    path('gnews/', processing.views.get_news_article_predictions, name='gnews'),
]