# Generated by Django 3.1.3 on 2021-04-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ECommerceApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='added_by_admin',
            field=models.BooleanField(default=False),
        ),
    ]