from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
from datetime import datetime, timedelta

# Create your views here.
def main_page(request):
  template_name = "restaraunt/main.html"
  return render(request, template_name)


def order_form(request):
  specials = ["Mega texas toast - $1.50", "Corn bread - $1.50", "Mac and cheese - $3.50", "Grits - $2.50"]
  select_special = random.choice(specials)
  template_name = "restaraunt/order_form.html"

  context = {
    "special": select_special
  }
  return render(request, template_name, context)

def submit_order(request):
  food = ""
  name = ""
  phone = ""
  email = ""
  instructions = ""
  possible_items = ["3 finger combo", "4 finger combo", "6 finger combo","Chicken Sandwhich", "no pickles", "special"]
  eta = ""
  if request.POST:
    name = request.POST['customer_name']
    phone = request.POST['customer_phone']
    email = request.POST['customer_email']

    for pitem in possible_items:
      
      if pitem in request.POST:
        if food != "":
          food = food + ", " + pitem
        else:
          food = food + pitem
    
    instructions = request.POST['instructions']

    eta = datetime.now() + timedelta(minutes=random.randint(30,60))
    
  template_name = "restaraunt/confirmation.html"
  context = {
    "name": name,
    "phone": phone,
    "email": email,
    "food": food,
    "instructions": instructions,
    "eta": eta
  }

  return render(request, template_name, context)

