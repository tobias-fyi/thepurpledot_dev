# Generated by Django 2.2.6 on 2019-10-21 21:42

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [("logue", "0010_auto_20191021_2100")]

    operations = [
        migrations.AlterField(
            model_name="loguepage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    ("heading", wagtail.core.blocks.CharBlock(classname="full title")),
                    ("paragraph", wagtail.core.blocks.RichTextBlock()),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                ],
                null=True,
            ),
        )
    ]
