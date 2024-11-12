from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User, Information,ScanImage,Tracking_Calorie_Daily, Notification, MealPlan,Video,QR_Code



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        Password = validated_data.pop('Password', None)
        instance = self.Meta.model(**validated_data)
        if Password is not None:
            instance.Password = make_password(Password) # make password the hash
            instance.save()
        return instance
    
    
class QR_CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QR_Code
        fields = '__all__'
        
    

class InformationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Information
        fields = '__all__'


class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking_Calorie_Daily
        fields = '__all__'

class ScanImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScanImage
        fields = ['id', 'image']


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
    
class MealPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = MealPlan
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'