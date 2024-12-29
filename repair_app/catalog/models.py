from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        'Тип техники',
        max_length=128,
    )

    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы,'
            ' цифры, дефис и подчёркивание.'
        ),
    )

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    title = models.CharField(
        'Производитель',
        max_length=128,
    )

    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы,'
            ' цифры, дефис и подчёркивание.'
        ),
    )

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.title


class Resources(models.Model):
    """Абстрактный класс ресурсов."""

    name = models.TextField(
        'Наименование',
        max_length=512,
    )
    article_number = models.TextField(
        'Артикул',
        max_length=128,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
    )
    comment = models.TextField(
        'Комментарий',
        max_length=512,
        blank=True,
        help_text='Необязательное поле',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Component(Resources):
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Производитель',
    )
    quantity = models.IntegerField(
        'Количество на складе',
    )
    availability = models.BooleanField(
        'Наличие',
        default=False,
    )
    image = models.ImageField(
        'Фото',
        upload_to='components_img',
        blank=True)

    class Meta:
        verbose_name = 'деталь'
        verbose_name_plural = 'Детали'

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.availability = True
        else:
            self.availability = False
        super(Component, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.manufacturer}'


class Service(Resources):
    duration = models.DurationField(
        verbose_name='Продолжительность',
    )

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'Услуги'

