from django.urls import path, include
from django.conf.urls import url
from ideal_classroom import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^account/$', views.account, name="account"),
    url(r'^account/edit/$', views.edit_info, name="edit_info"),
    url(r'^create_course/$', views.create_course, name="create_course"),
    url(r'^courses/$', views.courses, name="courses"),
    url(r'^courses/enroll/$', views.enroll, name="enroll"),
    url(r'^courses/(?P<course_id>[\w-]+)/$', views.course_details, name="course_details"),
    url(r'^courses/(?P<course_id>[\w-]+)/assignments/$', views.assignments, name="assignments"),
    url(r'^courses/(?P<course_id>[\w-]+)/assignments/(?P<assn_name>[\w-]+)/$', views.assignment_details, name="assignment_details"),
    url(r'^courses/(?P<course_id>[\w-]+)/assignments/(?P<assn_name>[\w-]+)/grades/$', views.assignment_grades, name="assignment_grades"),
    url(r'^courses/(?P<course_id>[\w-]+)/create_assignment/$', views.create_assignment, name="create_assignment"),
    url(r'^courses/(?P<course_id>[\w-]+)/grades/$', views.grades, name="grades"),
]

urlpatterns += staticfiles_urlpatterns()