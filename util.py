'''
Quiz
                *Value*                                             *Key in quiz Dict*
                rooms (bedroom and living room)                     nRoom
                daily hours with AC turned on                       nACHour
                hours on PC                                         hPC
                furniture (washing machines,refridgerators)         nLarge
                
                hours per week of driving                           hCar
                hours per week of public transportation             hPublic
                number of time traveled by airplane per year        nPlane

MCQ
                *Value*                                             *Key in mcquiz Dict*
                how big is your car                                 carSize
                what percent of your food is meat                   pMeat
                how much they spend on food per day                 foodCost
'''


def cleanQuiz(quiz, mcquiz):
    '''
    Converts mcquiz result into usable values and merges the result with the quiz result
    '''
    
    # emission per km based on car size
    if mcquiz["carSize"] == "small":
        quiz["carSize"] = 0.00017
    elif mcquiz["carSize"] == "medium":
        quiz["carSize"] = 0.00022
    elif mcquiz["carSize"] == "large":
        quiz["carSize"] = 0.00027
    else:
        quiz["carSize"] = 0
    
    # % of meal that's meat
    if mcquiz["pMeat"] == "0~20%":
        quiz["pMeat"] = 0.1
    elif mcquiz["pMeat"] == "20~40%":
        quiz["pMeat"] = 0.3
    elif mcquiz["pMeat"] == "40~60%":
        quiz["pMeat"] = 0.5
    elif mcquiz["pMeat"] == "60~80%":
        quiz["pMeat"] = 0.7
    else:
        quiz["pMeat"] = 1
    
    # money spent on food
    if mcquiz["foodCost"] == "<500 yen":
        quiz["foodCost"] = 500
    elif mcquiz["foodCost"] == "500~1000 yen":
        quiz["foodCost"] = 750
    elif mcquiz["foodCost"] == "1000~1500 yen":
        quiz["foodCost"] = 1250
    elif mcquiz["foodCost"] == "1500~2000 yen":
        quiz["foodCost"] = 1750
    else:
        quiz["foodCost"] = 2250
    
    return quiz



def calcCF(quiz):
    '''
    Takes the quiz data and calculates the carbon footprint of each factor in tonnes/day
    
    For Energy
    kWH/day * tonnes/kWH
    
    For Food
    tonnes/yenMeat * yenMeat/day + tonnes/yenOther * yenOther/day
    
    For Transport
    (tonnes/hourCarWeek * hourCarWeek / 7days) + (tonnes/hourPublicWeek * hourPublicWeek / 7days) + (tonnes/rideYear * rideYear / 365days)
    '''
    footprint = dict()
    
    # Calculate Carbon Footprint of AC, Lighting, PC, and other appliances
    dailyEnergy = (0.8 * quiz["nRoom"] * quiz["nACHour"]) + (0.72 * quiz["nRoom"]) + (0.3 * quiz["hPC"]) + (4 * quiz["nLarge"])
    footprint["Energy"] = 0.000465 * dailyEnergy
    
    # Calculate Carbon Footprint of eating Meat and Non-meat
    footprint["Food"] = (0.00001205 * quiz["pMeat"] * quiz["foodCost"]) + (0.00000596 * (1 - quiz["pMeat"]) * quiz["foodCost"])
    
    # Calculate Carbon Footprint of Car, Public Transport, and Plane
    footprint["Transport"] = (2.857 * quiz["carSize"] * quiz["hCar"]) + (0.000257 * quiz["hPublic"]) + (0.000395 * quiz["nPlane"])
    
    return footprint



def totalCF(footprint):
    '''
    Calculates total footprint of all factors
    '''
    return sum(footprint.values())



# Test
quiz = dict()
mcquiz = dict()

quiz["nRoom"] = 4
quiz["nACHour"] = 5
quiz["hPC"] = 24
quiz["nLarge"] = 5

quiz["hCar"] = 0
quiz["hPublic"] = 10
quiz["nPlane"] = 3

mcquiz["carSize"] = "medium"
mcquiz["pMeat"] = "0~20%"
mcquiz["foodCost"] = "<500 yen"


footprint = calcCF(cleanQuiz(quiz, mcquiz))

print("\n\n\n")
print(f"Energy: {footprint['Energy'] * 365} tonnes per year")
print(f"Food: {footprint['Food'] * 365} tonnes per year")
print(f"Transport: {footprint['Transport'] * 365} tonnes per year\n\n")
print(f"Total footprint: {totalCF(footprint) * 365} tonnes per year")