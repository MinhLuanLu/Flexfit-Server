from django.contrib import admin
from .models import User, Information, ScanImage, Tracking_Calorie_Daily, Notification, MealPlan, Video,QR_Code


admin.site.register(User)
admin.site.register(Information)
admin.site.register(ScanImage)
admin.site.register(Tracking_Calorie_Daily)
admin.site.register(Notification)
admin.site.register(MealPlan)
admin.site.register(Video)
admin.site.register(QR_Code)
