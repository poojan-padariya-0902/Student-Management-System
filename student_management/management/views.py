from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q,Count
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Student, Course, Enrollment
from .forms import StudentForm, CourseForm, EnrollmentForm, GradeUpdateForm

# Create your views here.

def home(request):
    
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    recent_enrollments = Enrollment.objects.select_related('student', 'course').order_by('-enrollment_date')[:5]
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'recent_enrollments': recent_enrollments
    }
    
    return render(request, 'home.html', context)

# Student Views
def student_list(request):
    
    search_query = request.GET.get('search', '')
    students = Student.objects.all()
    
    if search_query:
        
        students = students.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query)
        )
    
    students = students.annotate(enrollment_count=Count('enrollments'))
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)
    
    context = {
        'students': students,
        'search_query': search_query
    }
    
    return render(request, 'students/list.html', context)

def student_detail(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    
    context = {
        'student': student,
        'enrollments': enrollments
    }
    
    return render(request, 'students/details.html', context)

def student_create(request):
    
    if request.method == 'POST':
        
        form = StudentForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Please correct the errors below!')
            
        student = form.save()
        messages.success(request, f'Student "{student.name}" created successfully!')
        return redirect('student_detail', pk=student.pk)

    form = StudentForm()
        
    context = {
        'form': form,
        'title': 'Add New Student'
    }
    
    return render(request, 'students/form.html', context)

def student_edit(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        
        form = StudentForm(request.POST, instance=student)
        
        if not form.is_valid():
            messages.error(request, 'Please correct the errors below!')
            
        form.save()
        messages.success(request, f'Student "{student.name}" updated successfully!')
        return redirect('student_detail', pk=student.pk)
    
    form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'title': f'Edit {student.name}'
    }
    
    return render(request, 'students/form.html', context)

def student_delete(request,pk):
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        
        Student_name = student.name
        student.delete()
        messages.success(request, f'Student "{Student_name}" deleted successfully!')
        return redirect('student_list')
    
    enrollment_count = student.enrollments.count()
    context = {
        'student': student,
        'enrollment_count': enrollment_count
    }
    return render(request, 'students/confirm_delete.html', context)

# Course Views
def course_list(request):
    
    search_query = request.GET.get('search', '')
    courses = Course.objects.all()
    
    if search_query:
        courses = courses.filter(title__icontains=search_query)
        
    courses = courses.annotate(enrollment_count = Count('enrollments'))
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
    
    context = {
        'courses': courses,
        'search_query': search_query
    }
    
    return render(request, 'courses/list.html', context)

def course_detail(request, pk):
    
    course = get_object_or_404(Course, pk=pk)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    
    context = {
        'course': course,
        'enrollments': enrollments
    }
    
    return render(request, 'courses/details.html', context)

def course_create(request):
    
    if request.method == 'POST':
        
        form = CourseForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Please correct the errors below!')
            
        course = form.save()
        messages.success(request, f'Course "{course.title}" created successfully!')
        return redirect('course_detail', pk=course.pk)
    form = CourseForm()
    
    context = {
        'form': form,
        'title': 'Add New Course'
    }
    
    return render(request, 'courses/form.html', context)

def course_edit(request,pk):
    
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        
        form = CourseForm(request.POST, instance=course)
        
        if not form.is_valid():
            messages.error(request, 'Please correct the errors below!')
        
        form.save()
        messages.success(request, f'Course "{course.title}" updated successfully!')
        return redirect('course_detail', pk=course.pk)
    
    form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'title': f'Edit {course.title}'
    }
    
    return render(request, 'courses/form.html', context)

def course_delete(request, pk):
    
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        
        course_title = course.title
        course.delete()
        messages.success(request, f'Course "{course_title}" deleted successfully!')
        return redirect('course_list')
    
    enrollment_count = course.enrollments.count()
    
    context = {
        'course': course,
        'enrollment_count': enrollment_count
    }
    
    return render(request, 'courses/confirm_delete.html', context)

