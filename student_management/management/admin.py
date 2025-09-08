from django.contrib import admin
from .models import Student, Course, Enrollment

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']
    ordering = ['name']
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'credits', 'created_at']
    search_fields = ['title']
    list_filter = ['credits', 'created_at']
    ordering = ['title']
    
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade', 'enrollment_date']
    list_filter = ['grade', 'enrollment_date', 'course']
    search_fields = ['student__name', 'course__title']
    ordering = ['student__name', 'course__title']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course')