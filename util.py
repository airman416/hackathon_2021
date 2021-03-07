def CalculateFootprint(quiz):
    '''
    Takes the quiz data and calculates the daily carbon footprint
    '''
    # Calculate daily energy usage in kWH of AC, Lighting, PC, and other appliances
    dailyEnergy = (0.8 * quiz["nRoom"] * quiz["nACHour"])**0.5 + (0.36 * quiz["nRoom"]) + (0.3 * quiz["nPC"]) + min(15, (2 * quiz["nLarge"]))
    
    # Calculate the Carbon Footprint
    return (0.000465 * dailyEnergy) + 0 + 0


'''
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
                food waste                                          pFood
                recycled trash                                      pRecycle
'''