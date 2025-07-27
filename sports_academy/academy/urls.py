from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('programs/<slug:sport_slug>/', views.subprogram_list_view, name='subprogram_list'),
    path('program/new/', views.program_create_view, name='program_create'),
    path('programs/<slug:sport_slug>/new-subprogram/', views.subprogram_create_view, name='subprogram_create'),
    path('child/new/', views.child_create_view, name='child_create'),
    path('my-children/', views.child_list_view, name='child_list'),
    path('subprogram/<int:subprogram_id>/enroll/', views.enroll_child_view, name='enroll_child'),
    path('program/<int:program_id>/edit/', views.program_update_view, name='program_edit'),
    path('program/<int:program_id>/delete/', views.program_delete_view, name='program_delete'),
    path('subprogram/<int:subprogram_id>/edit/', views.subprogram_update_view, name='subprogram_edit'),
    path('subprogram/<int:subprogram_id>/delete/', views.subprogram_delete_view, name='subprogram_delete'),
    path('child/<int:child_id>/edit/', views.child_update_view, name='child_edit'),
    path('child/<int:child_id>/delete/', views.child_delete_view, name='child_delete'),
    path('coach/dashboard/', views.coach_dashboard_view, name='coach_dashboard'),
    path('subprogram/<int:subprogram_id>/detail/', views.subprogram_detail_view, name='subprogram_detail'),
    ]

