from django.contrib import admin
from .models import People, Address

# Register your models here.
admin.site.register(People)
admin.site.register(Address)