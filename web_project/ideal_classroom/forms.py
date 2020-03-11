from django import forms
from . import models

#Commented out b/c it does not work with SQL Formatting
#class MyDateTimeInput(forms.DateTimeInput):
    #input_type = 'datetime-local'


class CreateCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['Title', 'Code', 'Description', 'Password', 'GitHubPrefix']
        
class CreateAssignment(forms.ModelForm):
    class Meta:
        #widgets = {'DueDate' : MyDateTimeInput(), 'ReleaseDate' : MyDateTimeInput(), 'ShowSolutionOnDate' : MyDateTimeInput()}
        model = models.Assignment
        fields = ['Title', 'Description', 'DueDate', 'ReleaseDate', 'PossiblePts', 'SolutionLink', 'ShowSolution', 'ShowSolutionOnDate', 'NumAttempts', 'GitHubPrefix']