from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Post


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Post.objects.filter(
            status="published",
            published_at__lte=timezone.now(),
        ).order_by("-published_at")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse(
            "post_detail",
            kwargs={
                "slug": obj.slug,
            },
        )
