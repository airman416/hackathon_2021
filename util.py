def extractForm(form):
    '''
    Converts form data into result dict
    '''
    result = dict()
    for element in form:
        if element.name != "csrf_token":
            result[element.name] = float(element.data)
    return result



def calcCF(result):
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
    dailyEnergy = (1.1 * result["nRoom"] * result["nAC"]) + (0.72 * result["nRoom"]) + (0.3 * result["nPC"]) + (6 * result["nLarge"])
    footprint["Energy"] = 0.465 * dailyEnergy
    
    # Calculate Carbon Footprint of eating Meat and Non-meat
    footprint["Food"] = (0.01205 * result["pMeat"] * result["foodCost"]) + (0.00596 * (1 - result["pMeat"]) * result["foodCost"])
    
    # Calculate Carbon Footprint of Car, Public Transport, and Plane
    footprint["Transport"] = (2.857 * result["carSize"] * result["nCar"]) + (0.257 * result["nPublic"]) + (0.395 * result["nPlane"])
    
    return footprint


def compareCF(footprint):
    '''
    Compares the footprint relative to Japan's average carbon footprint per person per year
    Average: 9.09 tonnes in 2019
    
    E.g. If footprint = 8 tonnes
    "13.6% below average"
    
    If footprint = 12 tonnes
    "32.0% above average"
    '''
    percentDiff = round((100 * (footprint - 9.09)/9.09), 1)     # percentage change to one decimal place
    return f"{percentDiff}% above average" if percentDiff >= 0 else f"{-percentDiff}% below average"