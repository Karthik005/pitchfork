from django.contrib import admin
from users.models import *
from pitch.models import *
# Register your models here.

# class ProgLangAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     extra = 10

admin.site.register(Pitch)
# admin.site.register(PitchData)
# admin.site.register(DevData)
admin.site.register(Data)
# admin.site.register(Programming_language, ProgLangAdmin)