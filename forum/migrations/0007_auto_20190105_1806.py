# Generated by Django 2.1.3 on 2019-01-05 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20190105_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment_dongtai',
            name='nickname',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment_tiezi',
            name='nickname',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dongtai',
            name='nickname',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tiezi',
            name='nickname',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
