from django.db import models
from django.contrib.auth.models import *
from users import models as users_models


#File upload function
def upload_path(instance, filename):
	return str(instance.user.username)+"/pitches/"+str(instance.id)+"/"+filename


# Models.

class Pitch(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
   	title = models.CharField(max_length=200, unique=True)
   	date = models.DateField()
   	pitch = models.TextField()
	prog_langs = models.ManyToManyField(users_models.Programming_language)
	document = models.FileField(upload_to = upload_path, blank = True)
	dev_state = models.CharField(max_length=50)

	def __str__(self):
		return str(self.title)


class Data(models.Model):
	
	pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	def _get_votes(self): return self.upvotes-self.downvotes

	votes = property(_get_votes)


class PitchData(models.Model):
	
	data = models.ForeignKey(Data, on_delete=models.CASCADE)
	num_vol = models.PositiveIntegerField(default=0)
	dev_start_date = models.DateField()
	app_close_date = models.DateField()

class DevData(models.Model):

	data = models.ForeignKey(Data, on_delete=models.CASCADE)
	git_url = models.URLField()




