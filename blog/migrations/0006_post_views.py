# Generated by Django 5.0 on 2024-11-13 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_main_description_post_meta_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
