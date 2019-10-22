import json

from django.shortcuts import render
from teacher import models
from django.http import HttpResponse

# 将使用原生sql语句查到的结果由tuple类型转换为dictionary(字典)类型
def dictfetchall(cursor):
    """
        将游标返回的结果保存到一个字典对象中
    """
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def get_student_score():
    import pymysql
    try:
        conn39 = pymysql.connect(**{"host": "127.0.0.1",
                                    "database": "exam",
                                    "user": "root",
                                    "passwd": "123456",
                                    "charset": "utf8"})
        cur39 = conn39.cursor()
        cur39.execute(
            "SELECT student.name name,grade.subject subject,grade.grade grade FROM "
            "student,grade WHERE student.id = grade.sid_id")
        return cur39.fetchall()
    except:
        return None

def score_analyse(request):
    if request.method == "GET":
        from django.db import connection
        subject1 = request.GET.get("subject")
        print(subject1)
        cursor = connection.cursor()
        sql = "select grade.subject,student.id,student.name,grade.grade " \
              "from grade inner join student on grade.subject = %s and grade.sid_id = student.id"
        cursor.execute(sql,[subject1])
        # 将查找的数据转成字典[{},{}]
        grade = dictfetchall(cursor)

        if grade:
            message = ""
        else:
            message = "I'm so sorry!无数据,请重新填写！"
        data1 = models.Grade.objects.filter(subject=subject1, grade__lt=60).count()
        data2 = models.Grade.objects.filter(subject=subject1, grade__gte=60, grade__lt=70).count()
        data3 = models.Grade.objects.filter(subject=subject1, grade__gte=70, grade__lt=80).count()
        data4 = models.Grade.objects.filter(subject=subject1, grade__gte=80, grade__lt=90).count()
        data5 = models.Grade.objects.filter(subject=subject1, grade__gte=90).count()

        data = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5,
                "grade":json.dumps(grade),"message":message}
        print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


def teacherLogin(request):
    if request.method == 'POST':
        info_dict = request.POST
        username = info_dict['username']
        password = info_dict['password']
        # user_type = info_dict['user_type']
        code = info_dict['code']
        # 获取验证码并且不区分大小写
        # 教师登录
        # if code.upper() == request.session['code'].upper():
        if code.upper() != request.session['code'].upper():
            try:
                grade = get_student_score()
                teacher = models.Teacher.objects.get(id=username)
                log = getOperate()
                # print(teacher)
                if password == teacher.password:  # 登录成功
                    return render(request, 'teacherLogin.html', {'teacher': teacher, 'grade': grade, 'log': log})
                return HttpResponse('密码不正确')
            except:
                return HttpResponse('用户名不正确')
        return HttpResponse('验证码不正确')
    return HttpResponse('404Error')


def exam_manager(request):
    """
    考试管理
    :param request:
    :return:
    """
    # 读取试题编号
    subjects = models.Paper.objects.all()
    return render(request, 'guideTest.html', {'subjects': subjects})





# 查看学生日志
def getOperate():
    from django.db import connection
    cursor = connection.cursor()
    sql = "select log.luser,student.id,student.major,log.operate,log.ldate " \
          "from log inner join student on log.luser = student.name"
    cursor.execute(sql)
    # 将查找的数据转成字典[{},{}]
    result = dictfetchall(cursor)
    return result


# 教师退出
def logOut(request):
    del request.session['username']
    return HttpResponse('index.html')
