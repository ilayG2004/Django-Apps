from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random
# Create your views here.


class ShowAllView(ListView):
  """Show all article objects in our model"""

  model = Article
  template_name = "blog/show_all.html"

  # Contains many instances of our article format
  context_object_name = "articles"

class ArticleView(DetailView):
  model = Article
  template_name = "blog/article.html"
  context_object_name = "article"

class RandomArticleView(DetailView):
  """Display a single article selceted at random"""
  model = Article
  template_name = "blog/article.html"
  context_object_name = "article"

  #ovveride existing DetailView method
  def get_object(self, queryset = ...):
    """return one instance of Article object selected at random"""
    all_articles = Article.objects.all()
    article = random.choice(all_articles)
    return article