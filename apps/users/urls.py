# _*_ coding: utf-8 _*_
# __author__ = 'syss'
# __date__ = '2017/5/8 0008 下午 9:32'

from django.conf.urls import url
from .views import UserInfoView, UpdateImage, UpdatePwdView, UpdateEmailView,\
    SendEmailCodeView, UserCoursesView, UserFavView, UserMessageView


urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UpdateImage.as_view(), name='upload_image'),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='upload_pwd'),
    # 发送验证码邮件
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^user_courses/$', UserCoursesView.as_view(), name='user_courses'),
    url(r'^user_fav/$', UserFavView.as_view(), name='user_fav'),
    url(r'^user_message/$', UserMessageView.as_view(), name='user_message'),

]
