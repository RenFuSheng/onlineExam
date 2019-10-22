from django.shortcuts import render, redirect
from student import models
import teacher
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout


# Create your views here.
# def index(request):
#     return render(request, 'index.html')
#
#
# def toIndex(request):
#     return render(request, 'index.html')
#

# 学生登陆 视图函数
# def studentLogin(username, password):
#     # 获取表单信息
#     stuId = username
#     # 通过学号获取该学生实体
#     try:
#         student = models.Student.objects.get(id=stuId)
#         if password == student.password:  # 登录成功
#             # 查询考试信息
#             pass
#             paper = teacher.models.Paper.objects.filter(major=student.major)
#             # 查询成绩信息
#             grade = teacher.models.Grade.objects.filter(sid=student.id)
#             # 渲染index模板
#             # return render(request, 'index.html', )
#             return ['studentLogin.html', {'student': student, 'paper': paper, 'grade': grade}]
#         else:
#             # return render(request, 'index.html', {'message': '密码不正确'})
#             return '学号或密码错误'
#     except:
#         return '学号不存在'


def studentLogin(request):
    if request.method == 'POST':
        info_dict = request.POST
        username = info_dict['username']
        password = info_dict['password']
        code = info_dict['code']
        # if code.upper() == request.session['code'].upper():
        if code.upper() != request.session['code'].upper():
            try:
                student = models.Student.objects.get(id=username)
                if password == student.password:  # 登录成功
                    paper = teacher.models.Paper.objects.filter(major=student.major)
                    grade = teacher.models.Grade.objects.filter(sid=student.id)
                    insert_log(student.name, '登录')
                    return render(request, 'studentLogin.html', {'student': student, 'paper': paper, 'grade': grade})
                    # return render(request, 'index.html', {'message': '密码错误'})
                return HttpResponse('密码错误')
            except:
                # return render(request, 'index.html', {'message': '用户名不存在'})
                return HttpResponse('用户名不存在')
            # return render(request, 'index.html', {'message': '验证码错误'})
        return HttpResponse('验证码错误')
    return HttpResponse('404 error')


# 学生考试 的视图函数
def startExam(request):
    sid = request.GET.get('sid')
    subject1 = request.GET.get('subject')

    student = models.Student.objects.get(id=sid)
    paper = teacher.models.Paper.objects.filter(subject=subject1)
    # print(type(paper[0].pid.through.Paper_pid))
    paper_len = len(paper[0].pid.all())
    return render(request, 'exam.html', {'student': student, 'paper': paper, 'subject': subject1, 'paper_len':paper_len,'paper_score':paper_len*5})


# 计算由exam.html模版传过来的数据计算成绩
def calGrade(request):
    if request.method == 'POST':
        # 得到学号和科目
        sid = request.POST.get('sid')
        subject1 = request.POST.get('subject')

        # 重新生成Student实例，Paper实例，Grade实例，名字和index中for的一致，可重复渲染
        student = models.Student.objects.get(id=sid)
        paper = teacher.models.Paper.objects.filter(major=student.major)
        grade = teacher.models.Grade.objects.filter(sid=student.id)

        # 计算该门考试的学生成绩
        question = teacher.models.Paper.objects.filter(subject=subject1).values("pid").values('pid__id', 'pid__answer',
                                                                                              'pid__score')

        mygrade = 0  # 初始化一个成绩为0
        for p in question:
            qId = str(p['pid__id'])  # int 转 string,通过pid找到题号
            myans = request.POST.get(qId)  # 通过 qid 得到学生关于该题的作答
            # print(myans)
            okans = p['pid__answer']  # 得到正确答案
            # print(okans)
            if myans == okans:  # 判断学生作答与正确答案是否一致
                mygrade += p['pid__score']  # 若一致,得到该题的分数,累加mygrade变量

        # 向Grade表中插入数据
        teacher.models.Grade.objects.create(sid_id=sid, subject=subject1, grade=mygrade)
        # print(mygrade)
        # 重新渲染index.html模板
        return render(request, 'studentLogin.html', {'student': student, 'paper': paper, 'grade': grade})


# 向数据库中插入日志记录
def insert_log(user, operate):
    from django.db import connection
    import time
    ldate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    cursor = connection.cursor()
    sql = "insert into log values(null,%s,%s,%s) "
    val = (ldate, user, operate)
    cursor.execute(sql, val)
    try:
        connection.commit()
    except Exception:
        connection.rollback()


def logOut(request):
    del request.session['username']
    return HttpResponse('index.html')
