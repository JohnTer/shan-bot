# Generated by Django 2.2.11 on 2020-04-04 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0003_auto_20200404_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='award_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.Award'),
        ),
    ]
