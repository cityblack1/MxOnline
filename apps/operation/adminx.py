# _*_ coding: utf-8 _*_
__author__ = 'syss'
__date__ = '2017/4/27 0027 下午 8:42'


from models import UserAsk, CourseComments, UserFavorate, UserMessage, UserCourse
import xadmin

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'add_time', 'course_name']
    search_field = ['name', 'mobile', 'add_time']
    list_filter = ['name', 'mobile', 'add_time', 'course_name']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_field = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserFavorateAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_field = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_field = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course']
    search_field = ['user', 'course']
    list_filter = ['user', 'course']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorate, UserFavorateAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)

