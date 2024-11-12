from django.db import models

class User(models.Model):
    FullName = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50, unique=True)
    Password = models.CharField(max_length=500)
    Policy = models.BooleanField()
    Date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.FullName} - Joined by {str(self.Date_created)}"
    
class Information(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Age = models.DecimalField(max_digits=5, decimal_places=1)
    Gender = models.CharField(max_length=50)
    Weight = models.DecimalField(max_digits=5, decimal_places=1) 
    Height = models.DecimalField(max_digits=5, decimal_places=1)  
    Fat = models.DecimalField(max_digits=5,decimal_places=1)
    FitnessLevel = models.CharField(max_length=100)
    Goal = models.CharField(max_length=100)
    Active_Level = models.CharField(max_length=100)
    BMR_Calories = models.DecimalField(max_digits=10, decimal_places=1)
    TDEE_Calorie = models.DecimalField(max_digits=10, decimal_places=1)
    Calorie_Daily = models.DecimalField(max_digits=5, decimal_places=1)
    Protein_Daily = models.DecimalField(max_digits=5, decimal_places=1)
    Carb_Daily =  models.DecimalField(max_digits=5, decimal_places=1)
    Fat_Daily =  models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return f'{self.user} / {self.Age}'
    
class Tracking_Calorie_Daily(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Update_Status = models.BooleanField()
    Calorie_Daily_Left = models.DecimalField(max_digits=5, decimal_places=1)
    Protein_Daily_Left = models.DecimalField(max_digits=5, decimal_places=1)
    Carb_Daily_Left =  models.DecimalField(max_digits=5, decimal_places=1)
    Fat_Daily_Left =  models.DecimalField(max_digits=5, decimal_places=1)
    Calorie_Did_Take = models.DecimalField(max_digits=5,decimal_places=1)
    Protein_Did_Take = models.DecimalField(max_digits=5,decimal_places=1)
    Fat_Did_Take = models.DecimalField(max_digits=5,decimal_places=1)
    Carb_Did_Take = models.DecimalField(max_digits=5,decimal_places=1)

    def ___str__(self):
        return f'{self.user} - {self.Update_Status}'

    
class ScanImage(models.Model):
    image = models.ImageField(upload_to='Image/')

    def __str__(self):
        return self.image
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Message = models.CharField(max_length=5000)
    Type = models.CharField(max_length=100)
    Send_at = models.CharField(max_length=100)
    Created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} / {self.Type}: {self.Created_at} "
    

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MealPlan_Status = models.BooleanField()
    Meal_Type = models.CharField(max_length=100)
    FoodName = models.CharField(max_length=100)
    Quantity = models.CharField(max_length=100)
    Protein = models.CharField(max_length=100)
    Fat = models.CharField(max_length=100)
    Carb = models.CharField(max_length=100)
    Calorie = models.CharField(max_length=100)
    Notes = models.CharField(max_length=1000)
    Image_url = models.CharField(max_length=1000)


class Video(models.Model):
    Title = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Video = models.FileField(upload_to="videos/")
    Thumbnail = models.ImageField(upload_to="videos_thumbnail/")
    Uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.Category} - {self.Title}'
    
class QR_Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    QR_Code = models.ImageField(upload_to="QR_Code/")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user}'s QR Code Created at {self.create_at}")