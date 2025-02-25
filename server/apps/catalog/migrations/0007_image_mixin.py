# Generated by Django 3.2.18 on 2023-03-02 19:46

import sorl.thumbnail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_rename_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogitem',
            name='main_image',
            field=sorl.thumbnail.fields.ImageField(
                null=True,
                upload_to='images',
                verbose_name='image',
            ),
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='image',
            field=sorl.thumbnail.fields.ImageField(
                null=True,
                upload_to='images',
                verbose_name='image',
            ),
        ),
        migrations.RenameField(
            model_name='catalogitem',
            old_name='main_image',
            new_name='image',
        ),
    ]
