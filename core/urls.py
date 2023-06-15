from django.urls import path, include, re_path
from .api import BookUploadCSVView, BookApiSet, AuthorApiSet, UserApiSet, OrderApiSet
from rest_framework import routers

book = routers.DefaultRouter()
author = routers.DefaultRouter()
user = routers.DefaultRouter()
order = routers.DefaultRouter()
book.register(r'book', BookApiSet)
author.register(r'author', AuthorApiSet)
user.register(r'user', UserApiSet)
order.register(r'order', OrderApiSet)

urlpatterns = [
    path('', include(user.urls)),
    path('', include(author.urls)),
    path('', include(book.urls)),
    path('', include(order.urls)),
    re_path(r'^book_upload/(?P<filename>[^/]+)$', BookUploadCSVView.as_view()),
]
