# Generated by Django 2.1.3 on 2018-12-17 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment_Dongtai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('create_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Tiezi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('create_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dongtai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('create_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tiezi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=1000)),
                ('create_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('sex', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('department', models.IntegerField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='comment_tiezi',
            name='tiezi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Tiezi'),
        ),
        migrations.AddField(
            model_name='comment_dongtai',
            name='dongtai',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Dongtai'),
        ),
    ]
