from django.conf.urls import url
from . import views

urlpatterns = [
    # 教师登陆
    url(r'^index$', views.teacherLogin),
    # # 教师退出
    url(r'^logout', views.logOut),
    url(r'^score_analyse', views.score_analyse),
]
