from django.contrib import admin
from .models import User, Contact

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name', 'last_name', 'phone_number', 'email']
    search_fields = ['username', 'phone_number']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'spam', 'spam_count', 'user']
    search_fields = ['name', 'phone_number']
