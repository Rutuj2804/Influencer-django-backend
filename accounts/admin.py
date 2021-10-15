from django.contrib import admin
from accounts.models import Account, Link, Skill
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(Link)
admin.site.register(Skill)