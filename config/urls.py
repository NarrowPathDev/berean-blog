from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import PostSitemap, StaticViewSitemap
from blog.views import robots_txt

sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        robots_txt,
        name="robots_txt",
    ),
    path("", include("blog.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
