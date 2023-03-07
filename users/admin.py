from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional info',
            {
                'fields':(
                    'role',
                    'mahalla',
                    'tuman',
                )
            }
        )
    )

fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields':('first_name', 'last_name', 'email', 'role', 'mahalla', 'tuman')})
CustomUserAdmin.fieldsets = tuple(fields)
admin.site.register(User, CustomUserAdmin)