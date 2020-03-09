from django.urls import path
from ideal_classroom import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name="home"),
    path("dbtest/", views.dbtest, name="dbtest"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("account/", views.account, name="account"),
    path("course/assignment/", views.assignment, name="assignment"),
    path("course/", views.course, name="course"),
    path("create_course/", views.create_course, name="create_course"),
    path("", views.button),
]

urlpatterns += staticfiles_urlpatterns()