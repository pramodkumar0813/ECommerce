from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# 1. Custom User Model can register
# Custom User Model (AbstractBaseUser) can we using so, Admin also we can Customize
class UserAdmin(BaseUserAdmin):
    # display fields on the list page
    list_display = ('phone', 'first_name', 'last_name', 'is_staff', 'is_profile_complete') 
    # fields that can be searched
    search_fields = ('phone', 'first_name', 'email')
    # fields for adding/changing a user
    ordering = ('phone',)
    
    # Custom Fieldsets (we can use or other wise leave)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'is_profile_complete')}),
        ('Address', {'fields': ('address_line_1', 'street_name', 'city', 'state', 'pincode')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# 2.we can register model here
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)