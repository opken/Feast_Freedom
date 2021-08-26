from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('is_kitchen', 'is_customer',)}),
)

class MyUserAdmin(UserAdmin):
    model = User

    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

admin.site.register(User, MyUserAdmin)