from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Screenshot

admin.site.unregister(Group)
admin.site.unregister(User)


class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ['time', 'num', 'image']


admin.site.register(Screenshot, ScreenshotAdmin)
