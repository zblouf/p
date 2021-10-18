from django.shortcuts import render
from django.http import HttpResponseRedirect

def home(request):
	context = {}
	return render(request, 'superadmin/import/home.html', context)

