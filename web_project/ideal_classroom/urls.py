from django.urls import path
from django.conf.urls import url
from ideal_classroom import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("account/", views.account, name="account"),
    path("course/assignment/", views.assignment, name="assignment"),
    url(r'^course/(?P<slug>[\w-]+)/create_assignment/$', views.create_assignment, name="create_assignment"),
    path("course/", views.course, name="course"),
    path("create_course/", views.create_course, name="create_course"),
    path("", views.button),
    path("run_test", views.run_test, name="script"),
]

urlpatterns += staticfiles_urlpatterns()