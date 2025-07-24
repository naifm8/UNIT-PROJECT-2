from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import program_list_view, enroll_player_view,pending_enrollments_view,approve_enrollment_view, reject_enrollment_view,program_create_view,program_edit_view,program_delete_view,program_detail_view,subprogram_list_view,subprogram_create_view

app_name = 'academy'

urlpatterns = [
    path('program/', program_list_view, name='program_list'),
    path('enroll/<int:program_id>/', enroll_player_view, name='enroll_player'),
    path('enrollments/pending/', pending_enrollments_view, name='pending_enrollments'),
    path('enrollments/<int:enrollment_id>/approve/', approve_enrollment_view, name='approve_enrollment'),
    path('enrollments/<int:enrollment_id>/reject/', reject_enrollment_view, name='reject_enrollment'),
    path('programs/new/', program_create_view, name='program_create'),
    path('programs/<int:pk>/edit/', program_edit_view, name='program_edit'),
    path('programs/<int:pk>/delete/', program_delete_view, name='program_delete'),
    path('programs/<int:pk>/', program_detail_view, name='program_detail'),
    path('<int:program_id>/subprograms/', subprogram_list_view, name='subprogram_list'),
    path('<int:parent_id>/subprograms/new/', subprogram_create_view, name='subprogram_create'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
