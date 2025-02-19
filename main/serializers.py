from rest_framework import serializers
from .models import Bank, Branch, ExchangeRate, Currency, Advert
from users.serializers import ProfileSerializer
from users.models import Profile

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'icon']


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name', 'logo', 'color', 'manager']

class BranchSerializer(serializers.ModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all(), write_only=True)
    manager = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    bank_details = BankSerializer(source='bank', read_only=True)
    manager_details = ProfileSerializer(source='manager', read_only=True)

    class Meta:
        model = Branch
        fields = ['id', 'name', 'bank', 'manager', 'bank_details', 'manager_details']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['bank'] = {
            'id': instance.bank.id if instance.bank else None,
            'name': instance.bank.name if instance.bank else None
        }
        representation['manager'] = {
            'id': instance.manager.id if instance.manager else None,
            'email': instance.manager.email if instance.manager else None
        }
        return representation

class ExchangeRateSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = ExchangeRate
        fields = ['id', 'bank', 'currency', 'buy_price', 'sell_price']


class AdvertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advert
        fields = ['id', 'image']

class BankDetailSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    exchange_rates = ExchangeRateSerializer(many=True, read_only=True)
    adverts = AdvertSerializer(many=True, read_only=True)

    class Meta:
        model = Bank
        fields = ['name', 'logo', 'color', 'branches', 'exchange_rates', 'adverts']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'bankName': representation['name'],
            'logoUrl': representation['logo'],
            'tagline': representation['branches'][0]['name'] if representation['branches'] else '',
            'color': representation['color'],
            'date': self.context.get('date', ''),
            'time': self.context.get('time', ''),
            'rates': [
                {
                    'currency': rate['currency']['code'],
                    'buy': rate['buy_price'],
                    'sell': rate['sell_price'],
                    'icon': rate['currency']['icon']
                }
                for rate in representation['exchange_rates']
            ],
            'adverts': representation['adverts']
        }