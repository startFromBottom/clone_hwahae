# Generated by Django 2.2.4 on 2020-01-15 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('oily', models.CharField(max_length=1)),
                ('dry', models.CharField(max_length=1)),
                ('sensitive', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('imageId', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('gender', models.CharField(max_length=6)),
                ('category', models.CharField(choices=[('skincare', 'Skin care'), ('maskpack', 'Mask pack'), ('suncare', 'Sun care'), ('baskemakeup', 'Base makeup')], default='skincare', max_length=11)),
                ('monthlySales', models.IntegerField()),
                ('ingredients', models.ManyToManyField(related_name='products', to='products.Ingredient')),
            ],
        ),
    ]
