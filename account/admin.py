from django.contrib import admin
from .models import *


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'full_name', 'email', 'is_active', 'is_staff')
#     search_fields = ('full_name', 'email')
#     list_filter = ('is_active',)



admin.site.register(MyUser)
