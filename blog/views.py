from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Post


def home(request):
    posts = Post.objects.filter(
        status="published",
        published_at__lte=timezone.now(),
    ).order_by("-published_at")

    context = {
        "posts": posts,
        "canonical_url": settings.SITE_URL,
        "meta_title": "The Berean Scale | Test Every Claim Against Scripture",
        "meta_description": (
            "The Berean Scale examines biblical claims, theology, "
            "Greek and Hebrew texts, and Scripture in context."
        ),
        "meta_type": "website",
    }

    return render(
        request,
        "blog/home.html",
        context,
    )


def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status="published",
        published_at__lte=timezone.now(),
    )

    canonical_url = f"{settings.SITE_URL}/{post.slug}/"

    social_image_url = None

    if post.featured_image:
        social_image_url = f"{settings.SITE_URL}" f"{post.featured_image.url}"

    context = {
        "post": post,
        "canonical_url": canonical_url,
        "meta_title": f"{post.title} | The Berean Scale",
        "meta_description": post.excerpt,
        "meta_type": "article",
        "social_image_url": social_image_url,
    }

    return render(
        request,
        "blog/post_detail.html",
        context,
    )


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain",
    )
