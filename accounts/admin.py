from django.contrib import admin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    list_filter = ('is_staff', 'is_active')
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    ordering = ('username', 'email')
    
admin.site.register(CustomUser, CustomUserAdmin)
    
    