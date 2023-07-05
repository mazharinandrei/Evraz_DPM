from django.contrib import admin
from .models import ActionType, Fact, Plan, Profile, Standart, WorkShift, WorkShiftType

# Register your models here.

admin.site.register(ActionType)
admin.site.register(Fact)
admin.site.register(Plan)
admin.site.register(Profile)
admin.site.register(Standart)
admin.site.register(WorkShift)
admin.site.register(WorkShiftType)

