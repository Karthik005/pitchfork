from django.contrib import admin
from users.models import *
# Register your models here.
class ProgLangAdmin(admin.ModelAdmin):
    list_display = ['prog_lang_name']

admin.site.register(Detail)
admin.site.register(Programming_language, ProgLangAdmin)
