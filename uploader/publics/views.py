import json
from random import choice

from django.http import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext

from uploader import settings
from uploader.publics.forms import PhotoForm
from uploader.publics.models import File

@csrf_protect
def index(request):
	files = File.objects.all()
	return render_to_response('index.html', {'files':files, 'form':PhotoForm()}, context_instance=RequestContext(request))

@csrf_exempt
def upload(request):
	if request.method != 'POST':
		return HttpResponseRedirect('/')
	
	photoForm = PhotoForm(request.POST, request.FILES)
	if photoForm.is_valid():
		photoForm.save()
	#
	if request.is_ajax():
	
#		for file in request.POST:
#			name = request.GET.get('qqfile', 'some_name')
#			url = '%s/uploads/' % settings.MEDIA_ROOT
#			destination = open('%s%s' % (url, name), 'wb+')
#			for chunk in file.chunks():
#				destination.write(chunk)
#			destination.close()
		image = request.raw_post_data
		name = request.GET.get('qqfile', 'some_name')
		url = '%s/uploads/' % settings.MEDIA_ROOT
		
#		Looking if image with same name exists {
		try:
			d = open('%s%s' % (url, name), 'r')
			key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPKRSTUVWXYZ@$%&-_=+') for i in range(8)])
			name = '%s_%s' % (key, name)
		except IOError:
			pass
#		}

#		Writing image {
		destination = open('%s%s' % (url, name), 'wb+')
		destination.write(image)
		destination.close()
#		}

		url = '/media/uploads/'
		dir = '%s%s' % (url, name)
		output = {'success':1, 'image':name, 'url':dir}
		
		# Save in database
		f = File(file="uploads/%s" % name)
		f.save()
		
		return HttpResponse(json.dumps(output))
	return HttpResponseRedirect('/')

@csrf_exempt
def delete(request):
	if request.is_ajax():
		file = File.objects.all()
		for f in file:
		  f.delete()
		  for upload in os.listdir("%s/uploads/" % settings.MEDIA_ROOT):
		  	os.remove("%s/uploads/%s" % (settings.MEDIA_ROOT, upload))
		return HttpResponse('')
	else:
		return HttpResponseRedirect('/')
