from django.db import models
from django.contrib.auth.models import User
from catalog.models import Service, Component, Category, Resources


class Application(models.Model):
    """Class representing a Applications table."""

    first_name = models.CharField(
        'Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', max_length=20
    )
    email = models.EmailField(
        'E-mail',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    date_of_access = models.DateField(
        'Дата обращения',
        auto_now_add=True,
    )
    date_of_readiness = models.DateField(
        'Дата готовности',
    )
    comment = models.TextField(
        'Описание проблемы',
        max_length=512,
        blank=True,
        help_text='Необязательное поле',
    )
    master = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='applications',
    )

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-date_of_access']

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        """Calculation of the total cost of the application.

        Returns:
        int: total cost of the application.
        """
        return sum(item.get_cost() for item in self.component_items.all()) + \
            sum(item.get_cost() for item in self.service_items.all())


class ApplicationComponentItem(models.Model):
    """Class representing a table with components(details) in applications."""

    application = models.ForeignKey(
        Application,
        related_name='component_items',
        on_delete=models.CASCADE
    )
    component = models.ForeignKey(
        Component,
        related_name='component',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveBigIntegerField(
        'Количество',
        default=0,
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Calculation of the cost of components in application.

        Returns:
        int: total cost of components.
        """
        return self.component.price * self.quantity


class ApplicationServiceItem(models.Model):
    """Class representing a table with services in applications."""

    application = models.ForeignKey(
        Application,
        related_name='service_items',
        on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        related_name='service',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveBigIntegerField(
        'Количество',
        default=0,
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Calculation of the cost of services in application.

        Returns:
        int: total cost of services.
        """
        return self.service.price * self.quantity
