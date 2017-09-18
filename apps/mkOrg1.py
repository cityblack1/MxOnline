# _*_ coding: utf-8 _*_
import os,django
from MxOnline import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxOnline.settings")# project_name 项目名称
django.setup()
import random
from apps.organization.models import CourseOrg, CityDict


list2 = [u'幕课网', u'长安大学0', u'长安大学1', u'长安大学2', u'长安大学3', u'长安大学4', u'长安大学5', u'长安大学6', u'长安大学7', u'长安大学8', u'长安大学9', u'长安大学10', u'长安大学11']


def main():
    a = CityDict.objects.all()
    city_num = CityDict.objects.count()
    for org in list2:
        c = CourseOrg.objects.get_or_create(name=org)[0]
        c.name=org
        c.desc=org+u'的描述'
        c.address = org+u'的地址'
        c.image = u'org/%Y/%m'
        c.city = a[random.randint(0, city_num - 1)]
        c.save()

if __name__ == '__main__':
    main()
    print 'Done!'




