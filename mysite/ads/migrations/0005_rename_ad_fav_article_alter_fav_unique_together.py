# Generated by Django 4.1.5 on 2023-01-20 20:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0004_fav_article_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fav',
            old_name='ad',
            new_name='article',
        ),
        migrations.AlterUniqueTogether(
            name='fav',
            unique_together={('article', 'user')},
        ),
    ]