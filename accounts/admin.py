# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from .models import UserProfile, MemberResource


# -------------------------------
# Inline UserProfile inside User
# -------------------------------
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )


# Replace the default User admin with our custom version
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# -------------------------------
# UserProfile Admin
# -------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "get_email",
        "verified",
        "business_name",
        "business_type",
        "business_location",
        "target_audience",
        "get_date_joined",
        "account_age",
    )
    list_filter = ("verified", "business_type", "business_location")
    search_fields = (
        "user__username",
        "user__email",
        "business_name",
        "business_type",
        "business_location",
        "target_audience",
    )

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email"

    def get_date_joined(self, obj):
        return obj.user.date_joined

    get_date_joined.short_description = "Date Joined"

    def account_age(self, obj):
        return timesince(obj.user.date_joined).split(",")[0]

    account_age.short_description = "Account Age"


# -------------------------------
# Member Resources Admin
# -------------------------------
@admin.register(MemberResource)
class MemberResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_active", "order")
    list_editable = ("order",)
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    ordering = ("order",)
