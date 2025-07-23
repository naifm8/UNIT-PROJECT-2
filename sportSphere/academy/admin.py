from django.contrib import admin
from .models import Program, Enrollment

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'sport', 'min_age', 'max_age', 'start_date', 'coach')

    list_filter = ('sport', 'start_date')
    search_fields = ('title', 'description')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('player', 'program', 'enrolled_on', 'status')
    list_filter = ('status', 'program__sport')
    search_fields = ('player__full_name', 'program__title')
