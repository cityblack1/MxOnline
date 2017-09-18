# _*_ coding: utf-8 _*_
from django.apps import AppConfig
from django.db.models.signals import post_save


class OrganizationConfig(AppConfig):
    name = 'organization'
    verbose_name = u'教育机构'
    label = 'organization'  # <-- this is the important line - change it to anything other than the default, which is the module name ('foo' in this case)

    def ready(self):
        from signals import someSignal
        post_save.connect(
            receiver=someSignal,
            sender=self.get_model('CourseOrg')
        )

