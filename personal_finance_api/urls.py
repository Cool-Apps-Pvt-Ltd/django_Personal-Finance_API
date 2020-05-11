from django.urls import path, include
from rest_framework.routers import DefaultRouter
from personal_finance_api import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('home', views.OrganizationViewSet)
router.register('(?P<org_id>[^/.]+)/members', views.MemberViewSet)

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/', views.create_user),
    path('', include(router.urls)),
]
