# Generated by Django 4.2.2 on 2023-09-08 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faces_app', '0002_class_user_klass'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
