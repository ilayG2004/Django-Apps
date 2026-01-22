from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
import os
from django.conf import settings
# Create your views here.

quotes = ["This is a job and we want to have fun. But it's a job and we should look like we're going to work.",
          "Having hope is everything. The solutions to our problems rarely come as fast as we want them to, and in the meantime, while we wait, it’s our hope and our faith that keep us going.",
          "I'm confident with my ability.",
          "It's our ball ain't it!?",
          "There is a lot of pressure put on me, but I don't put a lot of pressure on myself. I feel if I play my game, it will take care of itself.",
          "You can't be afraid to fail. It's the only way you succeed - you're not gonna succeed all the time, and I know that."]
images_dir = os.path.join(settings.STATICFILES_DIRS[0], "images")

images = [
    f"images/{img}"
    for img in os.listdir(images_dir)
    if img.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))
]

def rand_quote(request):
  template_name = 'quotes/quote.html'
  context = {
    "time": time.ctime(),
    'pic': random.choice(images),
    'quote': random.choice(quotes),
  }
  print(context['pic'])
  return render(request, template_name, context)

def show_all(request):
  context = {"time": time.ctime(),
             "quotes": quotes,
             "images": images}
  template_name = 'quotes/show_all.html'
  return render(request, template_name, context)

def about(request):
  context = {"time": time.ctime(),}
  template_name = "quotes/about.html"
  return render(request, template_name, context)