# Generated by Django 3.2.17 on 2023-02-24 11:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import server.apps.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogCategory',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),
                ('name', models.CharField(
                    help_text='Максимальная длина 150',
                    max_length=150,
                    verbose_name='название',
                )),
                ('is_published', models.BooleanField(
                    default=True,
                    verbose_name='опубликовано',
                )),
                ('slug', models.SlugField(
                    max_length=200,
                    unique=True,
                    validators=[
                        django.core.validators.RegexValidator(
                            '^[0-9-_a-zA-Z]+$',
                        ),
                    ],
                )),
                ('weight', models.IntegerField(
                    default=100,
                    help_text='Вес должен быть больше 0 и меньше 32767',
                    validators=[
                        django.core.validators.MinValueValidator(0),
                        django.core.validators.MaxValueValidator(32767),
                    ],
                    verbose_name='вес',
                )),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='CatalogTag',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),
                ('name', models.CharField(
                    help_text='Максимальная длина 150',
                    max_length=150,
                    verbose_name='название',
                )),
                ('is_published', models.BooleanField(
                    default=True,
                    verbose_name='опубликовано',
                )),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='CatalogItem',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),
                ('name', models.CharField(
                    help_text='Максимальная длина 150',
                    max_length=150,
                    verbose_name='название',
                )),
                ('is_published', models.BooleanField(
                    default=True,
                    verbose_name='опубликовано',
                )),
                ('text', models.TextField(
                    help_text=(
                        '\nОписание должно быть больше чем из 2x слов' +
                        ' и содержать слова "превосходно, роскошно"\n'
                    ),
                    validators=[server.apps.core.validators.is_contains],
                    verbose_name='описание',
                )),
                ('category', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='catalog.catalogcategory',
                    verbose_name='категории',
                )),
                ('tags', models.ManyToManyField(
                    to='catalog.CatalogTag',
                    verbose_name='теги',
                )),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
