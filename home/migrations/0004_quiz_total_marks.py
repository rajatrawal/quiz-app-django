# Generated by Django 4.1.4 on 2023-04-01 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='total_marks',
            field=models.IntegerField(default=0),
        ),
    ]
