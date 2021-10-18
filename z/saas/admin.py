from django.contrib import admin
from z.saas.models import Account
from reversion.admin import VersionAdmin
#import reversion

class AccountAdmin(VersionAdmin):
	pass

admin.site.register(Account, AccountAdmin)