# Generated by Django 3.0.4 on 2020-05-19 05:50

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='article_text',
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Контент'),
        ),
    ]