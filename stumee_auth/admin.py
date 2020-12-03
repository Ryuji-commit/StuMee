from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CertificationPass, CustomUser

# Register your models here.
admin.site.register(CertificationPass)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'last_login', 'user_auth', 'is_certificated')
    fieldsets = (
        (None, {'fields': [('username',), ]}),
        (None, {'fields': [('user_auth',), ]}),
        ('ログイン時認証', {'fields': [('is_certificated',), ]}),
        ('権限', {'fields': ('is_active',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)