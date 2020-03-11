from django.urls import path
from django.conf.urls import url
from ideal_classroom import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("account/", views.account, name="account"),
    url(r'^course/(?P<slug>[\w-]+)/assignment', views.assignment, name="assignment"),
    url(r'^course/(?P<slug>[\w-]+)/create_assignment/$', views.create_assignment, name="create_assignment"),
    url(r'^course/(?P<slug>[\w-]+)', views.course, name="course"),
    path("create_course/", views.create_course, name="create_course"),
]

urlpatterns += staticfiles_urlpatterns()