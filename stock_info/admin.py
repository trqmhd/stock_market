from django.contrib import admin
from .models import StockInfo

# Register your models here.


class StockInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__','slug']
    class Meta:
        model = StockInfo



admin.site.register(StockInfo, StockInfoAdmin)
