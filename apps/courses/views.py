# _*_ encoding: utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from random import sample
from operation.models import UserFavorate, CourseComments, UserCourse
from .models import Course, CourseResources
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        current_page = 'course'
        all_courses = Course.objects.all().order_by('add_time')
        sort = request.GET.get('sort', '')
        recommended_courses = Course.objects.all().order_by('-click_nums')[:3]
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 4, request=request)
        all_courses = p.page(page)

        return render(request, 'course-list.html',
                      {
                          'current_page': current_page,
                          'all_courses': all_courses,
                          'sort': sort,
                          'recommended_courses':recommended_courses,
                       })


class CourseDetailView(View):
    def get(self, request, course_id):
        has_fav_org = False
        has_fav_course = False
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            recommend_courses = sample(Course.objects.filter(tag=tag), 1)
        else:
            recommend_courses = []
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_type=2, fav_id=course.course.id):
                has_fav_org = True
            if UserFavorate.objects.filter(user=request.user, fav_type=1, fav_id=course.id):
                has_fav_course = True

        return render(request, 'course-detail.html', {
            'course': course,
            'recommend_courses': recommend_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseVideoView(LoginRequiredMixin, View):
    def get(self ,request, course_id):
        course = Course.objects.get(id=course_id)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids)
        related_courses_ids = [courses.course.id for courses in all_courses]
        related_courses = Course.objects.filter(id__in=related_courses_ids).order_by('-click_nums')[:4]

        course_resources = CourseResources.objects.filter(course=course)

        user_cor = UserCourse.objects.filter(user=request.user, course=course)
        if not user_cor:
            user_cor = UserCourse(user=request.user, course=course)
            user_cor.save()

        sort = request.GET.get('sort', '')
        comments = CourseComments.objects.all() if sort == 'comments' else []
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comments, 10, request=request)
        comments = p.page(page)

        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'sort': sort,
            'comments': comments,
            'related_courses': related_courses,
        })


class CommentsView(View):
    def post(self, request):
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        if course_id > 0 and comments:
            course = Course.objects.get(id=course_id)
            course_comment = CourseComments()
            course_comment.course = course
            course_comment.user = request.user
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type="application/json")

