# Generated by Django 2.2.11 on 2020-04-04 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0006_auto_20200404_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='solving_mode',
            field=models.BooleanField(default=False),
        ),
    ]
