from django.db import models


class Orders(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование', null=True)
    description = models.TextField(verbose_name='описание', null=True)
    time_create = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        app_label = 'adminpanel'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name





