# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid

# MySQL Built-in Table added on 2/20/2020 by Micah Steinbock
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

# MySQL Built-in Table added on 2/20/2020 by Micah Steinbock
class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

# MySQL Built-in Table added on 2/20/2020 by Micah Steinbock
class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

# MySQL Built-in Table added on 2/20/2020 by Micah Steinbock
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'auth_user'

# MySQL Built-in Table added on 2/20/2020 by Micah Steinbock
class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

# MySQL Built-in Table added on 2/20/2020 by Micah Steinbock
class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

# Django Built-in Table added on 2/20/2020 by Micah Steinbock
class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

# Django Built-in Table added on 2/20/2020 by Micah Steinbock
class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

# Django Built-in Table added on 2/20/2020 by Micah Steinbock
class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

# Django Built-in Table added on 2/20/2020 by Micah Steinbock
class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

# Custom built table added on 2/20/2020 by Micah steinbock
class Roster(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    CourseID = models.ForeignKey('Course', on_delete=models.DO_NOTHING)
    #Which user class they are (instructor/student/ta/tutor)
    Classification = models.CharField(max_length=255)
    #Number of chances they have on assignments
    NumExtensions = models.IntegerField()

    def __str__(self):
        return self.UserID.username + ' - ' + self.CourseID.Code

# Custom built table added on 2/20/2020 by Micah steinbock
class Course(models.Model):
    InstructorID = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Title = models.CharField(max_length=255)
    Code = models.CharField(max_length=255)
    Description = models.TextField()
    Slug = models.SlugField(unique=True)
    #The code needed to add the class to your roster
    Password = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    GitHubPrefix = models.CharField(max_length=255)

    def __str__(self):
        return self.Code

# Custom built table added on 2/20/2020 by Micah steinbock
class Assignment(models.Model):
    CourseID = models.ForeignKey('Course', on_delete=models.DO_NOTHING)
    Title = models.CharField(max_length=255)
    Slug = models.SlugField(unique=True)
    Description = models.TextField()
    DueDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=False)
    ReleaseDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=False)
    PossiblePts = models.IntegerField()
    SolutionLink = models.CharField(max_length=255)
    ShowSolution = models.BooleanField()
    ShowSolutionOnDate = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    NumAttempts = models.IntegerField()
    GitHubPrefix = models.CharField(max_length=255)

    def __str__(self):
        return self.CourseID.Code + ' - ' + self.Title

# Custom built table added on 2/20/2020 by Micah steinbock
class Submission(models.Model):
    AssignmentID = models.ForeignKey('Assignment', on_delete=models.DO_NOTHING)
    RosterID = models.ForeignKey('Roster', on_delete=models.DO_NOTHING)
    SubmittedOn = models.DateTimeField()
    Grade = models.DecimalField(max_digits=7, decimal_places=2)
    Comments = models.TextField(blank=True)
    DidUseExtension = models.BooleanField()

    def __str__(self):
        return self.AssignmentID.CourseID.Code + ' - ' + self.AssignmentID.Title + ' - ' + self.RosterID.UserID.username

class UserDetail(models.Model):
    User = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    #Email is also used as username
    Email = models.EmailField()
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    SchoolID = models.CharField(max_length=20)
    GitHubUsername = models.CharField(max_length=255)
    isTeacher = models.BooleanField()

    def __str__(self):
        return self.User.username