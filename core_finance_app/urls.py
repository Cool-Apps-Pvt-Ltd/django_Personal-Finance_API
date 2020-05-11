from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core_finance_app import views

router = DefaultRouter()
router.register('income', views.IncomeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]