from rest_framework import serializers
from .models import Bank, Branch, ExchangeRate, Currency, Advert, BranchAdvert
from users.serializers import ProfileSerializer
from users.models import Profile

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'icon']


class BankSerializer(serializers.ModelSerializer):
    branches = serializers.SerializerMethodField()

    class Meta:
        model = Bank
        fields = ['id', 'name', 'logo', 'color', 'manager', 'branches']

    def get_branches(self, obj):
        return list(obj.branches.values_list('id', flat=True))

class BranchAdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchAdvert
        fields = ['id', 'media', 'media_type', 'text']

class BranchSerializer(serializers.ModelSerializer):
    bank = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all(), write_only=True)
    manager = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    bank_details = BankSerializer(source='bank', read_only=True)
    manager_details = ProfileSerializer(source='manager', read_only=True)
    adverts = BranchAdvertSerializer(many=True, read_only=True)  # Include BranchAdvertSerializer

    class Meta:
        model = Branch
        fields = ['id', 'name', 'bank', 'manager', 'bank_details', 'manager_details', 'adverts']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['bank'] = {
            'id': instance.bank.id if instance.bank else None,
            'name': instance.bank.name if instance.bank else None
        }
        representation['manager'] = {
            'id': instance.manager.id if instance.manager else None,
            'email': instance.manager.email if instance.manager else None,
            'is_superuser': getattr(instance.manager, 'is_superuser', False)
        }

        # Separate images and videos
        adverts = instance.branch_adverts.all()
        images = adverts.filter(media_type='image')
        videos = adverts.filter(media_type='video')
        texts = adverts.filter(media_type="text")

        representation['images'] = BranchAdvertSerializer(images, many=True).data
        representation['videos'] = BranchAdvertSerializer(videos, many=True).data
        representation['text'] = BranchAdvertSerializer(texts, many=True).data

        # Remove the combined adverts field
        representation.pop('adverts', None)

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
        branch_ids = [branch['id'] for branch in representation['branches']]
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
            'adverts': representation['adverts'],
            'branchIds': branch_ids 
        }