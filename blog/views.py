from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Article
from .forms import UpdateArticleForm
import random
from django.urls import reverse
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
  
class UpdateArticleView(UpdateView):
  model = Article
  form_class = UpdateArticleForm
  template_name = "blog/update_article_form.html"

  def get_success_url(self):
    pk = self.kwargs['pk']
    return reverse('article', kwargs={'pk':pk})


class DeleteArticleView(DeleteView):
  model = Article
  template_name = "blog/delete_article_form.html"

  def get_success_url(self):
    """ Return the URL to redirect after a successful delete """
    
    return reverse('show_all')