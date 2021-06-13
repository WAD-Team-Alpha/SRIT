from django.contrib import admin
from .models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('fn','ln','email','usr_nm','roll_no','sem_no','branch')
    
admin.site.register(Student ,StudentAdmin)
