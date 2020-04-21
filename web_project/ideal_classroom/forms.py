from django import forms
from . import models
from bootstrap_datepicker_plus import DateTimePickerInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CreateCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['Title', 'Slug', 'Code', 'Description', 'GitHubPrefix']
        
class CreateAssignment(forms.ModelForm):
    class Meta:
        model = models.Assignment
        fields = ['Title', 'Slug', 'Description', 'DueDate', 'ReleaseDate', 'PossiblePts', 'SolutionLink', 'ShowSolution', 'ShowSolutionOnDate', 'NumAttempts', 'GitHubPrefix']
        widgets = {'DueDate': DateTimePickerInput(), 'ReleaseDate': DateTimePickerInput(), 'ShowSolutionOnDate': DateTimePickerInput()}

class Enroll(forms.Form):
    course_password = forms.CharField(label='Course Enroll Code', max_length=100)

class Register(forms.ModelForm):
    class Meta:
        model = models.UserDetail
        fields = ['Email', 'Firstname', 'Lastname', 'SchoolID', 'GitHubUsername', 'isTeacher']

class EditInfo(forms.ModelForm):
    class Meta:
        model = models.UserDetail
        fields = ['Email', 'Firstname', 'Lastname', 'SchoolID', 'GitHubUsername']

class EditCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['Title', 'Code', 'Description', 'GitHubPrefix']

class EditAssn(forms.ModelForm):
    class Meta:
        model = models.Assignment
        fields = ['Title', 'Description', 'DueDate', 'ReleaseDate', 'PossiblePts', 'SolutionLink', 'ShowSolution', 'ShowSolutionOnDate', 'NumAttempts', 'GitHubPrefix']

class EditGrades(forms.ModelForm):
    class Meta:
        model = models.Submission
        fields = ['Grade', 'Comments']
