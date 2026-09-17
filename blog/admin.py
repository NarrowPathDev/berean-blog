from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "published_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "published_at",
    )

    search_fields = (
        "title",
        "excerpt",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    ordering = ("-published_at",)

    fieldsets = (
        (
            "Article",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "featured_image",
                    "content",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "status",
                    "published_at",
                )
            },
        ),
    )
