# _*_ encoding: utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from operation.models import UserFavorate
from models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from courses.models import Course

# Create your views here.


class OrgView(View):

    def get(self, request):
        current_page = 'org'
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        all_citys = CityDict.objects.all()
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', '')
        sort = request.GET.get('sort', '')

        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        if category:
            all_orgs = all_orgs.filter(category=category)
        if sort == 'courses':
            all_orgs = all_orgs.order_by('-courses')
        elif sort == 'students':
            all_orgs = all_orgs.order_by('-students')

        org_num = all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        # org_num = [index for index, em in enumerate(orgs.object_list)][-1] + 1

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_num': org_num,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'current_page': current_page,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type="application/json")

        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type="application/json")


class HomePageView(View):
    def get(self, request, org_id):
        current_page = 'home'
        org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        courses = org.course_set.all()[:3]
        teachers = org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'org': org,
            'courses': courses,
            'teachers': teachers,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCoursesView(View):
    def get(self, request, org_id):
        current_page = 'courses'
        org = CourseOrg.objects.get(id=org_id)
        courses = org.course_set.all()
        teachers = org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'org': org,
            'courses': courses,
            'teachers': teachers,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'org': org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgTeachersView(View):
    def get(self, request, org_id):
        current_page = 'teachers'
        org = CourseOrg.objects.get(id=org_id)
        teachers = org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'teachers': teachers,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        course = Course.objects.get(id=fav_id)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        exist_records = UserFavorate.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 取消收藏
            exist_records.delete()
            course.fav_nums -= 1
            course.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorate()
            if int(fav_type) > 0 and int(fav_id) > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save()
                course.fav_nums += 1
                course.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeachersListView(View):
    def get(self, request):
        current_page = 'teacher'
        teachers = Teacher.objects.all()
        nums = teachers.count()
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')
        recommended_teachers = teachers.order_by('-click_nums')[:5]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 1, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'current_page': current_page,
            'teachers': teachers,
            'sort': sort,
            'recommended_teachers': recommended_teachers,
            'nums': nums
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        has_teacher_fav = False
        has_org_fav = False

        teacher = Teacher.objects.get(id=teacher_id)
        courses = Course.objects.filter(teacher=teacher)
        org = teacher.org

        teacher_fav = UserFavorate.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3)
        if teacher_fav:
            has_teacher_fav = True
        org_fav = UserFavorate.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
        if org_fav:
            has_org_fav = True

        teachers = Teacher.objects.all().order_by('-click_nums')[:5]

        return render(request, 'teacher-detail.html', {
            'courses':courses,
            'org': org,
            'teacher': teacher,
            'teachers': teachers,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav
        })