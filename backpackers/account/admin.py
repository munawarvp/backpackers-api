from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active')
    readonly_fields = ('last_login', 'date_joined')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_img.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(User, UserAdmin) 
admin.site.register(UserProfile, UserProfileAdmin) 