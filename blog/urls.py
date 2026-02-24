from django.urls import path
from .views import ShowAllView, ArticleView, RandomArticleView, UpdateArticleView, DeleteArticleView


urlpatterns = [
  path('', RandomArticleView.as_view(), name="random_article"),
  path('show_all', ShowAllView.as_view(), name="show_all"),
  path('article/<int:pk>', ArticleView.as_view(), name="article"),
  path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"),
  path('article/<int:pk>/delete', DeleteArticleView.as_view(), name="delete_article")
]