from django.contrib import admin
from .models import *

# Register your models here.

class MarksAdmin(admin.ModelAdmin):
    list_display = ('type','sem_no','roll_no','s1','s2','s3','s4','s5','s6','s7','s8')
    
admin.site.register(Marks ,MarksAdmin)

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('sem_no','roll_no', 'status','cst','ot','csp','op','s1','s2','s3','s4','s5','s6','s7','s8')
    
admin.site.register(Semester ,SemesterAdmin)
