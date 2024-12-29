# Generated by Django 3.2.16 on 2024-12-12 01:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0003_auto_20241212_0100'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('date_of_access', models.DateField(auto_now_add=True, verbose_name='Дата обращения')),
                ('date_of_readiness', models.DateField(verbose_name='Дата готовности')),
                ('comment', models.TextField(blank=True, help_text='Необязательное поле', max_length=512, verbose_name='Комментарий')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.category')),
                ('components', models.ManyToManyField(to='catalog.Component')),
                ('services', models.ManyToManyField(to='catalog.Service')),
                ('wizard', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]