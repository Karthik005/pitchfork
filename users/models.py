from django.db import models
from django.contrib.auth.hashers import *
from django.contrib.auth import models as moder

# Create your models here.

    

class Programming_language(models.Model):
    prog_lang_name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return str(self.prog_lang_name)

    
class Detail(models.Model):
    user_ref = models.ForeignKey(moder.User, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    educational_qualifications = models.CharField(max_length=1000)
    experience = models.CharField(max_length=1000)
    prog_langs = models.ManyToManyField(Programming_language)

    