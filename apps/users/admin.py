# _*_ coding:utf-8 _*_
from django.contrib import admin
from .models import EmailVerifyRecord,Banner
from django import forms

# Register your models here.

class EmailVerifyRecordAdminForm(forms.ModelForm):
    def clean_name(self):
        # do something that validates your data
        return self.cleaned_data["email"]


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    # form = EmailVerifyRecordAdminForm
    # exclude = ['code']
    list_display = ['code', 'email', 'send_type', 'send_time', 'status']
    # fields = (('code', 'email', 'status'), 'send_type', 'send_time')
    #ordering = ['email']
    fieldsets = (
        ('sbbbbb', {
            'fields': ('code', 'email')
        }),
        ('Advanced options', {
            'description':('You son of a bitch!'),
            'fields': ('send_type', 'send_time'),
        }),
    )
    actions = ['make_published']

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        self.message_user(request, '%s 篇文章成功被标记为"p"' % rows_updated)
    make_published.short_description = u"将文章状态标记为'p'"


admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

# @admin.register(Banner)
# class PersonAdmin(admin.ModelAdmin):
#     date_hierarchy = 'add_time'



# @admin.register(Banner)
# class BannerAdmin(admin.ModelAdmin):
#     pass
# class EmailVerifyRecordAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)