from django.shortcuts import render
from rest_framework import generics
from .serializers import *
import random
from django.views.generic import ListView, DetailView

class RandomLookupMixin:
  def get_object(self):
    qset = self.get_queryset()
    qset_len = len(qset)
    rand_index = random.randint(0,qset_len-1)
    item = qset[rand_index]
    return item

# Create your views here.
class ListJokesAPI(generics.ListAPIView):
  queryset = Joke.objects.all()
  serializer_class = JokeSerializer

class DetailJokeAPI(generics.RetrieveUpdateDestroyAPIView):
  queryset= Joke.objects.all()
  serializer_class = JokeSerializer

class RandomJokeAPI(RandomLookupMixin, generics.RetrieveAPIView):
  queryset = Joke.objects.all()
  serializer_class = JokeSerializer

class ListPicturesAPI(generics.ListAPIView):
  queryset = Picture.objects.all()
  serializer_class = PictureSerializer

class DetailPictureAPI(generics.RetrieveUpdateDestroyAPIView):
  queryset= Picture.objects.all()
  serializer_class = PictureSerializer

class RandomPictureAPI(RandomLookupMixin, generics.RetrieveAPIView):
  """
  Apply this mixin to any view or viewset to get multiple field filtering
  based on a `lookup_fields` attribute, instead of the default single field filtering.
  """
  queryset = Picture.objects.all()
  serializer_class = PictureSerializer


# ----- REGULAR HTML VIEWS ------

"""
For the sake of simplicity this one comment will encompass ALL OF THESE GENERIC VIEWS:

I am reusing the same HTML template for all list data, regardless of the string being simple joke text, or an image url. 
This is called list_generic.html. I simply override the context data with a boolean, is_picture, to dynamically indicate to the template
if we need to render an <img> or a <p>

This same logic is being used for the detail view.

Not much else needs to be said here. These are the generics we always work with to display instance(s) of a model dynamically in HTML.
"""
class ListJokeView(ListView):
  model = Joke
  template_name = 'dadjokes/list_generic.html'
  context_object_name = 'items'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_picture'] = False
    return context

class DetailJokeView(DetailView):
  model = Joke
  template_name = 'dadjokes/detail_generic.html'
  context_object_name = 'item'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_picture'] = False
    return context

class ListPictureView(ListView):
  model = Picture
  template_name = 'dadjokes/list_generic.html'
  context_object_name = 'items'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_picture'] = True
    return context

class DetailPictureView(DetailView):
  model = Picture
  template_name = 'dadjokes/detail_generic.html'
  context_object_name = 'item'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_picture'] = True
    return context
  
def random_view(request):
  pic_qset = Picture.objects.all()
  joke_qset = Joke.objects.all()
  pic_rand_index = random.randint(0,len(pic_qset)-1)
  joke_rand_index = random.randint(0, len(joke_qset)-1)

  pic = pic_qset[pic_rand_index]
  joke = joke_qset[joke_rand_index]

  context = {
    "pic": pic,
    "text": joke
  }
  return render(request, template_name="dadjokes/random.html", context=context)

  