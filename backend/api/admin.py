from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Resume, Favorite, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['login', 'name', 'surname', 'role', 'company', 'created_at']
    list_filter = ['role', 'auth_method']
    search_fields = ['login', 'name', 'surname', 'email']
    ordering = ['-created_at']
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Личные данные', {'fields': ('name', 'surname', 'patronymic', 'email', 'phone', 'address')}),
        ('Роль', {'fields': ('role', 'company', 'auth_method')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2', 'name', 'surname', 'role'),
        }),
    )


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'profession', 'level', 'city', 'experience_years', 'created_at']
    list_filter = ['profession', 'level', 'city', 'has_bachelor', 'has_master']
    search_fields = ['name', 'surname', 'user__login']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['employer', 'resume', 'created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    list_filter = ['is_read']
