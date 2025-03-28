from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Chat Details",
            {
                "fields": ("user", "prompt", "response"),
                "classes": ("wide",),
            },
        ),
        (
            "Additional Information",
            {
                "fields": ("table", "chart"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("user", "prompt_summary", "response_summary", "created_at", "updated_at")
    list_filter = ("user", "created_at")
    search_fields = ("user__username", "prompt", "response")

    def prompt_summary(self, obj):
        return obj.prompt[:50]
    prompt_summary.short_description = "Prompt Summary"

    def response_summary(self, obj):
        return obj.response[:50]
    response_summary.short_description = "Response Summary"