# Enrollment Views
def enrollment_list(request):
    
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    
    student_filter = request.GET.get('student')
    course_filter = request.GET.get('course')
    grade_filter = request.GET.get('grade')
    
    if student_filter:
        enrollments = enrollments.filter(student__id=student_filter)
    if course_filter:
        enrollments = enrollments.filter(course__id=course_filter)
    if grade_filter:
        enrollments = enrollments.filter(grade=grade_filter)
        
    paginator = Paginator(enrollments, 10)
    page_number = request.GET.get('page')
    enrollments = paginator.get_page(page_number)
    
    students = Student.objects.all()
    courses = Course.objects.all()
    grades = Enrollment.GRADE_CHOICES
    
    context = {
        'enrollments': enrollments,
        'students': students,
        'courses': courses,
        'grades': grades,
        'current_filter': {
            'student': student_filter,
            'course': course_filter,
            'grade': grade_filter
        }
    }
    
    return render(request, 'enrollments/list.html', context)

def enrollment_create(request):
    
    if request.method == 'POST':
        
        form = EnrollmentForm(request.POST)
        
        if not form.is_valid():
            messages.error(request, 'Please correct the errors below!')
            
        try:
            enrollment = form.save()
            messages.success(request, f'{enrollment.student.name} successfully enrolled in {enrollment.course.title}!')
            return redirect('enrollment_list')
        except Exception as e:
            messages.error(request, f'Error creating enrollment: {str(e)}!')
        
    form = EnrollmentForm()
    
    context = {
        'form': form,
        'title': 'New Enrollment'
    }
    
    return render(request, 'enrollments/form.html', context)

def enrollment_update_grade(request, pk):
    
    enrollment = get_object_or_404(Enrollment, pk=pk)
    
    if request.method == 'POST':
        
        form = GradeUpdateForm(request.POST, instance=enrollment)
        
        if not form.is_valid():
            messages.error(request, 'Please correct the errors below!')
        
        form.save()
        messages.success(request, f'Grade updated for "{enrollment.student.name}" in "{enrollment.course.title}"!')
        return redirect('enrollment_list')
    
    form = GradeUpdateForm(instance=enrollment)
    
    context = {
        'form': form,
        'enrollment': enrollment,
        'title': f'Update Grade - {enrollment.student.name}'
    }
    
    return render(request, 'enrollments/grade_form.html', context)

def enrollment_delete(request, pk):
    
    enrollment = get_object_or_404(Enrollment, pk=pk)
    
    if request.method == 'POST':
        
        student_name = enrollment.student.name
        course_title = enrollment.course.title
        enrollment.delete()
        messages.success(request, f'{student_name} unenrolled from {course_title} successfully!')
        return redirect('enrollment_list')
    
    context = {
        'enrollment': enrollment    
    }
    
    return render(request, 'enrollments/confirm_delete.html', context)

# Reporting Views
def report_overview(request):
    
    students_with_enrollments = (
        Student.objects
        .annotate(enrollment_count=Count('enrollments'))
        .order_by('-enrollment_count')[:5]   # get top 10
    )
    
    popular_courses = Course.objects.annotate(enrollment_count = Count('enrollments')).order_by('-enrollment_count')[:5]
    
    grade_stats = {}
    
    for grade_code, grade_name in Enrollment.GRADE_CHOICES:
        grade_stats[grade_name] =Enrollment.objects.filter(grade=grade_code).count()
        
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
        
    context = {
        'students_with_enrollments': students_with_enrollments,
        'popular_courses': popular_courses,
        'grade_stats': grade_stats,
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments
    }
    
    return render(request, 'reports/overview.html', context)

def student_transcript(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    
    gpa_calculation = None
    grade_points = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'F': 0.0
    }
    
    grade_enrollments = enrollments.filter(grade__in=grade_points.keys())
    if grade_enrollments:
        
        total_points = sum(grade_points[e.grade] * e.course.credits for e in grade_enrollments)
        total_credits = sum(e.course.credits for e in grade_enrollments)    
        gpa_calculation = round(total_points/total_credits, 2) if total_credits > 0 else 0
        
    total_credits = sum(e.course.credits for e in enrollments)
    in_progress = enrollments.filter(Q(grade__isnull=True) | Q(grade='I')).count()
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'gpa': gpa_calculation,
        'total_credits': sum(e.course.credits for e in enrollments),
        'in_progress_count': in_progress,
    }
    
    return render(request, 'reports/student_transcript.html', context)
