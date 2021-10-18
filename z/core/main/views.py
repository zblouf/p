from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings

def root(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home')
	else:
		return HttpResponseRedirect(settings.LOGIN_URL)

def home(request):
	context = {}
	return render_to_response('main/home.html', context, context_instance=RequestContext(request))

def springboard(request):
	context = {}
	return render_to_response('main/springboard.html', context, context_instance=RequestContext(request))
