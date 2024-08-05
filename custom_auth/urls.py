from django.urls import path
from . import views
from .views import  group_list

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.user_list_create, name='user-list-create'),
    path('users/<int:pk>/', views.user_detail, name='user-detail'),
    path('groups/', group_list, name='group-list'),
]