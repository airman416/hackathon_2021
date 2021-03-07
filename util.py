def cleanQuiz(quiz, mcquiz):
    '''
    Converts mcquiz result into usable values and merges the result with the quiz result
    '''
    
    # e.g. for mcquiz["pMeat"]
    # If 0% of the meal is meat, add quiz["meatFrequency"] = 0
    # If 50% of the meal is meat, add quiz["meatFrequency"] = 0.5
    # etc. Convert MCQ data into useful values
    
    # e.g. for mcquiz["foodCost"]
    # If the user answered 0-1000 yen, add quiz["foodCost"] = 500
    
    return quiz



def calcCF(quiz):
    '''
    Takes the quiz data and calculates the daily carbon footprint of each factors
    '''
    footprint = dict()
    
    # Calculate Carbon Footprint of AC, Lighting, PC, and other appliances
    dailyEnergy = (0.8 * quiz["nRoom"] * quiz["nACHour"]) + (0.72 * quiz["nRoom"]) + (0.3 * quiz["nPC"]) + (4 * quiz["nLarge"])
    footprint["Energy"] = 0.000465 * dailyEnergy
    
    # Calculate Carbon Footprint of eating Meat and Non-meat
    footprint["Food"] = (0.00001205 * quiz["pMeat"] * quiz["foodCost"]) + (0.00000596 * (1 - quiz["pMeat"]) * quiz["foodCost"])
    
    # Calculate Carbon Footprint of Transport
    footprint["Transport"] = 0
    
    return footprint



def totalCF(footprint):
    '''
    Calculates total footprint of all of the factors
    '''
    return sum(footprint.values())


'''
Quiz
                *Value*                                             *Key in quiz Dict*
                rooms (bedroom and living room)                     nRoom
                daily hours with AC turned on                       nACHour
                family members living with you                      nPeople
                hours on PC                                         nPC
                furniture (washing machines,refridgerators)         nLarge
                
                number of time traveled by airplane per year        nAirPlane
                hours per week of driving                           nDriving
                hours per week of public transportation             nPublic
                set ac temperature                                  nACTemp
                rough num. of windows                               nWINDOWS

MCQ
                *Value*                                             *Key in mcquiz Dict*
                what percent of their food is meat                  pMeat
                how much they spend on food per day                 foodCost
'''


# Test
quiz = dict()
quiz["nRoom"] = 3
quiz["nACHour"] = 3
quiz["nPeople"] = 3
quiz["nPC"] = 8
quiz["nLarge"] = 4
quiz["pMeat"] = 0.6
quiz["foodCost"] = 1500

footprint = calcCF(quiz)
print("\n\n\n")
print(f"Energy: {footprint['Energy'] * 365} tonnes per year")
print(f"Food: {footprint['Food'] * 365} tonnes per year")
print(f"Transport: {footprint['Transport'] * 365} tonnes per year\n\n")
print(f"Total footprint: {totalCF(footprint) * 365} tonnes per year")