# Generated by Django 4.1.5 on 2023-01-20 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_rename_ad_fav_article_alter_fav_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content_type',
            field=models.CharField(blank=True, help_text='The MIMEType of the file', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='picture',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
    ]
