# Generated by Django 3.1 on 2020-09-01 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200901_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
