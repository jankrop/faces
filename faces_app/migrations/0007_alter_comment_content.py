# Generated by Django 4.2.2 on 2023-09-22 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faces_app', '0006_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=1024),
        ),
    ]
