from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.snippets.models import register_snippet

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class LogueIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Include only published posts, ordered in reverse chron
        context = super().get_context(request)
        logue = self.get_children().live().order_by("-first_published_at")
        context["logue"] = logue
        return context

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]


class LoguePageTag(TaggedItemBase):
    content_object = ParentalKey("LoguePage", related_name="tagged_items", on_delete=models.CASCADE)


class LogueTagIndexPage(Page):
    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get("tag")
        logue = LoguePage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["logue"] = logue
        return context


@register_snippet
class LogueCategory(models.Model):
    name = models.CharField(max_length=240)
    icon = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    panels = [FieldPanel("name"), ImageChooserPanel("icon")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "logue categories"


class LoguePage(Page):
    date = models.DateField("Post date")
    header_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=LoguePageTag, blank=True)
    categories = ParentalManyToManyField("logue.LogueCategory", blank=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.FilterField("date"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("date"), FieldPanel("tags"), FieldPanel("categories", widget=forms.CheckboxSelectMultiple)],
            heading="Logue information",
        ),
        ImageChooserPanel("header_image"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
        InlinePanel("gallery_images", label="Gallery images"),
        InlinePanel("related_links", label="Related links"),
    ]

    promote_panels = [ImageChooserPanel("feed_image")]


class LoguePageGalleryImage(Orderable):
    page = ParentalKey(LoguePage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(blank=True, max_length=250)

    panels = [ImageChooserPanel("image"), FieldPanel("caption")]


class LoguePageRelatedLink(Orderable):
    page = ParentalKey(LoguePage, on_delete=models.CASCADE, related_name="related_links")
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [FieldPanel("name"), FieldPanel("url")]
