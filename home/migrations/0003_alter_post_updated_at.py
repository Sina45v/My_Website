# Generated by Django 5.1.5 on 2025-01-27 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
