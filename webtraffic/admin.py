from django.contrib import admin

# Register your models here.
from .models import ReceivedData, SentData

admin.site.register(ReceivedData)
admin.site.register(SentData)