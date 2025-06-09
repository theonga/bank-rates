from django.contrib import admin
from .models import Bank, Branch, ExchangeRate, Currency, Advert, BranchAdvert

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'color')
    search_fields = ('name', 'manager__username')
    list_filter = ('color',)

    # Inline for managing exchange rates on the bank detail page
    class ExchangeRateInline(admin.TabularInline):
        model = ExchangeRate
        extra = 1  # Number of empty forms to display for adding new exchange rates
        fields = ('currency', 'buy_price', 'sell_price')  # Fields to display in the inline form

    inlines = [ExchangeRateInline]  # Add the inline to the Bank admin

@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'image')
    search_fields = ('bank__name',)

class BranchAdvertInline(admin.TabularInline):  # Inline for BranchAdvert
    model = BranchAdvert
    extra = 1  # Number of empty forms to display for adding new adverts
    fields = ('media', 'media_type')  # Fields to display in the inline form

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bank')
    search_fields = ('name', 'bank__name')
    list_filter = ('bank',)
    inlines = [BranchAdvertInline]  # Add the inline to the Branch admin

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'currency', 'buy_price', 'sell_price')
    search_fields = ('bank__name', 'currency__code')
    list_filter = ('bank', 'currency')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('code', 'name')

@admin.register(BranchAdvert)
class BranchAdvertAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'media', 'media_type')
    search_fields = ('branch__name', 'media_type')
    list_filter = ('media_type', 'branch')