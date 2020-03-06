from django import forms
from . import models

class CreateCourse(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['Title', 'Code', 'Description', 'Password', 'GitHubPrefix']
        