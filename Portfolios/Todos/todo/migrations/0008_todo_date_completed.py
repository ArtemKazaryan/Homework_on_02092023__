# Generated by Django 4.2.4 on 2023-09-01 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_todo_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]