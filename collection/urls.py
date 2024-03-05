from django.urls import path

import collection.views

urlpatterns = [
    path('gnews/', collection.views.gnews, name='gnews'),
    path('test/', collection.views.test, name='test'),
]
