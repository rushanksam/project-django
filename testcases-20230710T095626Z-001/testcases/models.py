from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class POD(models.Model):
    pod_name = models.CharField(verbose_name='pod',max_length=150)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
            return self.pod_name


class DeviceConfig(models.Model):
    device_name = models.CharField(verbose_name='deviceconfig', max_length=150)   
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
            return self.device_name


class Milestone(models.Model):
    milestone_name = models.CharField(verbose_name='milestone', max_length=150)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
            return self.milestone_name

class Priority(models.Model):
    priority_name = models.CharField(verbose_name='priority',max_length=10) 
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
            return self.priority_name

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=["csv","xml","xls"])]) 
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE,related_name='milestone_up')
    device = models.ForeignKey(DeviceConfig, on_delete=models.CASCADE, related_name='device_up')
    priority = models.ForeignKey(Priority,on_delete=models.CASCADE, related_name='priority_up')
    pod = models.ForeignKey(POD, on_delete=models.CASCADE,related_name='pod_up')
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
          return f'{self.milestone.milestone_name}#{self.device.device_name}#{self.priority.priority_name}'


class TestCase(models.Model):
    passed = models.PositiveIntegerField(blank=True, default=0)
    passpercentage = models.PositiveIntegerField(blank=True, default=0)
    failed = models.PositiveIntegerField(blank=True, default=0)
    failpercentage = models.PositiveIntegerField(blank=True, default=0)
    blocked = models.PositiveIntegerField(blank=True, default=0)
    blockpercentage = models.PositiveIntegerField(blank=True, default=0)
    skipped = models.PositiveIntegerField(blank=True, default=0)
    skippercentage = models.PositiveIntegerField(blank=True, default=0)
    untested = models.PositiveIntegerField(blank=True, default=0)
    untestpercentage = models.PositiveIntegerField(blank=True, default=0)
    bugs = models.TextField(max_length=1000, blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, default=0)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE,related_name='milestone_tc')
    pod = models.ForeignKey(POD, on_delete=models.CASCADE,related_name='pod_tc')
    device = models.ForeignKey(DeviceConfig, on_delete=models.CASCADE, related_name='device_tc')
    priority = models.ForeignKey(Priority,on_delete=models.CASCADE, related_name='priority_tc')
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_dt = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
          verbose_name_plural='DashBoard'

    @property
    def pass_percentage(self):
        return f"{self.passpercentage} %"
    
    @property
    def fail_percentage(self):
          return f"{self.failpercentage} %"
    
    @property
    def block_percentage(self):
          return f"{self.blockpercentage} %"
    
    @property
    def untest_percentage(self):
          return f"{self.untestpercentage} %"
  
    @property
    def skip_percentage(self):
          return f"{self.skippercentage} %"





