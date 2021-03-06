# Generated by Django 3.0.5 on 2020-04-10 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coviddb', '0005_infectedperson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infectedperson',
            name='announce_date',
            field=models.CharField(default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='city_no',
            field=models.CharField(default='', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='close_contact',
            field=models.CharField(default='', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='cluster_location',
            field=models.CharField(default='', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='cluster_name',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='death_date',
            field=models.CharField(default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='full_presentation',
            field=models.CharField(default='', max_length=8096, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='infected_date',
            field=models.CharField(default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='living_city',
            field=models.CharField(default='', max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='living_state',
            field=models.CharField(default='', max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='occupation',
            field=models.CharField(default='', max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='rel_close_contact',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='remarks',
            field=models.CharField(default='', max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='status',
            field=models.CharField(default='', max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='symptoms',
            field=models.CharField(default='', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='infectedperson',
            name='travel_destination',
            field=models.CharField(default='', max_length=128, null=True),
        ),
    ]
