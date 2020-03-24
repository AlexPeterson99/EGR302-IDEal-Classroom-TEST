from django.urls import path, include
from django.conf.urls import url
from ideal_classroom import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'', views.home, name="home"),
    url(r'/login/', views.login, name="login"),
    url(r'/register/', views.register, name="register"),
    url(r'/account/', views.account, name="account"),
    url(r'create_course/', views.create_course, name="create_course"),
    url(r'course/', include([
        url(r'', views.course, name="course"),
        url(r'enroll/', views.enroll, name="enroll"),
        url(r'(?P<course_id>[\w-]+)/', views.course, name="course"),
        url(r'(?P<course_id>[\w-]+)/assignment/', views.assignment, name="assignment"),
        url(r'(?P<course_id>[\w-]+)/assignment/(?P<assn_name>[\w-]+)/', views.assignment, name="assignment"),
        url(r'(?P<course_id>[\w-]+)/create_assignment/', views.create_assignment, name="create_assignment"),
    ])),
    
]

urlpatterns += staticfiles_urlpatterns()