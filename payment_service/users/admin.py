from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from payment_service.payment_gateway.utils import generate_random_string
from payment_service.users.forms import UserAdminChangeForm, UserAdminCreationForm
from payment_service.users.models import ApplicationMaster

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(ApplicationMaster)
class ApplicationMasterAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "access_code",
        "redirect_url",
        "cancel_url",
        "is_active",
    ]
    readonly_fields = [
        "access_code",
        "working_key",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.access_code = generate_random_string(18)
            obj.working_key = generate_random_string(32)

        super().save_model(request, obj, form, change)
