from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
    path('add/', views.add_user_view, name='add_user'),
]

