# Generated by Django 5.0.1 on 2024-01-19 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='userimage',
            field=models.ImageField(default='', upload_to='bloguser/images'),
        ),
    ]
