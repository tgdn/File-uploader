# -*- coding: utf-8 -*-

# django
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.timesince import timesince
from django.utils.translation import ugettext as _
from django.contrib.auth.models import *
import re,urllib,urllib2
from django.utils.html import escape

import uploader.settings as settings

register = template.Library()

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
