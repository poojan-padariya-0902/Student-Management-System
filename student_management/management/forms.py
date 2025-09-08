from django import forms
from .models import Student, Course, Enrollment

class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
        }
    
    def clean_name(self):
        
        name = self.cleaned_data.get('name')
        
        if name:
            
            name = name.strip().title()
            if len(name.split()) < 2:
                raise forms.ValidationError("Please enter both first and last name.")
            
            if not all(part.isalpha() for part in name.split()):
                raise forms.ValidationError('Name can only contain letters and spaces.')
            
        return name
    
class CourseForm(forms.ModelForm):
    
    class Meta:
        
        model = Course
        fields = ['title', 'credits']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course Title'
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'credits (1-6)',
                'min': 1,
                'max': 6
            }),
        }
    
    def clean_title(self):
        
        title = self.cleaned_data.get('title')
        
        if title:
            
            title = title.strip().title()
            
        return title
    
class EnrollmentForm(forms.ModelForm):
    
    class Meta:
        
        model = Enrollment
        fields = ['student', 'course', 'grade']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['student'].quaryset = Student.objects.all().order_by('name')
        self.fields['course'].quaryset = Course.objects.all().order_by('title')
        self.fields['grade'].quaryset = Enrollment.GRADE_CHOICES
        self.fields['grade'].required = False
        
class GradeUpdateForm(forms.ModelForm):
    
    class Meta:
        
        model = Enrollment
        fields = ['grade']
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-select'}),
        }
    
    
    