# Generated by Django 3.0.5 on 2020-04-08 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JapanInfectedNumber',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=128)),
                ('positive', models.IntegerField(null=True)),
                ('hospitalization', models.IntegerField(null=True)),
                ('discharge', models.IntegerField(null=True)),
                ('death', models.IntegerField(null=True)),
                ('date', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('jp', models.CharField(max_length=100)),
                ('kana', models.CharField(max_length=100)),
                ('romam', models.CharField(max_length=100)),
                ('disp', models.IntegerField()),
                ('color', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
