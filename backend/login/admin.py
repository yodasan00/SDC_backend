from django.contrib import admin
from .models import User, Department, Domain
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('value', 'display')
    search_fields = ('value', 'display')


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'role', 'department_name', 'domain', 'is_staff')
#     list_filter = ('role', 'department_name', 'domain')
#     search_fields = ('username', 'email')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Inheriting from BaseUserAdmin ensures password hashing
    list_display = ('username', 'email', 'phone_number', 'role', 'department_name', 'domain', 'is_staff')
    list_filter = ('role', 'department_name', 'domain')
    search_fields = ('username', 'email', 'phone_number')

    # Add your custom fields (role, department_name, etc.) to the fieldsets
    # so they appear when editing a user
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'role', 'department_name', 'domain',)}),
    )

    # Add custom fields to the user creation page
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'role', 'department_name', 'domain')}),
    )