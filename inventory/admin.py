from django.contrib import admin
from .models import Category, Item  # Supplier 임포트 제거

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Category Information", {
            "fields": ("name", "description"),
        }),
    )
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Item Information", {
            "fields": (
                "name", "category", "quantity", "price_per_unit", 
                "received_date", "expiration_date", 
                "status", "organization", "created_by"
            ),
        }),
    )
    list_display = ("name", "category", "quantity", "price_per_unit", "status", "organization", "created_by")
    list_filter = ("category", "status", "organization")
    search_fields = ("name",)  # 괄호 추가 (이전 코드에서 누락됨)
