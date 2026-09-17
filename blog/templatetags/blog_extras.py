import bleach
import markdown

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdownify(value):
    if not value:
        return ""

    html = markdown.markdown(
        value,
        extensions=[
            "extra",
            "sane_lists",
        ],
    )

    allowed_tags = [
        "p",
        "h2",
        "h3",
        "h4",
        "strong",
        "em",
        "blockquote",
        "ul",
        "ol",
        "li",
        "a",
        "code",
        "pre",
        "hr",
        "br",
    ]

    allowed_attributes = {
        "a": [
            "href",
            "title",
        ],
    }

    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=[
            "http",
            "https",
            "mailto",
        ],
        strip=True,
    )

    return mark_safe(clean_html)
