# Generated by Django 3.0.6 on 2020-05-10 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_finance_api', '0008_auto_20200509_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membermodel',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='membermodel',
            name='last_updated_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='organizationmodel',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]
