from django.contrib import admin
from .models import Bank, Branch, ExchangeRate, Currency, Advert, BranchAdvert
from django import forms

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

# @admin.register(Advert)
# class AdvertAdmin(admin.ModelAdmin):
#     list_display = ('id', 'bank', 'image')
#     search_fields = ('bank__name',)

class BranchAdvertInline(admin.TabularInline):  # Inline for BranchAdvert
    model = BranchAdvert
    extra = 1  # Number of empty forms to display for adding new adverts
    fields = ('media', 'text', 'media_type')  # Fields to display in the inline form

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_login')
    search_fields = ('name', )
    list_filter = ('bank',)
    inlines = [BranchAdvertInline]

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'currency', 'buy_price', 'sell_price')
    search_fields = ('bank__name', 'currency__code')
    list_filter = ('bank', 'currency')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('code', 'name')

# class BranchAdvertAdminForm(forms.ModelForm):
#     apply_to_all_branches = forms.BooleanField(
#         required=False,
#         label="Apply to all branches of this bank",
#         help_text="If checked, this advert will be added to all branches of the selected branch's bank."
#     )

#     class Meta:
#         model = BranchAdvert
#         fields = '__all__'

# @admin.register(BranchAdvert)
# class BranchAdvertAdmin(admin.ModelAdmin):
#     form = BranchAdvertAdminForm
#     list_display = ('id', 'branch', 'media', 'media_type')
#     search_fields = ('branch__name', 'media_type')
#     list_filter = ('media_type', 'branch')

#     def save_model(self, request, obj, form, change):
#         apply_to_all = form.cleaned_data.get('apply_to_all_branches', False)
#         if apply_to_all and obj.branch:
#             # Save the original object for the selected branch
#             super().save_model(request, obj, form, change)
#             # Get all other branches of the same bank
#             other_branches = Branch.objects.filter(bank=obj.branch.bank).exclude(id=obj.branch.id)
#             for branch in other_branches:
#                 BranchAdvert.objects.create(
#                     branch=branch,
#                     media=obj.media,
#                     media_type=obj.media_type,
#                     text=getattr(obj, 'text', None)
#                 )
#         else:
#             super().save_model(request, obj, form, change)