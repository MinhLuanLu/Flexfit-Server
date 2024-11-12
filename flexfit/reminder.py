# reminder.py
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import User, Information, ScanImage, Tracking_Calorie_Daily, Notification, MealPlan
from .serializers import UserSerializer, InformationSerializer, ScanImageSerializer, TrackingSerializer, NotificationSerializer, MealPlanSerializer

def Reminder():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = datetime.now().strftime("%H:%M:%S")
    
    get_user = User.objects.all()
    serializer = UserSerializer(get_user, many=True)
    all_user_list = serializer.data

    for user_data in all_user_list:
        email = user_data['Email']
        make_Notification(email, time) 

def make_Notification(email,time):
    Tilte = ''
    Message = ''
    Type = ''
    create = False

    Morning='08:00:00'
    Midday='12:00:00'
    Afternoon='16:00:00'
    Evening='20:00:00'

    if time == Morning:
        Tilte = 'Breakfast'
        Message = 'Bearkfast time'
        Type = 'Reminder'
        create = True
        
    if time == Midday:
        Tilte = 'Lunch Time'
        Message = 'Eat your lunch'
        Type = 'Reminder'

    if time == Afternoon:
        Tilte = 'Meal Time'
        Message = 'Remember eat your meal'
        Type = 'Reminder'
        create = True

    if time == Evening:
        Tilte = 'Dinner Time'
        Message = 'Eat your dinner'
        Type = 'Reminder'
        create = True

    user_instance = User.objects.filter(Email=email).first()
    
    if user_instance and create == True:
        Notification.objects.create(
        user=user_instance,            # Use the user instance
        Title= Tilte,
        Message= Message,
        Type=Type,
        Send_at=time
        )
        if create == True:
            print(f'{user_instance} Notification has been create at {time}')
            create = False

    
    
def Run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(Reminder, 'interval', seconds=1)
    scheduler.start()
    return scheduler
