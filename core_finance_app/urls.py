from django.urls import path, include
from rest_framework.routers import DefaultRouter
from personal_finance_api.views import MemberViewSet
from core_finance_app import views

router = DefaultRouter()
router.register('income', views.IncomeViewSet)
router.register('members', MemberViewSet)
router.register('monthly', views.MonthYearViewSet)
router.register('currency', views.CurrencyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
