from django.urls import path, include
from rest_framework.routers import DefaultRouter
from personal_finance_api.views import MemberViewSet
from core_finance_app import views

router = DefaultRouter()
router.register('income', views.IncomeViewSet)
router.register('members', MemberViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
