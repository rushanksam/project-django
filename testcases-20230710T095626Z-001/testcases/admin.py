from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.forms import Textarea
from django import forms
from django.forms import TextInput, Textarea
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

admin.autodiscover()
admin.site.enable_nav_sidebar = False


# Register your models here.

@admin.register(POD)
class PlatformAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(DeviceConfig)
class DeviceConfig(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False



@admin.register(Milestone)
class Milestone(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(TestCase)
class TestCaseAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('priority','Passed','passPercent','Failed','failPercent',
                    'Blocked','blockPercent','Skipped','skipPercent','Untested',
                    'untestPercent','Total','bugs_refrence','device_name','pod_name','milestone_name', 'remarks')        
    #list_filter = ('priority__priority_name', 'device__device_name','milestone__milestone_name')
    list_filter = (
        ('priority__priority_name', DropdownFilter),
        ('device__device_name', DropdownFilter),
        ('pod__pod_name', DropdownFilter),
        ('milestone__milestone_name', DropdownFilter)
    )
    list_editable = ('remarks',)
    
    def priority(self, obj):
        return f'<b>{obj.priority.priority_name}</b>'

    def device_name(self, obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('blue', obj.device.device_name))
    
    def pod_name(self, obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('blue', obj.pod.pod_name))
    
    def milestone_name(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('blue', obj.milestone.milestone_name))
    
    def bugs_refrence(self,obj):
        if obj.bugs:
            bugs_list = obj.bugs.split('#')
            return mark_safe('<b style="color:{};">{}</b>'.format('red', bugs_list))
        return obj.bugs 
    
    def Passed(self, obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('green', obj.passed))

    def passPercent(self, obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('green', obj.pass_percentage))
        
    def Failed(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('red', obj.failed))

    def failPercent(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('red', obj.fail_percentage))
    
    def Skipped(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('darkslategray', obj.skipped))
        
    def skipPercent(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('darkslategray', obj.skip_percentage))
        
    def Blocked(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('purple', obj.blocked))
        
    def blockPercent(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('purple', obj.block_percentage))
        
    def Untested(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('darkkhaki', obj.untested))
        
    def untestPercent(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('darkkhaki', obj.untest_percentage))
        
    def Total(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('blue', obj.total))

    def remarks(self,obj):
        return mark_safe('<b style="color:{};">{}</b>'.format('yellow', obj.remarks))
    
    def has_add_permission(self, request):
        return False
    
    # This will help you to disable change functionality
    # def has_change_permission(self, request, obj=None):
    #     return False



    
          
    
admin.site.register(Upload)
