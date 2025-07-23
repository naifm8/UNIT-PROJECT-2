from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    player_list_view, player_add_view, player_update_view, player_delete_view,player_detail_view,dashboard_view
)

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),

    # this is for the player management
    path('players/', player_list_view, name='player_list'),
    path('players/add/', player_add_view, name='player_add'),
    path('players/<int:pk>/edit/', player_update_view, name='player_edit'),
    path('players/<int:pk>/delete/', player_delete_view, name='player_delete'),
    path('players/<int:pk>/detail/', player_detail_view, name='player_detail'),

]
