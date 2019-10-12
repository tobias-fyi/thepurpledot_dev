from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class LogueIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]


class LoguePage(Page):
    date = models.DateField("Post date")
    header_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.FilterField("date"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        ImageChooserPanel("header_image"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
    ]

    promote_panels = [ImageChooserPanel("feed_image")]

