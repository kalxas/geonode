# Generated by Django 2.2.24 on 2022-04-08 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0033_upload_store_spatial_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='layer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layers.Layer'),
        ),
    ]