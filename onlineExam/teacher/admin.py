from django.contrib import admin
from .models import Teacher, Paper, Question, Grade


# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'dept', 'password', 'email', 'birth')
    list_display_links = ('id', 'name')
    search_fields = ['name', 'dept', 'birth']
    list_filter = ['name', 'dept']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'title', 'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'level', 'score')


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('tid', 'major', 'subject', 'examtime')
    list_display_links = ('major', 'subject', 'examtime')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('sid', 'subject', 'grade',)
    list_display_links = ('sid', 'subject', 'grade',)
    # fk_fields = ['sid']
