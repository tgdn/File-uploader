from django.db import models
import datetime

class File(models.Model):
	file = models.FileField(upload_to='uploads')
	timestamp = models.DateTimeField(default=datetime.datetime.now)
	
	def __unicode__(self):
	  return self.file.name
	
	def image(self):
		return '<img src="%s" alt="" />' % self.file.file
