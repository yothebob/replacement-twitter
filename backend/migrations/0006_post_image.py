# Generated by Django 4.1.3 on 2022-11-25 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_account_post_color_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
