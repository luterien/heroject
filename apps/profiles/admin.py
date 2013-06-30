from apps.profiles.models import *
from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'date_joined')

admin.site.register(Profile, ProfileAdmin)
