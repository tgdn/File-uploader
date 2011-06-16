# -*- coding: utf-8 -*-

# django
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.timesince import timesince
from django.utils.translation import ugettext as _
from django.contrib.auth.models import *
import re,urllib,urllib2
from django.utils.html import escape

# placemeet
import uploader.settings as settings

register = template.Library()

def get_youtube_title(url, id):
	f=urllib.urlopen("http://youtube.com/v/%s" % id,'')
	tas=f.read()
	link=re.compile('<title>(.*)<\/title>')
	if link.search(tas):
		a= link.search(tas).group()
		url =  a.strip('[<title>,",</title>]')
	return url
		

def get_video_size(size):
	"""
		Returns video object width and height
	"""
	if size == "small":
		width = 350
		height = 230
	elif size == "medium":
		width = 425
		height = 344
	elif size == "big":
		width = 661
		height = 400
	else:
		width = 350
		height = 230
	return [width, height]

def get_youtube(value, video_id, size):
	"""
		Return youtube object
	"""
	width = get_video_size(size)[0]
	height = get_video_size(size)[1]
	video_key = keygen()
	value = """
	%s
	<span class="post_line"></span>
	<a href="#" class="watch_video_link" onclick="Posts.show_video('%s');return false;">%s</a>
	<div class="video video_num_%s" style="display:none;">
		<object type="application/x-shockwave-flash" width="%s" height="%s" data="http://www.youtube.com/v/%s">
			<param name="movie" value="http://www.youtube.com/v/%s" />
			<param value="true" name="allowFullScreen" />
			<param name="wmode" value="transparent" />
		</object>
		<!--[if lte IE 6 ]>
			<embed src="http://www.youtube.com/v/_%s" type="application/x-shockwave-flash" wmode="transparent" width="%s" height="%s"></embed>
		<![endif]-->
	</div>
	""" % (value, video_key, _('Watch the video'), video_key, width, height, video_id, video_id, video_id, width, height)
	
	return value


@register.filter
@stringfilter
def youtube(value, arg):
	"""
		Check if there are any youtube links
	"""
	regex = re.compile(r"(.*)(https?://)?(www\.)?(youtube\.com/watch\?v=)(?P<id>[A-Za-z0-9\-=_]{11})(.*)")
	match = regex.match(value)
	if not match:
		return value
	else:
		video_id = match.group('id')
		value = get_youtube(value, video_id, size=arg)
	return value
youtube.is_safe = True # Don't escape HTML

def check_user(user):
	try:
		int(user)
		is_int = True
	except:
		is_int = False
		
	if is_int:
		try:
			user_data = User.objects.get(id=user)
		except User.DoesNotExist:
			try:
				user_data = User.objects.get(username=user)
			except User.DoesNotExist:
				return False
	else:
		try:
			user_data = User.objects.get(username=user)
		except User.DoesNotExist:
			return False
	
	return user_data

def make_friend_link(user):
	try:
		user = str(user)
	except:
		pass
	if check_user(user):
		old = user
		user = check_user(user)
		return '<a href="/profile/%s">@%s</a>' % (user.username, old)
	else:
		return '@%s' % user

def create_smileys(value):
	"""
		Value must be escaped first
	"""
	value = re.sub(r'\:\)', '<img src="%simg/emoticons/emoticon_smile.png" class="emoticon"/>' % settings.MEDIA_URL_NORMAL, value)
	value = re.sub(r'\:D', '<img src="%simg/emoticons/emoticon_grin.png" class="emoticon"/>' % settings.MEDIA_URL_NORMAL, value)
	value = re.sub(r'\;\)', '<img src="%simg/emoticons/emoticon_wink.png" class="emoticon"/>' % settings.MEDIA_URL_NORMAL, value)
	value = re.sub(r'\:P', '<img src="%simg/emoticons/emoticon_tongue.png" class="emoticon"/>' % settings.MEDIA_URL_NORMAL, value)
	value = re.sub(r'\:3', '<img src="%simg/emoticons/emoticon_waii.png" class="emoticon"/>' % settings.MEDIA_URL_NORMAL, value)
	value = re.sub(r'\:\(', '<img src="%simg/emoticons/emoticon_unhappy.png" class="emoticon"/>' % settings.MEDIA_URL_NORMAL, value)
	value = re.sub(r'\(phone\)', '<img src="%simg/emoticons/emoticon_mobile.png" class="emoticon emoticon_phone"/>' % settings.MEDIA_URL_NORMAL, value)
	return value
	
def create_special_chars(value):
	"""
		Value must be escaped first
	"""
	value = re.sub(r'\((L|l|hearts)\)', '&hearts;', value)
	value = re.sub(r'\((spades)\)', '&spades;', value)
	value = re.sub(r'\((clubs)\)', '&clubs;', value)
	value = re.sub(r'\((diams)\)', '&diams;', value)
	value = re.sub(r'\((trade)\)', '&trade;', value)
	return value

