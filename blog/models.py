from django.db import models
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
    )

    excerpt = models.TextField(
        blank=True,
        help_text="Short description shown on the homepage and search engines.",
    )

    featured_image = models.ImageField(
        upload_to="featured/",
        blank=True,
        null=True,
    )

    content = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )

    published_at = models.DateTimeField(
        default=timezone.now,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
