from django.db import models
from django.conf import settings

# Currency Model
class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name_plural = 'Currencies'
        verbose_name = 'Currency'

# Bank Model
class Bank(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')
    color = models.CharField(max_length=7)  # Hex color
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managed_banks')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Companies' 
        verbose_name = 'Company' 

# Branch Model
class Branch(models.Model):
    name = models.CharField(max_length=255)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='branches')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managed_branches')
    password = models.CharField(max_length=255, default="12345678")
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.bank.name}"
    
    class Meta:
        verbose_name_plural = 'Branches'
        verbose_name = 'Branch'

    def check_password(self, raw_password):
        # In a real app, use hashing here
        return self.password == raw_password

# Exchange Rate Model
class ExchangeRate(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='exchange_rates')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_rates')
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.currency.code} - {self.bank.name}"
    

    class Meta:
        verbose_name_plural = 'Exchange Rates'
        verbose_name = 'Exchange Rate'
        

# Bank adverts
class Advert(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='adverts')
    image = models.ImageField(upload_to='adverts/')
    
    def __str__(self):
        return f"{self.bank.name}"
    
    class Meta:
        verbose_name_plural = 'Adverts'
        verbose_name = 'Advert'

class BranchAdvert(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('text', 'Text')
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_adverts')
    media = models.FileField(upload_to='branch_adverts/', null=True, blank=True)
    text = models.TextField(help_text="Branch Advert text", null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')

    def __str__(self):
        return f"{self.branch.name} - {self.media_type}"
    
    class Meta:
        verbose_name_plural = 'Branch Adverts'
        verbose_name = 'Branch Advert'