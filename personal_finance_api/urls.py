from django.urls import path
from personal_finance_api import views

urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view()),
]