from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Notification, Responses


class NotificationSummernoteAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)


admin.site.register(Category)
admin.site.register(Notification, NotificationSummernoteAdmin)
admin.site.register(Responses)
