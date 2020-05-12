from django.contrib import admin
from .models import Income, MonthYear, CurrencyConverter

# Register your models here.
admin.site.register(Income)
admin.site.register(MonthYear)
admin.site.register(CurrencyConverter)
