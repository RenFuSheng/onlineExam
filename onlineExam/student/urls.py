from django.conf.urls import url
from . import views

urlpatterns = [

    # 学生首页
    url(r'^index$', views.studentLogin),
    # # 开始考试
    url(r'^startExam', views.startExam),
    # # 查看成绩
    url(r'^calGrade', views.calGrade),
]
