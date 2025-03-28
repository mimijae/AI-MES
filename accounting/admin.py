from django.contrib import admin
from .models import Accounting  # Transaction → Accounting

@admin.register(Accounting)  # Transaction → Accounting
class AccountingAdmin(admin.ModelAdmin):  # TransactionAdmin → AccountingAdmin
    fieldsets = (
        (
            "Accounting Details",  # Transaction Details → Accounting Details
            {
                "fields": (
                    "organization",
                    "accounting_type",  # transaction_type → accounting_type
                    "amount",
                    "payment_method",
                    "accounting_date",  # transaction_date → accounting_date
                    "description",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Handled By",
            {
                "fields": ("handled_by",),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("organization", "accounting_type", "amount", "accounting_date", "payment_method", "handled_by")  # transaction_type → accounting_type, transaction_date → accounting_date
    list_filter = ("organization", "accounting_type", "payment_method")  # transaction_type → accounting_type
    search_fields = ("description", "handled_by__username")
