# Generated by Django 3.1.12 on 2021-06-20 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='url',
            field=models.URLField(max_length=255, null=True),
        ),
    ]