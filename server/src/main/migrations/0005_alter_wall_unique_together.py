# Generated by Django 4.1.5 on 2023-02-13 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_vkgroup_remove_vkuser_profile_type_alter_wall_user_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wall',
            unique_together={('user', 'group')},
        ),
    ]
