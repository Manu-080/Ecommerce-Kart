from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.

class UserAdminManager(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login')
    list_display_links = ('email', 'first_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAdminManager)
