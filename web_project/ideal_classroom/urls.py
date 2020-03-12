from django.urls import path
from django.conf.urls import url
from ideal_classroom import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^account/$', views.account, name="account"),
    url(r'^create_course/$', views.create_course, name="create_course"),
    url(r'^course/$', views.course, name="course"),
    url(r'^course/enroll/$', views.enroll, name="enroll"),
    url(r'^course/(?P<course_id>[\w-]+)/$', views.course, name="course"),
    url(r'^course/(?P<course_id>[\w-]+)/assignment', views.assignment, name="assignment"),
    url(r'^course/(?P<course_id>[\w-]+)/assignment/(?P<assn_name>[\w-]+)/$', views.assignment, name="assignment"),
    url(r'^course/(?P<course_id>[\w-]+)/create_assignment/$', views.create_assignment, name="create_assignment"),
]

urlpatterns += staticfiles_urlpatterns()