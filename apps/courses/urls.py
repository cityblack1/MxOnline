# _*_ coding: utf-8 _*_
# __author__ = 'syss'
# __date__ = '2017/5/8 0008 下午 9:32'

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseVideoView, CommentsView


urlpatterns = [
    url(r'^list/$',CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^comments/$', CommentsView.as_view(), name='add_comment'),

]
