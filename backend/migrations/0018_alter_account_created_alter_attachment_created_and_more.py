# Generated by Django 4.1.3 on 2023-04-23 20:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_attachment_ext_alter_account_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 23, 20, 45, 5, 150944)),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 23, 20, 45, 5, 150668)),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 23, 20, 45, 5, 154070)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 23, 20, 45, 5, 155455)),
        ),
        migrations.AlterField(
            model_name='message',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 23, 20, 45, 5, 153191)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 23, 20, 45, 5, 152135)),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime(2023, 4, 23, 20, 45, 5, 155112))),
                ('notification_id', models.CharField(default='0', max_length=20)),
                ('message', models.CharField(default='this is a notification', max_length=200)),
                ('From', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='made_notifications', to='backend.account')),
                ('To', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to='backend.account')),
            ],
        ),
    ]