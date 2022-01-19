# Generated by Django 3.0.4 on 2020-10-05 07:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_comment_comment_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата комментария'),
        ),
    ]