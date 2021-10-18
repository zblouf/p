from django.shortcuts import render
from django.http import HttpResponseRedirect
from z.prev.domain.models import Sector, Domain
from z.superadmin import superadmin_menus as menus


def home(request):
	context = {'DB_MENU': menus.DB_MENU}
	return render(request, 'superadmin/db/home.html', context)

def common(request):
	context = {'DB_MENU': menus.DB_MENU}
	return render(request, 'superadmin/db/common/home.html', context)

def prev(request):
	context = {'DB_MENU': menus.DB_MENU}
	return render(request, 'superadmin/db/prev/home.html', context)

def domains_home(request):
	context = {'sectors': Sector.objects.all()}
	return render(request, 'superadmin/db/domains/home.html', context)
