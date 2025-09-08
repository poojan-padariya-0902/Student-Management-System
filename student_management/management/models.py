from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re

# Create your models here.

class Student(models.Model):
    
    name = models.CharField(max_length=100, help_text="Full name of the student.")
    email = models.EmailField(unique=True, help_text="Email address of the student.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def clean(self):
        
        if self.email:
            self.email = self.email.lower()
            
        # Validate that name contains only letters and spaces
        if self.name and not re.match(r'^[A-Za-z\s]+$', self.name):
            raise ValidationError("Name can only contain letters and spaces.")
        
class Course(models.Model):
    
    title = models.CharField(max_length=200, help_text='Title of the course.')
    credits = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], 
        help_text='Number of credits of the course (1-6).'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self):
        return f"{self.title} ({self.credits} credits)"
    
    def clean(self):
        
        if self.title:
            self.title = self.title.strip()

        if self.credits is None:
            raise ValidationError("Credits cannot be empty.")
            
        if self.credits < 1 or self.credits > 6:
            return ValidationError('Credits must be between 1 and 6.')
        
class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D+', 'D+'), ('D', 'D'), ('F', 'F'),
        ('I', 'Incomplete'), ('W', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        blank=True,
        null=True,
        help_text='Grade received in the course.'
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'course')
        ordering = ['student__name', 'course__title']
        
    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.title} - Grade: {self.grade or 'N/A'}"
