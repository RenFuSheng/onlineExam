from django.contrib import admin
from django.conf.urls import url, include
from . import views

urlpatterns = [

    # 管理员登陆
    url('admin/', admin.site.urls),
    # #默认访问首页
    url(r'^$', views.acc_login),
    url(r'^studentLogin/', include('student.urls')),
    url(r'^teacherLogin/', include('teacher.urls')),
    url(r'^get_code/', views.get_code),
]
