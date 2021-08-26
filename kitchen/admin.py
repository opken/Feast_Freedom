from django.contrib import admin

from .models import Kitchen, Item, Day

# Register your models here.
admin.site.register(Kitchen)
admin.site.register(Item)
admin.site.register(Day)