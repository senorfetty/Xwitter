# Generated by Django 5.0.2 on 2024-03-22 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatter', '0031_alter_comment_tags_alter_post_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tags',
            new_name='name',
        ),
    ]
