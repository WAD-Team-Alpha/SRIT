# Generated by Django 3.1.5 on 2021-06-22 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phn_no',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='security_code',
            field=models.CharField(default=0, max_length=25),
            preserve_default=False,
        ),
    ]
