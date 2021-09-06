from django.contrib import admin

# Register your models here.
from .models import ApprovalRequest, Department, Identity


class RequestAdmin(admin.ModelAdmin):
    fields = '__all__'

admin.site.register(ApprovalRequest)


class DepartmentAdmin(admin.ModelAdmin):
    fields = '__all__'

admin.site.register(Department)


class IdentityAdmin(admin.ModelAdmin):
    fields = '__all__'

admin.site.register(Identity)