from django import forms
from . import models

class CreateCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['Title', 'Code', 'Description', 'Password', 'GitHubPrefix']
        
class CreateAssignment(forms.ModelForm):
    class Meta:
        model = models.Assignment
        fields = ['CourseID', 'Title', 'Description', 'DueDate', 'ReleaseDate', 'PossiblePts', 'SolutionLink', 'ShowSolution', 'ShowSolutionOnDate', 'NumAttempts', 'GitHubPrefix']