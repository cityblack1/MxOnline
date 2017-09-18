# _*_ coding: utf-8 _*_
# __author__ = 'syss'
# __date__ = '2017/5/8 0008 下午 9:32'

from django.conf.urls import url
from .views import TeachersListView, OrgView, AddUserAskView, HomePageView, OrgCoursesView, OrgDescView, OrgTeachersView, AddFavView, TeacherDetailView


urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home_page/(?P<org_id>\d+)/$', HomePageView.as_view(), name='home_page'),
    url(r'^courses/(?P<org_id>\d+)/$', OrgCoursesView.as_view(), name='courses'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='desc'),
    url(r'^teachers/(?P<org_id>\d+)/$', OrgTeachersView.as_view(), name='teachers'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    url(r'^teachers/list/$', TeachersListView.as_view(), name='teachers_list'),
    url(r'^teachers/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teachers_detail'),
]
