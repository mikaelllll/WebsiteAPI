# Generated by Django 2.2.7 on 2019-12-04 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='deleteDate',
            field=models.DateTimeField(blank=True, default=False, null=True),
        ),
    ]
