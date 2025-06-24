from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Bank, Branch, ExchangeRate, Currency
from .serializers import BankSerializer, BranchSerializer, ExchangeRateSerializer, BankDetailSerializer, CurrencySerializer
from .permissions import IsBankManager, IsBranchManager, IsBankManagerForBranch
from datetime import datetime
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def auth_branch(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        branch_id = int(data.get("branchId"))
        bank_id = int(data.get("bankId"))
        password = data.get("password", "")
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"success": False, "message": "Invalid input"}, status=400)

    try:
        branch = Branch.objects.select_related('bank').get(id=branch_id, bank_id=bank_id)
    except Branch.DoesNotExist:
        return JsonResponse({"success": False, "message": "Branch with given Bank not found"}, status=404)

    if branch.check_password(password):
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "message": "Invalid password"}, status=401)
    
class BankViewSet(viewsets.ModelViewSet):
    serializer_class = BankSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        # Bank.objects.filter(manager=user)
        return Bank.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BankDetailSerializer
        return BankSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'date': datetime.now().strftime('%A, %B %d, %Y'),
            'time': datetime.now().strftime('%I:%M %p')
        })
        return context

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsBankManager, IsBankManagerForBranch]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsBranchManager]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()


class UpdateExchangeRatesView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsBankManager]
    serializer_class = ExchangeRateSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.user_type != 'bank_admin':
            return Response({'error': 'Only bank managers can update exchange rates.'}, status=status.HTTP_403_FORBIDDEN)

        bank = user.bank
        data = request.data

        # Delete existing exchange rates for the bank
        ExchangeRate.objects.filter(bank=bank).delete()
       
        # Create new exchange rates
        for rate in data:
            try:
                currency = Currency.objects.get(code=rate['currency'])
                ExchangeRate.objects.update_or_create(
                    bank=bank,
                    currency=currency,
                    defaults={'buy_price': rate['buy'], 'sell_price': rate['sell']}
                )
            except Currency.DoesNotExist:
                return Response({'error': f"Currency {rate['currency']} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        updated_rates = ExchangeRate.objects.filter(bank=bank)
        serializer = self.get_serializer(updated_rates, many=True)
        return Response({'status': 'Exchange rates updated successfully.', 'rates': serializer.data}, status=status.HTTP_200_OK)


class AddBranchView(generics.CreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsBankManager]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'bank_admin':
            return Response({'error': "You're not allowed to create a branch"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(bank=user.bank)

class BankBranchesView(generics.ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'bank_admin':
            return Branch.objects.filter(bank=user.bank)
        return Branch.objects.none()
    

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


