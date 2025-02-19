from django.contrib import admin
from .models import Bank, Branch, ExchangeRate, Currency, Advert

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'color')
    search_fields = ('name', 'manager__username')
    list_filter = ('color',)

@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'image')
    search_fields = ('bank__name',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bank')
    search_fields = ('name', 'bank__name')
    list_filter = ('bank',)

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'currency', 'buy_price', 'sell_price')
    search_fields = ('bank__name', 'currency__code')
    list_filter = ('bank', 'currency')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('code', 'name')