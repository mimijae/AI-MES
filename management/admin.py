from django.contrib import admin
from .models import Organization, OrganizationMember

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Organization Information", {
            "fields": ("name", "description", "organization_type", "contact_email", "contact_phone", "address", "created_by"),
        }),
    )
    list_display = ("name", "organization_type", "contact_email", "created_by")
    list_filter = ("organization_type",)
    search_fields = ("name", "contact_email")

@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Membership Information", {
            "fields": ("organization", "user", "role"),
        }),
    )
    list_display = ("user", "organization", "role")
    list_filter = ("role", "organization")
    search_fields = ("user__username", "organization__name")
    raw_id_fields = ("user",)