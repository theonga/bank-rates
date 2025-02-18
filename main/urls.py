from django.urls import path
from .views import BankViewSet, BranchViewSet, ExchangeRateViewSet, BankBranchesView, CurrencyViewSet, UpdateExchangeRatesView, AddBranchView

bank_list = BankViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
bank_detail = BankViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

branch_list = BranchViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
branch_detail = BranchViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

exchange_rate_list = ExchangeRateViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
exchange_rate_detail = ExchangeRateViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

currency_list = CurrencyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
currency_detail = CurrencyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('banks/', bank_list, name='bank-list'),
    path('banks/<int:pk>', bank_detail, name='bank-detail'),
    path('banks/branches', BankBranchesView.as_view(), name='bank-branches'),
    path('branches', branch_list, name='branch-list'),
    path('branches/add', AddBranchView.as_view(), name='add-branch'),
    path('branches/<int:pk>', branch_detail, name='branch-detail'),
    path('exchange-rates', exchange_rate_list, name='exchange-rate-list'),
    path('exchange-rates/<int:pk>', exchange_rate_detail, name='exchange-rate-detail'),
    path('currencies', currency_list, name='currency-list'),
    path('currencies/<int:pk>', currency_detail, name='currency-detail'),
    path('rates', UpdateExchangeRatesView.as_view(), name='update-exchange-rates'),
   
]