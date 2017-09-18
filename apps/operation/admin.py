from django.contrib import admin
from .models import UserCourse
from django import forms
# Register your models here.


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']


admin.site.register(UserCourse, UserCourseAdmin)

