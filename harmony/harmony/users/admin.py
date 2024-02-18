from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from harmony.users.forms import UserAdminChangeForm
from harmony.users.forms import UserAdminCreationForm
from harmony.users.models import Member

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


#register the user model

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    list_display = ["email", "is_active", "is_staff", "is_superuser"]

    #remove date_joined from change form
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login",)}),
        ("Additional Information", {"fields": ("avatar", "type")}),
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["user", "prn_number", "first_name", "last_name", "date_of_birth"]
    search_fields = ["user__username", "user__email", "prn_number", "first_name", "last_name"]
    list_filter = ["user__is_active", "user__is_staff", "user__is_superuser"]
    ordering = ["-user__date_joined"]
    fieldsets = (
        (None, {"fields": ("user", "prn_number")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "date_of_birth")}),
    )

