from django.urls import path, include
from rest_framework.routers import DefaultRouter
from personal_finance_api import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    #path('user-profile/', views.UserProfileView.as_view()),
    path('', include(router.urls)),
]