from django.contrib import admin

from z.meta.idtag.models import IdTag

class IdTagAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'content_type', 'label', 'value')

admin.site.register(IdTag, IdTagAdmin)