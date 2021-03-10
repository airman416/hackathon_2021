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
    if footprint == None:       # return nothing when there are no entries
        return ""
    
    percentDiff = round((100 * (footprint.yearly - 9.09)/9.09), 1)     # percentage change to one decimal place
    return f"{percentDiff}% above average" if percentDiff >= 0 else f"{-percentDiff}% below average"



def recommend(cf):
    #{'nRoom': 5.0, 'nAC': 3.0, 'nPC': 8.0, 'nLarge': 4.0, 'pMeat': 0.5, 'foodCost': 750.0, 'carSize': 0.22, 'nCar': 5.0, 'nPublic': 4.0, 'nPlane': 0.0}

    
    form = cf.form
    reco=[]
    sug=""
    sdg=""" <a href="https://sdgs.un.org/goals" target="_blank">Visit the UN SDGs Page!</a> """
    urg=0 #sclae of 1~ to apply a level to decide which suggestion to show


    # this is just used for testing the function and it's urgency sorting. 
    #------------------------------------------


    # template for link inb
    # <a href="" target="_blank"> </a>

    # form['nPlane']*2 + 2
    #-----------------------------------------
    if urg <= (form['nAC']/3 +1):
        sug="""
            <ul>
                <li>Close curtains to prevent energy loss </li> 
                <li>Create shade around your home</li>
                <li>Use a fan instead of AC</li>
                <li>Insulate your home</li>
                <li>Upgrade your windows</li>
                <li>Raise the target temperature when you are not home</li>
                <a href="<a href="https://www.economist.com/leaders/2018/08/25/how-to-make-air-conditioning-more-sustainable" target="_blank"> Want to know more?</a>
            </ul>
                """
        urg=(form['nAC']/3 +1)
            

    if urg <= (form['nPC']/2):
        sug="""
            <ul>
                <li>Reduce monitor brightness</li>
                <li>Set the computer to sleep when not used</li>
                <li>Set the computer's mode to battery saving scheme</li>
                <li>Use a software</li> <a href="<a href="https://download.cnet.com/PowerSlave/3000-2094_4-10921574.html" target="_blank"> (ie PowerSlave) </a> to shutdown at certain times</li>
                <li>Close softwares that you are not using</li>
                <li>Underclock the computer components</li>
                <a href="https://www.techradar.com/news/computing/pc/the-ultimate-guide-to-reducing-your-pc-s-power-consumption-661978/3" target="_blank">Want to know more? </a>

            </ul>
                """
        urg=(form['nPC']/2)

    if urg <= (form['nLarge']*2):
        sug="""
            <ul>
                <li>Clean your refrigerator</li>
                <li>Reorganize your refrigerator</li>
                <li>Run the washing machine in large quantities</li>
                <li>Run the washing machine with cold water</li>
                <li>Opt for an energy certified <a href="https://www.energystar.gov/" target="_blank"> (ie ENERGY STAR) </a> electric furniture</li>
                <li>Opt for a water and electric efficient furniture <a href="https://www.energystar.gov/products/most_efficient" target="_blank">(ie showerhead, dish washer, cloth washer)</a></li>
                <a href="https://www.treehugger.com/how-to-go-green-in-the-kitchen-4858697" target="_blank">Want to know more?</a>
            </ul>
                """    
        urg=(form['nLarge']*2)


    if urg <= (form['pMeat']*10 + 3):
        sug="""
            <ul>
                <li>Experiment with new grains, vegetables and <a href="https://www.allrecipes.com/recipes/87/everyday-cooking/vegetarian/" target="_blank">recipes</a></li>
                <li>Bulk up meat dishes with beans, grains or vegetable</li>
                <li>Try substituting your favourite foods for meat free versions</li>
                <li>Look to the cuisines of countries with well-known vegetarian dishes</li>
                <li><a href="https://www.sustainweb.org/sustainablefood/meat_and_dairy_products_less_is_more/" target="_blank">Try going meat free for one day a week</a></li>
                <li>Buy meat on the bone</li>
                <a href="https://www.treehugger.com/strategies-reducing-meat-your-diet-4852990" target="_blank">Want to know more?</a>
                
            </ul>
                """  
        urg = (form['pMeat']*10 + 3)


    if urg <= (form['nPlane']*2 + 2):
        sug="""
            <ul>
                <li>Choose non-stop flights</li>
                <li>Fly Economy or Coach</li>
                <li>Try to avoid flying</li>
                <li><a href="https://thepointsguy.com/guide/everything-you-need-to-know-carbon-offsetting-flights/" target="_blank"> Offset your emissions</a></li>
                <li>Use other means of transportation</li>
                <li><a href="https://www.nytimes.com/2017/07/27/climate/airplane-pollution-global-warming.html" target="_blank">Learn the effects of flying </a></li>
                <a href="https://www.pbs.org/newshour/science/these-7-simple-airplane-fixes-could-halve-carbon-emissions-at-little-to-no-cost" target="_blank"> Want to know more?</a>
            </ul>
            """
        urg = (form['nPlane']*2 + 2)



    if urg <= (form['nCar']/2):
        sug="""
            <ul>
                <li>Use a cleaning agent <a href="https://youtu.be/9RXY8TRMMzs" target="_blank">(Video)</a></li>
                <li>Change the engine oil <a href="https://www.rac.co.uk/drive/advice/car-maintenance/how-to-check-your-oil/" target="_blank">(How?)</a></li>
                <li>Change the air filter</li>
                <li>Optimize your tyre pressure <a href="https://youtu.be/IFbx6INKc2Y" target="_blank">(How?)</a></li>
                <li>Reduce the use of car AC</li>
                <li>Avoid constant breaking and accelerating</li>
                <li>Reduce idle time</li>
                <li>Refrain from driving</li>
                <a href="https://www.epa.gov/transportation-air-pollution-and-climate-change/what-you-can-do-reduce-pollution-vehicles-and-engines" target="_blank">Want to know more? </a>
            </ul>
        """
        urg = ()

    reco=[sug, sdg]
    return reco



