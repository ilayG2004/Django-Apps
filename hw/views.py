#file: hw/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
# Create your views here.
def home(request):
  '''Func to respond to the "views.home" request'''

  response_text =f'''
  <html>
  <h1>Hello World!</h1>
  <p>The current time is {time.ctime()}.</p>
  </html>
  '''

  return HttpResponse(response_text)

def home_page(request):
  '''Respone to URL '', delegate work to a template'''
  template_name = 'hw/home.html'
  # Dict of context variables (key-value pairs)
  context = {
    "time": time.ctime(),
    "letter1": chr(random.randint(65,90)),
    "letter2": chr(random.randint(65,90)),
  }
  return render(request, template_name, context)

def about(request):
  template_name = 'hw/about.html'
  context = {
    "time": time.ctime(),
    "letter1": chr(random.randint(65,90)),
    "letter2": chr(random.randint(65,90)),
  }
  return render(request, template_name, context)