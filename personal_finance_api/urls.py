from django.urls import path, include
from rest_framework.routers import DefaultRouter

from personal_finance_api import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('home', views.OrganizationViewSet)

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('', include(router.urls)),
]
