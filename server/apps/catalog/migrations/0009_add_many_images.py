# Generated by Django 3.2.18 on 2023-03-05 12:56


from django.db import migrations, models, transaction


def link_item_images_to_catalog_item(apps, schema):
    """Linking the ItemImages table to the gallery."""
    catalog_item = apps.get_model('catalog', 'catalogitem')
    item_image = apps.get_model('catalog', 'imageitem')

    with transaction.atomic():
        item_images = item_image.objects
        catalog_items = catalog_item.objects

        for product in catalog_items.filter(  # noqa: WPS352
            gallery__isnull=True,
        ):
            product.gallery.add(
                *item_images.filter(
                    product=product.id,
                ).values_list(
                    'id', flat=True,
                ),
            )


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0008_is_on_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogitem',
            name='gallery',
            field=models.ManyToManyField(
                to='catalog.ImageItem',
                verbose_name='gallery',
            ),
        ),
        migrations.RunPython(
            code=link_item_images_to_catalog_item,
        ),
    ]
