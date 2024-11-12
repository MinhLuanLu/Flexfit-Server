from django.urls import path

from . import views

urlpatterns = [
    path('Register/api', views.Register,name='Register'),
    path('Login/api', views.Login, name='Login'),
    path('Information/api', views.UserInformation, name="Information"),
    path('ScanImage/api', views.ScanImage_API, name='ScanImage_API'),
    path('Tracking_Calorie/api', views.Tracking_Calorie_API,name='Tracking_Calorie_API'),
    path('Update_Tracking_Calorie/api', views.Update_Tracking_API, name='Update_Tracking_API'),
    path('Notification/api', views.Notification_API, name='Notification'),
    path('MealPlan/api', views.MealPlan_API, name='MealPlan_API'),
    path('Get/MealPlan/api', views.Get_MealPlan_API, name='Get_MealPlan_API'),
    path('AddTrackingMeal/api', views.AddTrackingMeal_API, name='AddTrackingMeal/api'),
    path('GetCalorieLeft/api', views.GetCalorieLeft, name='GetCalorieLeft'),
    path('Profile/api', views.Profile_API, name='Profile/api'),
    path('Video/api', views.Video_API, name='Video/API'),
    path('QRCode/api', views.QRCode, name ='QRCode')
]