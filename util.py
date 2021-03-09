import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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



def recommend(cf):
    '''
    Takes in a footprint object and returns suggestions
    '''
    form = cf.form
    return []



def plot(cfs):
    '''
    Takes a query/list of carbon footprints and returns a javascript of the plot of
    Time against footprint
    '''
    # get axis values
    dates = [i.date_added for i in cfs]
    daily_values = [i.daily for i in cfs]
    energy_values = [i.energy for i in cfs]
    food_values = [i.food for i in cfs]
    transport_values = [i.transport for i in cfs]
    
    # plot the graph
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 4)
    p1, = ax.plot(dates, daily_values, color='blueviolet', label='Total')
    p2, = ax.plot(dates, energy_values, color='firebrick', label='Energy')
    p3, = ax.plot(dates, food_values, color='gold', label='Food')
    p4, = ax.plot(dates, transport_values, color='steelblue', label='Transport')
    ax.set_ylabel("Footprint (tonnes per year)")
    ax.set_xlabel("Date")
    ax.legend(handles=[p1, p2, p3, p4])
    
    # convert plot to string in order to display it
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plot_string = "data:image/png;base64,"
    plot_string += base64.b64encode(output.getvalue()).decode('utf8')

    return plot_string