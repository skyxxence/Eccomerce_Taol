from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_vendor', 'shop_name', 'shop_address')
    list_filter = ('is_vendor',)
    search_fields = ('username', 'email', 'shop_name')

# Register your models here.
