# Generated by Django 4.2.5 on 2023-11-20 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearningApp', '0006_alter_userprofile_options_alter_userprofile_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
