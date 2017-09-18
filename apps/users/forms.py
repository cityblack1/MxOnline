# _*_ coding: utf-8 _*_
__author__ = 'syss'
__date__ = '2017/4/29 0029 下午 3:40'

from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile, EmailVerifyRecord


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})  # 生成url的验证码....黑科技


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyRecord
        fields = ['email']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birth', 'gender', 'address', 'mobile', ]