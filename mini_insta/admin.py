# File: mini_insta/admin.py
# Author: Ilay Guler (ilay2004@bu.edu), 2/12/2026
# Description: Registering the Profile model so we can manage data in this model through the admin interface

from django.contrib import admin

from .models import Profile

# Register your models here.
admin.site.register(Profile)