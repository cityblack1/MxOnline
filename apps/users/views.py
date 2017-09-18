# _*_ coding:utf-8 _*_
import json
from utils.email_send import send_register_email
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.mixin_utils import LoginRequiredMixin

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageForm, UpdateEmailForm, UserInfoForm
from django.http import HttpResponse
from operation.models import UserCourse, UserFavorate, UserMessage
from courses.models import Course, Teacher
from organization.models import CourseOrg


# Create your views here.


# 自定义认证用户名密码的方法, 系统会自动调用
isExist = False
class CustomBackend(ModelBackend):   # 重定向进行用户名的验证
    # ModelBackend 类有一个方法可以被自动调用
    def authenticate(self, username=None, password=None, **kwargs):
        global isExist
        try:  # 查询POST的用户名或者邮箱是否和数据库内部匹配, 如果匹配就把他们都视为用户名,再去匹配他们的密码是不是和数据库匹配
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            isExist = True   # 这里面有一个问题啊, 就是万一邮箱被用作用户名的情况
            if user.check_password(password):   # 所以在注册用户名的时候要严格匹配防止其成为邮箱的格式
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                if record.is_used == False:
                    email = record.email
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    record.is_used = True
                    record.save()
                    user.save()
                else:
                    return render(request, 'active_fail.html')
            return render(request, 'login.html', {})
        else:
            return render(request, 'active_fail.html')


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form,})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        register_form.is_valid()
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': u'用户已经存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = u'欢迎注册'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):    # 通过回调类的方式处理路由
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)  # 将前端传递进来的字典进行验证
        # login_form.is_valid()
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 实际调用的是自己定义的 authenticate 的方法而不是原本的方法. 因为在setting设定了自定义
            user = authenticate(username=user_name, password=pass_word)
            if isExist == False:
                return render(request, 'login.html', {'msg': u'用户不存在'})
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:return render(request, 'login.html',{'login_form': login_form, 'msg': u'用户未激活'})
            else:
                return render(request, 'login.html',{'login_form': login_form, 'msg': u'用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                if record.is_used == False:
                    record.is_used = True
                    record.save()
                    return render(request, 'password_reset.html', {'email': email})
                else:
                    return render(request, 'active_fail.html', {})

        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'active_fail.html', {'email': email, 'msg':u'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'active_fail.html', {'email': email, 'modify_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        try:
            user_form = UserInfoForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return HttpResponse('{"status":"success"}', content_type="application/json")
            else:
                a = request.POST['birth']
                if '-' not in a:
                    birth = a.replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
                    address = request.POST.get('address', '')
                    gender = request.POST.get('gender', '')
                    mobile = request.POST.get('mobile', '')
                    nick_name = request.POST.get('nick_name', '')

                    user = request.user
                    user.birth = birth
                    user.gender = gender
                    user.address = address
                    user.nick_name = nick_name
                    user.mobile = mobile
                    user.save()
                    return HttpResponse('{"status":"success"}', content_type="application/json")

                else:
                    return HttpResponse(json.dumps(user_form.errors), content_type='application/json')
        except:
            pass


class UpdateImage(LoginRequiredMixin, View):
    def post(self, request):
        image_form = ImageForm(request.POST, request.FILES, instance=request.user)
        if image_form:
            image_form.save()
        return None


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"fail", "msg":"邮箱已经存在"}', content_type="application/json")
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type="application/json")

class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email_form = UpdateEmailForm(request.POST)
        if email_form.is_valid():
            email = request.POST.get('email', '')
            code = request.POST.get('code', '')
            try:
                record = EmailVerifyRecord.objects.get(code=code, email=email)
                if record:
                    if not record.is_used:
                        record.is_used = True
                        user = request.user
                        user.email = email
                        user.save()
                        record.save()
                        return HttpResponse('{"status":"success"}', content_type="application/json")
                    else:
                        return HttpResponse(json.dumps(email_form.errors), content_type='application/json')
                else:
                    return HttpResponse(json.dumps(email_form.errors), content_type='application/json')
            except:
                return HttpResponse(json.dumps(email_form.errors), content_type='application/json')
        else:
            return HttpResponse(json.dumps(email_form.errors), content_type='application/json')


class UserCoursesView(LoginRequiredMixin, View):
    def get(self, request):
        user_course = UserCourse.objects.filter(user=request.user) or []
        all_courses = [course.course for course in user_course]

        return render(request, 'usercenter-mycourse.html', {
            'all_courses': all_courses,
        })


class UserFavView(LoginRequiredMixin, View):
    def get(self, request):
        sort = request.GET.get('sort', '')
        if sort == '':
            org_fav = UserFavorate.objects.filter(user=request.user, fav_type=2) or []
            all_orgs = [CourseOrg.objects.get(id=org.fav_id) for org in org_fav]

            return render(request, 'usercenter-fav-org.html', {
                'all_orgs': all_orgs,
                'sort': sort,
            })
        if sort == 'course':
            course_fav = UserFavorate.objects.filter(user=request.user, fav_type=1) or []
            all_courses = [Course.objects.get(id=course.fav_id) for course in course_fav]
            return render(request, 'usercenter-fav-org.html', {
                'all_courses': all_courses,
                'sort': sort,
            })
        if sort == 'teacher':
            teacher_fav = UserFavorate.objects.filter(user=request.user, fav_type=3) or []
            all_teachers = [Teacher.objects.get(id=teacher.fav_id) for teacher in teacher_fav]
            return render(request, 'usercenter-fav-org.html', {
                'all_teachers': all_teachers,
                'sort': sort,
            })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        user_messages = UserMessage.objects.filter(Q(user=request.user.id) | Q(user=0)) or []

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_messages, 3, request=request)
        user_messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'user_messages': user_messages,
        })

