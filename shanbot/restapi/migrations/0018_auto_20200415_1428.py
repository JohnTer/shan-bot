# Generated by Django 2.2.11 on 2020-04-15 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0017_auto_20200409_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='WrongAward',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=4100)),
                ('attachments_json', models.CharField(blank=True, default=None, max_length=4100, null=True)),
                ('extended_text', models.CharField(blank=True, default=None, max_length=4100, null=True)),
                ('extended_attachments_json', models.CharField(blank=True, default=None, max_length=4100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='wrong_award_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.WrongAward'),
        ),
    ]
