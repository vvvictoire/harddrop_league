# Generated by Django 2.2.1 on 2019-06-06 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_only_site', '0007_auto_20190603_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='jstris_handle',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]