def create_links(value):
	"""
		Value must be escaped first
	"""
	#value = re.sub(r"[\W| |\s]\#((.+))", '<a href="/search/?q=\\1">#\\1</a>', value)
	#value = re.sub(r'\@([^ |^\n]+)', make_friend_link('\\1'), value)
	#regex = re.compile(r"\W\#(?P<link>(.+))\W")
	#match = regex.match(value)
	
	return value

def do_get_img(value, url):
	value = """
	%s
	<span class="post_line"></span>
	%s
	<img src="%s" alt="post_img" class="post_img" />
	""" % (value, url, url)

def get_post_img(value):
	"""
		Get img from urls if there are
	"""
	regex = re.compile(r"(.*)(?P<url>(https?://)?(www\.)?[a-z0-9._-]{2,}\.[a-z]{2,4}\/(.+)\.[jpg|jpeg|png|gif])(.*)")
	match = regex.match(value)
	if match:
		url = match.group('url')
		try:
			f=urllib.urlopen(url)
			exists=f.read()
		except IOError:
			exists = False
		if exists:
			value = do_get_img(value, url)
		
	return value

@register.filter
def edit_post(value):
	"""
		Create smileys, links to profiles and to searchs results → Escapes the value first
	"""
	value = escape(value)
	value = create_smileys(value)
	value = create_special_chars(value)
	value = create_links(value)
	#value = get_post_img(value)
	
	return value
edit_post.is_safe = True # Don't escape HTML

@register.filter
def edit_post_no_smileys(value):
	"""
		Create links to profiles and to searchs results → Escapes the value first
	"""
	value = escape(value)
	value = create_special_chars(value)
	value = create_links(value)
	
	return value
edit_post_no_smileys.is_safe = True # Don't escape HTML

@register.filter
def naturalTimeDifference(value):
	"""
	Returns appropriate humanize time. ex: "about 7 minutes ago"
	"""
	ago = timesince(value)
	ret = ago.split(",")[0]
	if ret == _('0 minutes') or ret == _('0 minute'):
		return _('just now')
	else:
		since = ago.split(",")[0]
		about = _('about ')
		ago = _(' ago')
		return about + since + ago
		
		
class PpicUrlNode(template.Node):
	def __init__(self, user, size, className=None):
		self.user = template.Variable(user)
		self.size = str(size)
		if className is not None:
			self.className = str(className)
		else:
			self.className = False

	def render(self, context):
		user = self.user.resolve(context)
		default = 'default.png'
		
		user_data = check_user(user)
		if user_data:
			person = Person.objects.get(user=user_data.id)
			if person.photo:
				if self.size == 'small':
					ppic = person.photo.small.name
				elif self.size == 'medium':
					ppic = person.photo.medium.name
				else:
					ppic = person.photo.normal.name
			else:
				ppic = default
				
			src = "%s%s" % (settings.MEDIA_URL, ppic.replace('uploads/', ''))

			if self.className:
				data = '<img src="%s" alt="%s" class="%s" />' % (src, user_data.username, self.className)
			else:
				data = '<img src="%s" alt="%s" />' % (src, user_data.username)
			return data
		else:
			return user

@register.tag
def get_ppic(parser, token):
	"""
		You can use this tag with user's username or user's id
		examples:	
			{% get_ppic user.id %} == {% get_ppic user.username %}
			{% get_ppic user.id small %}		→		<img src="thumb_small_ppic.png" alt="username" />
			{% get_ppic user.id small myclass %}		→		<img src="thumb_small_ppic.png" alt="username" class="myclass" />
	"""
	bits = token.contents.split()
	try:
		str(bits[3])
		return PpicUrlNode(bits[1], bits[2], bits[3])
	except:
		return PpicUrlNode(bits[1], bits[2])


class JsUrlNode(template.Node):
	def __init__(self, directory):
		self.dir = template.Variable(directory)

	def render(self, context):
		_dir_ = self.dir.resolve(context)
		js = '<script type="text/javascript" src="%s"></script>' % _dir_
		return js

@register.tag
def get_js(parser, token):
	"""
		examples:	
			{% get_js /public/js/index.js %}
	"""
	bits = token.contents.split()
	return JsUrlNode(bits[1])


class CssUrlNode(template.Node):
	def __init__(self, directory):
		self.dir = template.Variable(directory)

	def render(self, context):
		_dir_ = self.dir.resolve(context)
		link = '<link rel="stylesheet" href="%s" type="text/css" media="all" />' % _dir_
		return link

@register.tag
def get_css(parser, token):
	"""
		examples:	
			{% get_css /public/css/index.css %}
	"""
	bits = token.contents.split()
	return CssUrlNode(bits[1])



# ----------------
class JsStartNode(template.Node):

	def render(self, context):
		return '<script type="text/javascript">//<![CDATA['

@register.tag
def js(parser, token):
	"""
		examples:	
			{% js %}
			{% endjs %}
	"""
	bits = token.contents.split()
	return JsStartNode()

class JsEndNode(template.Node):

	def render(self, context):
		return '//]]></script>'

@register.tag
def endjs(parser, token):
	"""
		examples:	
			{% js %}
			{% endjs %}
	"""
	bits = token.contents.split()
	return JsEndNode()
