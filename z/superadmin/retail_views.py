from django.shortcuts import render
from django.http import HttpResponseRedirect
from z.retail.vendor.models import Vendor

def list(request):
	vendors = Vendor.objects.all()
	context = {'vendors': vendors}
	return render(request, 'superadmin/retail/list.html', context)

def detail(request, vid):
	vendor = Vendor.objects.get(id=vid)
	context = {'vendor': vendor}
	return render(request, 'superadmin/retail/detail.html', context)

def create(request):
	from z.superadmin.forms import CreateRetailerForm
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CreateRetailerForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			v = Vendor(name=form.cleaned_data['retailer_name'], login=form.cleaned_data['retailer_slug'])
			v.save()
			# redirect to a new URL:
			return HttpResponseRedirect('list')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = CreateRetailerForm()

	context = {"form": form}
	return render(request, 'superadmin/retail/create.html', context)
