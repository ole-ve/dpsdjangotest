from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('collection/', include('collection.urls')),
    path('processing/', include('processing.urls')),
]
