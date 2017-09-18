# _*_ encoding: utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

from organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    course = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时常')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图片', max_length=200)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    category = models.CharField(default=u'后端开发', verbose_name=u'课程类别', max_length=20)
    tag = models.CharField(default='', max_length=20, verbose_name=u'标签')
    notice = models.CharField(max_length=100, verbose_name=u'课程公告', default='')
    teacher = models.ForeignKey(Teacher, verbose_name=u'授课讲师', null=True, blank=True)
    you_need_know = models.CharField(max_length=300, default='', verbose_name=u'课程须知')
    teacher_tells_you = models.CharField(max_length=300, default='', verbose_name=u'老师告诉你')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_chapter(self):
        return self.lesson_set.all().order_by('-add_time')

    # 获取章节数量
    def get_chapter_nums(self):
        return self.lesson_set.all().count()

    def learn_users(self):
        return self.usercourse_set.all()[:3]

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.URLField(max_length=200, default='', verbose_name=u'视频链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResources(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='courses/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
