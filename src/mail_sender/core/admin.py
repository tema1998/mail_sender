from django.contrib import admin

from .models import *

# @admin.register(Email)
# class EmailAdmin(admin.ModelAdmin):
#     list_display = '__all__'

admin.site.register(EmailHistory)
admin.site.register(TaskCore)
admin.site.register(TaskHistory)
