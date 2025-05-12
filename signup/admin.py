from django.contrib import admin
from .models import  EmployeeNumber,UserProfile,Crop,Livestock,Equipment

admin.site.register(EmployeeNumber)
admin.site.register(Crop)
admin.site.register(Livestock)
admin.site.register(Equipment)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'employee_number')