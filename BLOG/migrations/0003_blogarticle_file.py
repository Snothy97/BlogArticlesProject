# Generated by Django 5.0.7 on 2024-09-15 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BLOG', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticle',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='blog_files/'),
        ),
    ]
