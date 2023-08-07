from django.contrib import admin
from .models import Orders


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_create')


admin.site.register(Orders, OrdersAdmin,)