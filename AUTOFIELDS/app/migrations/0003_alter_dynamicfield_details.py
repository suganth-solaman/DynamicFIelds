# Generated by Django 4.2.1 on 2023-06-04 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_forms_details_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicfield',
            name='details',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.forms'),
        ),
    ]