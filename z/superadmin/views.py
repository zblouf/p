from django.shortcuts import render

def main(request):
	context = {}
	return render(request, 'superadmin/main.html', context)
