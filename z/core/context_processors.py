from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings

#from z.saas.models import Account

def z_context(request):
	_account = None
	_eid = None
	_entity = None
	_aid = None
	_activity = None
	_authorized_ent = None
	_authorized_apps = []
	_units = []
	_activities = []

	#load user pofile
	

	return {
		'settings': settings,
	}

def base_template(request):
	_bt = settings.DEFAULT_BASE_TEMPLATE
	return {'BASE_TEMPLATE': _bt}
