from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
import psutil
import socket
import os
import json

from .models import User, Information, ScanImage, Tracking_Calorie_Daily, Notification, MealPlan, Video,QR_Code
from .serializers import UserSerializer, InformationSerializer, ScanImageSerializer, TrackingSerializer, NotificationSerializer, MealPlanSerializer, VideoSerializer, QR_CodeSerializer


from .BMR_TDEECalculate import  TDEE_Calculate, Calorie_Daily, Macros,BMR_Calculate
from .GeminiAPI import SacnImage
from .ChatGPT import Chat_GPT_request
from .Unsplash import Image_Unsplash
from .Generate_QR_Code import Generate_QRCode
from . getIP import get_LocalIP




@api_view(['GET','POST'])
def Register(res):
    if res.method == 'GET':
        info = User.objects.all()
        serializer = UserSerializer(info, many= True)
        return Response(serializer.data)
    
    if res.method == 'POST':
        serializer = UserSerializer(data=res.data)
        Email = res.data.get('Email')
        FullName = res.data.get('FullName')

        print(Email)
        check_user = User.objects.filter(Email=Email).first()
        if not check_user:
        
            if serializer.is_valid():
                
                user = serializer.save()

                

                #Save the Email in the Information and everything is default
                Information.objects.create(
                    user=user,  
                    Age=25,  
                    Gender="Not Specified",  
                    Weight=0.0,  
                    Height=0.0,  
                    Fat=0.0,  
                    FitnessLevel="Beginner",  
                    Goal="Not Set", 
                    Active_Level="Not Specified",  
                    BMR_Calories=0.0,  
                    TDEE_Calorie=0.0 ,
                    Calorie_Daily = 0.0,
                    Protein_Daily = 0.0,
                    Carb_Daily =  0.0,
                    Fat_Daily =  0.0
                )

                Tracking_Calorie_Daily.objects.create(
                    user=user,  
                    Update_Status = False,
                    Calorie_Daily_Left = 0.0,
                    Protein_Daily_Left = 0.0,
                    Carb_Daily_Left = 0.0,
                    Fat_Daily_Left = 0.0,
                    Calorie_Did_Take = 0.0,
                    Protein_Did_Take = 0.0,
                    Fat_Did_Take = 0.0,
                    Carb_Did_Take = 0.0

                )

                
                print('Register success..')
                return Response({'message':'Register success..'}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": 'Email already exist in system!'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def Login(res):

    if res.method == 'POST':
        Email = res.data.get('Email')
        Password = res.data.get('Password')

        user = User.objects.filter(Email=Email).first()
        FullName = user.FullName
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not check_password(Password,user.Password):
            raise AuthenticationFailed('Incorrect Password')
        
        check_user = Information.objects.filter(user__Email = Email)
        check_user_tracking = Tracking_Calorie_Daily.objects.filter(user__Email = Email)

        if not check_user.exists():
            return Response({"message":"Login Success...", "FullName":FullName, "Email": Email, "TDEE": '0'}, status=status.HTTP_202_ACCEPTED)
        
        information = InformationSerializer(check_user, many=True)  ### Get data from Infomation Model
        

        tracking_update = TrackingSerializer(check_user_tracking, many=True) # Get data from Tracking Calorie Daily Model
    

        
        Calorie_from_current_info = information.data[0]['Calorie_Daily']
        Calorie_from_Tracking_daily = tracking_update.data[0]['Calorie_Daily_Left']
        Calorie_from_Tracking_daily = float(Calorie_from_Tracking_daily)

        if Calorie_from_Tracking_daily >= 1: # If Calorie in Tracking Calorie Daily Model != default then get the data from Infomation Model
            data_list = tracking_update.data[0]
            print('Get Calorie from Tracking Calorie Daily')
            data_location = 'Tracking_Model'
        
        else:
            data_list = information.data[0]
            print('Get Calorie from User Information Default')
            data_location = "Information_Model"
        
        
        Total_Marco_default = information.data[0] #maybe delete
        print("Login Success...")
        return Response({"message":"Login Success...", "data_location": data_location,"FullName":FullName, "Email": Email, "data_list":data_list, "Total_Marco_default": Total_Marco_default}, status=status.HTTP_202_ACCEPTED)
    

@api_view(['POST'])
def UserInformation(request):
    if request.method == 'POST':
        Email = request.data.get('user')
        Age = request.data.get('Age')
        Gender = request.data.get('Gender')
        Weight = request.data.get('Weight')
        Height = request.data.get('Height')
        Fat = request.data.get('Fat')
        FitnessLevel = request.data.get('Fitness Level')
        Goal = request.data.get('Goal')
        Active_Level = request.data.get('Active Level')

        check_user = Information.objects.filter(user__Email = Email)
        check_tracking_user = Tracking_Calorie_Daily.objects.filter(user__Email = Email)
        if not check_user.exists():
            return Response({"message": "Couldn't find you in our system!"} ,status=status.HTTP_400_BAD_REQUEST)
        
        BMR = BMR_Calculate(Age,Weight,Height,Gender) # Calculate BMR
        TDEE = TDEE_Calculate(BMR, Active_Level) # Calculate TDEE
        
        
        information =check_user.first()
        information.Age = Age
        information.Gender = Gender
        information.Weight = Weight
        information.Height = Height
        information.Fat = Fat
        information.FitnessLevel = FitnessLevel
        information.Goal = Goal
        information.Active_Level = Active_Level
        information.BMR_Calories = BMR
        information.TDEE_Calorie = TDEE

        information.save()
        
        info = InformationSerializer(check_user, many=True)
        user_Information = info.data[0]
        get_weight = user_Information['Weight']
        get_FitnessLevel = user_Information['FitnessLevel']
        get_Goal = user_Information['Goal']

        Calorie_daily = Calorie_Daily(BMR, TDEE, get_FitnessLevel, get_Goal) # Calculate Calories Daily

        macros = Macros(Calorie_daily, get_weight) # Calculate Marco
        information.Protein_Daily = macros['Protein']
        information.Carb_Daily = macros['Carb']
        information.Fat_Daily = macros['Fat']
        information.Calorie_Daily = Calorie_daily
        information.save()
            
        '''
            Calorie Daily include the final result of how much you need for a day
            use user_Information inclue all data about user like Age, Height, Weight, Goal
            Macro include Protein, fat, Carb

        '''
        print(f'Calorie Daily: {Calorie_daily}')
        return Response({"message":"Calculate succsess...", "Calorie_daily": Calorie_daily,"user_Information":user_Information, "Marcos": macros}, status=status.HTTP_202_ACCEPTED)
    
@api_view(['GET', 'POST'])
def Tracking_Calorie_API(res):
    if res.method == 'GET':
        info = Tracking_Calorie_Daily.objects.all()
        serializer = TrackingSerializer(info, many=True)
        return Response(serializer.data)
    if res.method == 'POST':
        
        Update_Status = res.data.get('Update_Status')
        Calorie_Did_Take = res.data.get("Calorie_Did_Take")
        Fat_Did_Take= res.data.get("Fat_Did_Take")
        Carb_Did_Take = res.data.get("Carb_Did_Take")
        Protein_Did_Take = res.data.get("Protein_Did_Take")

        Calorie_Daily_Left = res.data.get("Calorie_Daily_Left")
        Protein_Daily_Left = res.data.get("Protein_Daily_Left")
        Fat_Daily_Left = res.data.get("Fat_Daily_Left")
        Carb_Daily_Left = res.data.get("Carb_Daily_Left")

        Email = res.data.get('Email')

        check_user = Tracking_Calorie_Daily.objects.filter(user__Email = Email)

        information = check_user.first()
        information.Calorie_Did_Take = Calorie_Did_Take
        information.Fat_Did_Take = Fat_Did_Take
        information.Carb_Did_Take = Carb_Did_Take
        information.Protein_Did_Take = Protein_Did_Take
        information.Calorie_Daily_Left = Calorie_Daily_Left
        information.Protein_Daily_Left = Protein_Daily_Left
        information.Fat_Daily_Left = Fat_Daily_Left
        information.Carb_Daily_Left = Carb_Daily_Left
        information.save()
        

        check_info = TrackingSerializer(check_user, many=True)
        print('Calorie in a Daily has been updated...')
        # print(f"Calorie update daily: {check_info.data[0]}")

        return Response({'message': 'Got update Calorie data...', "data_list": check_info.data[0]}, status=status.HTTP_202_ACCEPTED)
    return Response({'message': 'Error 404 Server...'}, status=status.HTTP_400_BAD_REQUEST)


# Use for update Marce when user calculate a new BRM and TDEE
# DataBase will take the new Marce - to the macro is currenly taken than give to use a new macre base on that.
@api_view(['POST'])
def Update_Tracking_API(res):
    if res.method == 'POST':
        Email = res.data.get('Email')

        check_tracking_user = Tracking_Calorie_Daily.objects.filter(user__Email = Email)
        check_information_user = Information.objects.filter(user__Email = Email)
        
        get_information =InformationSerializer(check_information_user, many=True)
        get_tracking_info = TrackingSerializer(check_tracking_user, many=True)

        get_Calorie_Did_Take = get_tracking_info.data[0]["Calorie_Did_Take"]
        get_Protein_Did_Take = get_tracking_info.data[0]["Protein_Did_Take"]
        get_Fat_Did_Take = get_tracking_info.data[0]["Fat_Did_Take"]
        get_Carb_Did_Take = get_tracking_info.data[0]["Carb_Did_Take"]


        get_Calorie_Daily = get_information.data[0]["Calorie_Daily"]
        get_Protein_Daily = get_information.data[0]["Protein_Daily"]
        get_Fat_Daily = get_information.data[0]["Fat_Daily"]
        get_Carb_Daily = get_information.data[0]["Carb_Daily"]

        update_calorie_Left = float(get_Calorie_Daily) - float(get_Calorie_Did_Take)
        update_protein_left = float(get_Protein_Daily) - float(get_Protein_Did_Take)
        update_fat_left = float(get_Fat_Daily) - float(get_Fat_Did_Take)
        update_carb_left = float(get_Carb_Daily) - float(get_Carb_Did_Take)

        update_tracking = check_tracking_user.first()
        update_tracking.Calorie_Daily_Left = update_calorie_Left
        update_tracking.Protein_Daily_Left = update_protein_left
        update_tracking.Fat_Daily_Left = update_fat_left
        update_tracking.Carb_Daily_Left = update_carb_left
        update_tracking.save()     

        get_update_tracking_info = TrackingSerializer(check_tracking_user, many=True) 
        get_information =InformationSerializer(check_information_user, many=True)  
        
        

        return Response({"message": "Update Tracking Macro success...","Default_Information": get_information.data[0] ,"Update_tracking_Macro": get_update_tracking_info.data[0]}, status=status.HTTP_202_ACCEPTED)
    return Response({"Messege": "Error to Uddate Tracking Macro.."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def GetCalorieLeft(res):
    if res.method == 'POST':
        Request = res.data.get("Request")
        Email = res.data.get('Email')

        if Request == 'Get-CalorieLeft':
            check = Tracking_Calorie_Daily.objects.filter(user__Email = Email)
            get_Notification = TrackingSerializer(check, many=True)
            CalorieLeft = get_Notification.data[0]['Calorie_Daily_Left']
            return Response({"message": "Get Calorie left successfully..", "CalorieLeft": CalorieLeft}, status=status.HTTP_202_ACCEPTED)
    return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def ScanImage_API(request):
    if request.method == 'GET':
        info = ScanImage.objects.all()
        serializer = ScanImageSerializer(info, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ScanImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the uploaded image
            if serializer.data:
                Image_Url = serializer.data['image']
                IP = get_LocalIP()
         
                ObjectName = SacnImage(f'http://{IP}:8000{Image_Url}') # get the Local IP address Auto
             
                
                try:
                    data = json.loads(ObjectName)
                   
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
        
                # missing delete Image after Processing...
                
            return Response({'message': 'Upload success..', "imageUrl": Image_Url,'Image Data': serializer.data, 'Macro_Info': data}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST', 'GET'])
def Notification_API(request):
    
    if request.method == 'POST':
        Email = request.data.get('Email')
        Title = request.data.get('Title')
        Message = request.data.get('Message')
        Type = request.data.get('Type')
        Send_At = request.data.get('Send_At')
        ID = request.data.get('ID')
        Request = request.data.get('Request')

        check_user = User.objects.filter(Email=Email).first()

        if check_user is None :
            print('User is not in system')
            return Response({"message": "User is not in system"}, status=status.HTTP_409_CONFLICT)
        
        if Title:
            Notification.objects.create(
            user=check_user,
            Title = Title,
            Message = Message,
            Type = Type,
            Send_at = Send_At
        )
        
        if ID:
            checkID = Notification.objects.filter(id = ID)
            getIDInfo = NotificationSerializer(checkID, many=True)
            print(getIDInfo.data)
            checkID.delete()
            return Response({"Notification_Status": "Notification has been deleted."}, status=status.HTTP_200_OK)

        if Request:
            check = Notification.objects.filter(user__Email = Email)
            get_Notification = NotificationSerializer(check, many=True)
            return Response({"Notification": get_Notification.data}, status=status.HTTP_200_OK)
        
        return Response({"message": "Notification saved."}, status=status.HTTP_201_CREATED) 
    return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def MealPlan_API(res):
    if res.method == 'GET':
        info = MealPlan.objects.all()
        serializer = MealPlanSerializer(info, many= True)        
        return Response({"message": "get Meal Plan success..", "Data": serializer.data}, status=status.HTTP_202_ACCEPTED)
    

    if res.method == 'POST':
        serializer = MealPlanSerializer(data=res.data)
        Email = res.data.get('Email')
        Meal_Type = res.data.get('Meal_Type')
        FoodName = res.data.get('FoodName')
        Quantity = res.data.get('Quantity')
        QuantityValue = res.data.get('QuantityValue')
        Calorie = res.data.get('Calorie')
        Notes = res.data.get('Notes')

        check_user = User.objects.filter(Email = Email ).first()

        if check_user is None:
            return Response({"message": "Couldn't found user..."})
        
        check_Food = Chat_GPT_request(FoodName,Quantity, QuantityValue)
        convert_check_food = json.loads(check_Food)

        get_Food_Name = convert_check_food['FoodName']
        image_url = Image_Unsplash(get_Food_Name)
        
        if convert_check_food["Food"] == 'True' or convert_check_food["Food"] == 'true':
            MealPlan.objects.create(
                user=check_user,
                MealPlan_Status = False,
                Meal_Type = Meal_Type,
                FoodName = convert_check_food["FoodName"],
                Quantity = convert_check_food["Quantity"],
                Protein = convert_check_food["Protein"],
                Fat = convert_check_food["Fat"],
                Carb = convert_check_food["Carb"],
                Calorie = convert_check_food["Calories"],
                Notes = Notes,
                Image_url = image_url
            )

            getCalorie = convert_check_food["Calories"]

            return Response({'message':"Meal plan has saved..", "Calorie": getCalorie}, status=status.HTTP_201_CREATED)
        if not convert_check_food:
            return Response({'message':"Sorry, your input is not recognized"}, status=status.HTTP_200_OK)
        
        
        return Response({'error':"Sorry, your input is not recognized as food."}, status=status.HTTP_200_OK)

    return Response({'error':"Error to save Mael Plan !"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Get_MealPlan_API(res):
    if res.method == 'POST':
        Email = res.data.get('Email')

        check_user = User.objects.filter(Email = Email).first()
        if check_user is None:
            return Response({"message": "user is not in system.."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        check_MealPlan = MealPlan.objects.filter(user__Email = Email)
        set_MealPlan = MealPlanSerializer(check_MealPlan, many=True)
        return Response({"message": "Get Meal plan Success...", "Data": set_MealPlan.data}, status=status.HTTP_202_ACCEPTED)

    return Response({"message": "Error to get Meal Plan.."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def AddTrackingMeal_API(res):
    if res.method == 'POST':
        Request = res.data.get('Request')
        id = res.data.get('id')
        Email = res.data.get('Email')
        print(id)
        
        check_user = User.objects.filter(Email = Email).first()
        
        if(check_user is None):
            return Response({'message': 'User checking error'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if Request == 'Add':
                checkID = MealPlan.objects.filter(id = id)
                getIDInfo = MealPlanSerializer(checkID, many=True)
                print(getIDInfo.data[0])

                check_tracking = Tracking_Calorie_Daily.objects.filter(user__Email = Email)
                get_Tracking = TrackingSerializer(check_tracking, many=True)
                print(get_Tracking.data[0])

                Calorie_Daily_Left = float(get_Tracking.data[0]['Calorie_Daily_Left']) - float(getIDInfo.data[0]['Calorie']) 
                Protein_Daily_Left = float(get_Tracking.data[0]['Protein_Daily_Left']) - float(getIDInfo.data[0]['Protein']) 
                Carb_Daily_Left = float(get_Tracking.data[0]['Carb_Daily_Left']) - float(getIDInfo.data[0]['Carb'])
                Fat_Daily_Left = float(get_Tracking.data[0]['Fat_Daily_Left']) - float(getIDInfo.data[0]['Fat'])

                Calorie_Did_Take = float(get_Tracking.data[0]['Calorie_Did_Take']) + float(getIDInfo.data[0]['Calorie']) 
                Protein_Did_Take = float(get_Tracking.data[0]['Protein_Did_Take']) + float(getIDInfo.data[0]['Protein']) 
                Carb_Did_Take = float(get_Tracking.data[0]['Carb_Did_Take']) + float(getIDInfo.data[0]['Carb'])
                Fat_Did_Take = float(get_Tracking.data[0]['Fat_Did_Take']) + float(getIDInfo.data[0]['Fat'])
                


                updateInfo = check_tracking.first()
                updateInfo.Calorie_Daily_Left = Calorie_Daily_Left
                updateInfo.Protein_Daily_Left = Protein_Daily_Left
                updateInfo.Carb_Daily_Left = Carb_Daily_Left
                updateInfo.Fat_Daily_Left = Fat_Daily_Left

                updateInfo.Calorie_Did_Take = Calorie_Did_Take
                updateInfo.Protein_Did_Take = Protein_Did_Take
                updateInfo.Carb_Did_Take = Carb_Did_Take
                updateInfo.Fat_Did_Take = Fat_Did_Take
                updateInfo.save()
                w = 'Carb_Daily_Left'
                q = 'Carb'
                a = f'{get_Tracking.data[0][w]} - {getIDInfo.data[0][q]}'
                print(f'{a} = {Carb_Daily_Left}')
            
                return Response({"message": "add tracking meal success..", "Request": Request}, status=status.HTTP_202_ACCEPTED)
            if Request == 'Remove':
                print(Request)
                checkID = MealPlan.objects.filter(id = id)
                getIDInfo = MealPlanSerializer(checkID, many=True)
                print(getIDInfo.data)
                checkID.delete()
                return Response({"message": "Remove the meal successfully..", "Request": Request}, status=status.HTTP_202_ACCEPTED)

    return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Profile_API(res):
    if res.method == 'POST':

        Email = res.data.get('Email')
        Request = res.data.get('Request')
        Input = res.data.get('Input')
        checkUSer = User.objects.filter(Email=Email)
        checkInfo = Information.objects.filter(user__Email=Email)

        if Request == 'Delete':
            user = User.objects.filter(Email=Email).first()
            if user:
                user.delete()
            return(Response({"message": "Delete Account Successfully"}, status=status.HTTP_202_ACCEPTED))
        if Request == 'ChangeName':
           
            change = checkUSer.first()
            change.FullName=Input
            change.save()
            return(Response({"message": "Change Name Successfully", "Name": Input}, status=status.HTTP_202_ACCEPTED))

        if Request == 'ChangeAge':
            change = checkInfo.first()
            change.Age=Input
            change.save()
            return(Response({"message": "Change Age Successfully", "Age": Input}, status=status.HTTP_202_ACCEPTED))

        if Request == 'ChangeHeight':
            change = checkInfo.first()
            change.Height=Input
            change.save()
            return(Response({"message": "Change Height Successfully", "Height": Input}, status=status.HTTP_202_ACCEPTED))
        
        if Request == 'ChangeWeight':
            change = checkInfo.first()
            change.Weight=Input
            change.save()
            return(Response({"message": "Change Weight Successfully", "Weight": Input}, status=status.HTTP_202_ACCEPTED))

        if Request == 'Get_Info':
            check_user = Information.objects.filter(user__Email=Email)
            get_info = InformationSerializer(check_user, many=True)
           
            return(Response({"message": "Get Info Successfully", "Info": get_info.data[0]}, status=status.HTTP_202_ACCEPTED))


    return (Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST))


@api_view(['POST', 'GET'])
def Video_API(request):
    if request.method == 'POST':
        Category = request.data.get('Categogy')  
        Video_Type = request.data.get('Video_Type')
        VideoID = request.data.get('Video_ID')

        

        if Category == 'Muscle Group':
            
            check = Video.objects.filter(Category=Category)
            if check.exists():
                print('Video exist')
                check_Video_type = Video.objects.filter(Type = Video_Type)

                get_Videos_Type = VideoSerializer(check_Video_type, many=True)   
                return Response({"Video_data": get_Videos_Type.data, "message": "Get videos successfully"}, status=status.HTTP_200_OK)

        if Category == 'Strength' or Category == 'CrossFit' or Category == 'Cardio' or Category == 'Full-Body':
            check_category = Video.objects.filter(Category = Category)
            get_video = VideoSerializer(check_category, many=True)
           
            return Response({"Video_data":get_video.data, "message": "Get videos successfully"}, status=status.HTTP_200_OK)
        
        

        if VideoID:
            checkID = Video.objects.filter(id=VideoID)
            get_VideURL = VideoSerializer(checkID, many=True)
            URL = get_VideURL.data[0]['Video']
            video_title = get_VideURL.data[0]['Title']
            print(URL)
            return Response({"VideoURL": URL,"Video_Title": video_title, "message": "Get URL successfully.."}, status=status.HTTP_200_OK)

    return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def QRCode(res):
    if res.method == 'POST':
        Request = res.data.get('Request')
        Email = res.data.get('Email')
        FullName = res.data.get('FullName')

        if Request == 'Get_QRCode':
            message = f'Get {FullName} Information'

            check_QR_Code = QR_Code.objects.filter(user__Email=Email)
            if not check_QR_Code:
                print('Create new QR code')
                user = User.objects.filter(Email=Email).first()
                QR_img = Generate_QRCode(FullName, message)
                QR_Code.objects.create(
                    user=user,
                    QR_Code=QR_img
                )
                
            check_user = QR_Code.objects.filter(user__Email=Email)
            get_QR = QR_CodeSerializer(check_user,many=True)
            return Response({"message": "got QR code", "QR_Code":get_QR.data[0]['QR_Code']}, status=status.HTTP_200_OK)
    return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)