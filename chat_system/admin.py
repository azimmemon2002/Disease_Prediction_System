from django.contrib import admin
from .models import Chat


# Register your models here.

class chatdisplay(admin.ModelAdmin):
    list_display =("message","sender","created_time","consultation_id")

admin.site.register(Chat,chatdisplay)
