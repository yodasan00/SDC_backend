from django.contrib import admin
from .models import User, Department, Domain


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('value', 'display')
    search_fields = ('value', 'display')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'department_name', 'domain', 'is_staff')
    list_filter = ('role', 'department_name', 'domain')
    search_fields = ('username', 'email')
