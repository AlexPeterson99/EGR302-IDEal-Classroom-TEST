from django.contrib import admin
from .models import Roster, Course, Assignment, Submission, TempUsers

admin.site.register(Roster)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(TempUsers)