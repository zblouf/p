from django.contrib import admin
from z.auth.zuser.models import ZUser

@admin.register(ZUser)
class ZUserAdmin(admin.ModelAdmin):
	list_display = ('account', 'user', 'user_type', 'is_admin', 'is_generic')