def plotToImg(fig):
    '''
    Converts a matplotlib pyplot object into a string that can be used as the html img tag
    '''
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plot_string = "data:image/png;base64,"
    plot_string += base64.b64encode(output.getvalue()).decode('utf8')
    return plot_string



def plotTime(cfs):
    '''
    Takes a query/list of carbon footprints and returns a plotted graph
    '''
    if cfs == []:       # return nothing if there are no entries
        return ""
    
    # get axis values
    dates = [i.date_added for i in cfs]
    daily_values = [i.daily for i in cfs]
    energy_values = [i.energy for i in cfs]
    food_values = [i.food for i in cfs]
    transport_values = [i.transport for i in cfs]
    
    # plot the graph
    fig, ax = plt.subplots()
    fig.set_size_inches(12.5, 4)
    ax.plot(dates, daily_values, color='blueviolet', label='Total')
    ax.plot(dates, energy_values, color='firebrick', label='Energy')
    ax.plot(dates, food_values, color='gold', label='Food')
    ax.plot(dates, transport_values, color='steelblue', label='Transport')
    ax.set_ylabel("Footprint (kg per day)")
    ax.set_xlabel("Date")
    ax.legend(bbox_to_anchor=(0, 0, 1, 1), loc='upper left')
    
    # convert plot to string in order to display it and return it
    return plotToImg(fig)



def plotOverview(cf):
    '''
    Takes the most recent footprint and returns a stacked bar graph
    '''
    if cf == None:       # return nothing if there are no entries
        return ""
    
    # get axis values
    date = cf.date_added
    energy = cf.energy
    food = cf.food
    transport = cf.transport
    
    # plot the graph
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 6)
    
    ax.bar(date, energy, color='firebrick', label='Energy')
    ax.bar(date, food, color='gold', label='Food')
    ax.bar(date, transport, color='steelblue', label='Transport')
    ax.set_ylabel("Footprint (kg per day)")
    ax.set_xticks([])   # Hide xticks
    ax.legend(bbox_to_anchor=(0, 0, 1, 1), loc='upper left')
    
    return plotToImg(fig)