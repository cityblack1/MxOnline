# _*_ coding: utf-8 _*_
# __author__ = 'syss'
# __date__ = '2017/4/27 0027 下午 7:43'


from models import CityDict, CourseOrg, Teacher
import xadmin


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_field = ['name', 'desc']
    list_filter = ['name', 'desc']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time' ]
    search_field = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time' ]


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_field = ['org', 'name', 'work_years', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
