def blood_pressure_label(sys, dias):

    if sys <= 120 and dias <= 80:
        return 'normal'
    elif sys < 90 and dias < 60:
        return 'low'
    elif (sys > 120 and sys <= 129) and dias < 80:
        return 'elevated'
    elif (sys >= 130 and sys <= 139) or (dias >= 80 and dias <= 89):
        return 'high_stage_1'
    elif sys >= 140 or dias >= 90:
        return 'high_stage_2'
    elif sys > 180 or dias > 120:
        'hypertensive_crisis'


def overweight_label(imc):

    if imc < 18.5  :
        return 'underweight'
    elif imc >= 18.5 and imc < 25:
        return 'healthy'
    elif imc >= 25 and imc < 30:
        return 'overweight'
    elif imc >= 30 < 35:
        return 'obesity_class1'
    elif imc >= 35 < 40:
        return 'obesity_class2'
    elif imc >= 40:
        return 'severe_obesity'


class Cardio(object):


    ### TRANSFORMATION ###
    def transformation(self, test):
        new_cols = ['id', 'age', 'gender', 'height', 'weight', 'systolic_pressure', 'diastolic_pressure', 'cholesterol', 'glucose', 'smoke', 'alcohol_intake', 'active', 'cardio_disease']

        test.columns = new_cols

        # Converting age from days to years
        test['age'] = test['age'].apply(lambda x: int(x/365))

        return test


    ### FEATURE ENGINEERING ###
    def feature_enginearing(self, test):


        # Body mass Index
        test['bmi'] = test['weight']/(test['height']/100)**2

        # Weight Consition
        test['weight_condition'] = test['bmi'].apply(lambda x: overweight_label(x))

        #  Blood Pressure Level
        test['blood_pressure_level'] = test[['systolic_pressure', 'diastolic_pressure']].apply(lambda x: blood_pressure_label(x['systolic_pressure'], x['diastolic_pressure']), axis=1)

        # Cholesterol and Glucose
        levels = {1: 'normal', 2: 'above_normal', 3:'well_above_normal'}

        test['cholesterol'] = test['cholesterol'].map(levels)
        test['glucose'] = test['glucose'].map(levels)

        test['gender'] = test['gender'].apply(lambda x: 'male' if x == 2 else 'female')

        return test


    ### DATA FILTERING ###
    def filtering(self, test):

        test = test.query('diastolic_pressure <= 140 & diastolic_pressure > 50')
        test = test.query('systolic_pressure <= 250 & systolic_pressure >= 80')
        test = test.query('systolic_pressure > diastolic_pressure')
        test = test.query('height > 65.24')


        X_test = test.drop('cardio_disease', axis=1)
    
        return X_test