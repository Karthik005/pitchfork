from django.contrib import admin
from users.models import *
# Register your models here.

class ProgLangAdmin(admin.ModelAdmin):
    list_display = ['name']
    extra = 10

admin.site.register(Detail)
admin.site.register(Programming_language, ProgLangAdmin)
