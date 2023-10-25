from .models import User,Profile,Location
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm,UserChangeForm,UserCreationForm


class CustomUserAdmin(UserAdmin):
    # form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    model = User
    list_display = ("phone_number", "is_staff", "is_active",'email')
    list_filter = ("phone_number", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone_number', 'first_name', 'last_name', 'other_name', 'password1', 'password2','slug')
        }),
    )
    change_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone_number', 'first_name', 'last_name', 'other_name' ,'password1', 'password2','slug')
        }),
    )
    search_fields = ("phone_number",'email')
    ordering = ("phone_number",'email','-first_name','-last_name')


    @admin.action(description="Ban selected users")
    def ban_users(self, request, queryset):
        # Update the selected users to be inactive
        queryset.update(is_active=False)
    
    @admin.action(description="Unban selected users")
    def un_ban_users(self, request, queryset):
        # Update the selected users to be active
        queryset.update(is_active=True)

    actions = [ban_users,un_ban_users]


admin.site.register(User,CustomUserAdmin)


class CustomProfileAdmin(admin.ModelAdmin):
    list_display=['profile_picture_tag','username','gender','is_varified']
admin.site.register(Profile,CustomProfileAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ['id','country','state']
admin.site.register(Location,LocationAdmin)