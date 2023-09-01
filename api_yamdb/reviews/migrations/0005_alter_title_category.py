# Generated by Django 3.2 on 2023-08-30 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230830_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.category', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]