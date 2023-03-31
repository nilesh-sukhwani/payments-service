from django import forms
from django.contrib import admin
from django.contrib.admin import register

from payment_service.payment_gateway.models import ServiceProvider, Transaction
from payment_service.users.models import ApplicationMaster


class ApplicationChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"Application: {obj.name}"


class ServiceProviderChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"Service Provider: {obj.name}"


# Register your models here.
@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ("tracking_id", "order_id")

    readonly_fields = ("order_status", "payment_mode")

    list_display = (
        "id",
        "order_id",
        "tracking_id",
        "order_status",
        "created_at",
        "get_application_name",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "application_fk":
            return ApplicationChoiceField(queryset=ApplicationMaster.objects.all())
        if db_field.name == "service_provider_fk":
            return ServiceProviderChoiceField(queryset=ServiceProvider.objects.all())

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(ordering="-application_fk", description="Application")
    def get_application_name(self, obj):
        return obj.application_fk.name if obj.application_fk else None


@register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "contact_person_name",
        "contact_person_email",
        "is_active",
    )
