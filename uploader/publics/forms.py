# -*- coding: utf-8 -*-

# python
import hashlib

# django
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

# placemeet
from django.contrib.auth.models import *
from uploader.publics.models import File


class PhotoForm(ModelForm):
	class Meta:
		model = File
		fields = ('file',)
		
	def clean_file(self):
		# Safe copy of data...
		self.cleaned_data['file'].seek(0)
		data = self.cleaned_data['file'].read()
		self.cleaned_data['file'].seek(0)
		
		return self.cleaned_data['file']
