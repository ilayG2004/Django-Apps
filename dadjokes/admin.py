# File: dadjokes/views.py
# Author: Ilay Guler (ilay2004@bu.edu), 4/3/2026
# Description: Register our models to the admin site so they can be CRUD'ed through the django admin UI

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)