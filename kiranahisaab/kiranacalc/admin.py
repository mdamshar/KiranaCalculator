from django.contrib import admin
from .models import calc

@admin.register(calc)
class CalcAdmin(admin.ModelAdmin):
    exclude = ('slug',)