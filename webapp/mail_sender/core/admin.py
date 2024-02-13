from django.contrib import admin
from .models import *


# @admin.register(Email)
# class EmailAdmin(admin.ModelAdmin):
#     list_display = '__all__'
admin.site.register(SingleEmail)
admin.site.register(MassEmail)
admin.site.register(TaskCore)