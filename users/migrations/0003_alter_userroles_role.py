# Generated by Django 5.0.2 on 2024-02-27 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_is_super_alter_userroles_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userroles',
            name='role',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
