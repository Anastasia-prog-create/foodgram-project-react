# Generated by Django 2.2.19 on 2022-05-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220505_1319'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscribe',
            name='unique follow',
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'subscriber'), name='unique subscribe'),
        ),
    ]
