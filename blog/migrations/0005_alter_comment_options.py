# Generated by Django 3.2.6 on 2021-08-27 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comment_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-createdOn']},
        ),
    ]
