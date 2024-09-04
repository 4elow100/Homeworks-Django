from django.contrib import admin

from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    filter_horizontal = ['teachers']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
