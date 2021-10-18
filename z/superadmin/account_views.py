from django.shortcuts import render
from django.http import HttpResponseRedirect
from z.saas.models import Account

def list(request):
	context = {'accounts': Account.objects.all()}
	return render(request, 'superadmin/account/list.html', context)

def detail_home(request, aid):
	from z.core.app.models import App, AppRegistration
	context = {
		'account': Account.objects.get(pk=aid),
		'apps': App.objects.all()

		}
	return render(request, 'superadmin/account/detail_home.html', context)

def detail_apps(request, aid):
	from z.core.app.models import App, AppRegistration
	context = {
		'account': Account.objects.get(pk=aid),
		'apps': App.objects.all()

		}
	return render(request, 'superadmin/account/detail_apps.html', context)

def detail_entities(request, aid):
	from z.core.app.models import App, AppRegistration
	context = {
		'account': Account.objects.get(pk=aid),
		'apps': App.objects.all()

		}
	return render(request, 'superadmin/account/detail_entities.html', context)


def create(request):
	from z.superadmin.forms import CreateAccountForm
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CreateAccountForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			from django.contrib.auth.models import User
			from z.auth.zuser.models import ZUser
			from z.core import zutils
			# process the data in form.cleaned_data as required
			a, created = Account.objects.get_or_create(name=form.cleaned_data['account_name'], login=form.cleaned_data['account_slug'])
			if created:
				a.save()
			full_username = zutils.full_username(form.cleaned_data['admin_login'], a)
			u = User.objects.create_user(full_username, form.cleaned_data['admin_email'], form.cleaned_data['admin_pass'])
			zu, created = ZUser.objects.get_or_create(user=u, is_admin=True)
			zu.account = a
			zu.save()
			# redirect to a new URL:
			return HttpResponseRedirect('list')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = CreateAccountForm()

	context = {"form": form}
	return render(request, 'superadmin/account/create.html', context)
