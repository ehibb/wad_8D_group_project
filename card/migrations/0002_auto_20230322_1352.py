# Generated by Django 2.2.28 on 2023-03-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.AlterField(
            model_name='flashcardset',
            name='subject',
            field=models.CharField(default='other', max_length=20),
        ),
    ]
