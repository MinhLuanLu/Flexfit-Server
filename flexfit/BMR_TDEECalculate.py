def BMR_Calculate(age, weight, height, gender):
    """
    Calculate Basal Metabolic Rate (BMR) based on age, weight, height, and gender.
    
    :param age: Age in years
    :param weight: Weight in kg
    :param height: Height in cm
    :param gender: Gender ('Male' or 'Female')
    :return: BMR value
    """
    if gender == "Female":
        BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161
    elif gender == "Male":
        BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        raise ValueError("Invalid gender. Choose 'Male' or 'Female'.")
    
    return BMR


def TDEE_Calculate(BMR, activity):
    """
    Calculate Total Daily Energy Expenditure (TDEE) based on BMR and activity level.
    
    :param BMR: Basal Metabolic Rate
    :param activity: Activity level ('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Super Active')
    :return: TDEE value
    """
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.9
    }

    if activity in activity_multipliers:
        TDEE = BMR * activity_multipliers[activity]
    else:
        raise ValueError("Invalid activity level. Choose from 'Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Super Active'.")
    
    return TDEE


def Calorie_Daily(BMR, TDEE, FitnessLevel, Goal):
    """
    Calculate daily calorie needs based on fitness level and goal.
    
    :param BMR: Basal Metabolic Rate
    :param TDEE: Total Daily Energy Expenditure
    :param FitnessLevel: Fitness level ('Newbie', 'Beginner', 'Intermediate', 'Advanced')
    :param Goal: Fitness goal ('Build Muscle', 'Build Strength', 'Lose Fat')
    :return: Daily calorie intake
    """
    if FitnessLevel in ['Newbie', 'Beginner']:
        if Goal == 'Lose Fat':
            result = (BMR + TDEE) / 2 - 250
        else:  # For muscle building or strength
            result = (BMR + TDEE) / 2 + 250
    elif FitnessLevel in ['Intermediate', 'Advanced']:
        if Goal == 'Lose Fat':
            result = TDEE - 250  # Adjust to a range of 500-700 if needed
        else:  # For muscle building or strength
            result = TDEE + 250
    else:
        raise ValueError("Invalid FitnessLevel. Choose from 'Newbie', 'Beginner', 'Intermediate', or 'Advanced'.")
    
    return result


def Macros(Calorie_daily, bodyweight):
    """
    Calculate macronutrient distribution based on total daily caloric intake (TDEE).
    
    :param TDEE: Total Daily Energy Expenditure
    :return: Dictionary with protein, carbohydrate, and fat amounts in grams
    """
    
    protein = 1.8 * float(bodyweight)
    proteinCalorie = float(protein) * 4
    print(f'Protein in gram: {protein} g')
    print(f'Protein Calorie: {proteinCalorie} Kcal')

    fat = 0.88 * float(bodyweight)
    fatCalorie = float(fat) * 9
    print(f'Fat in gram: {fat} g')
    print(f'Fat Calorie: {fatCalorie} Kcal')

    calorietaken = float(proteinCalorie) + float(fatCalorie)
    print(f'Calorie Taken: {proteinCalorie} + {fatCalorie}: {calorietaken} Calories Taken')

    calorieleft = float(Calorie_daily) - float(calorietaken)
    print(f'Calorie Left for Carb: {Calorie_daily} - {calorietaken}:  {calorieleft} Kcal')

    carb = float(calorieleft) / 4
    print(f'Carb in gram: {carb} g')

    protein = round(protein,1)
    fat = round(fat,1)
    carb = round(carb,1)

    

    result = {"Protein": protein, "Carb": carb, "Fat": fat}

    return result
