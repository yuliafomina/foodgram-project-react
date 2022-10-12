from django.conf import settings
from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username',
        'first_name', 'last_name',)
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'author',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
