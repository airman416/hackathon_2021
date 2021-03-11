import matplotlib.pyplot as plt
import io
import base64
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# matplotlib plot colors
OVERALL = "mediumslateblue"
ENERGY = "orangered"
FOOD = "gold"
TRANSPORT = "deepskyblue"


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



def calcPercent(cf):
    '''
    Calculates the percentage contribution of each factor
    '''
    if cf == None:       # return nothing when there are no entries
        return {'Energy': 0.0, 'Food': 0.0, 'Transport': 0.0}
    
    percent = dict()
    percent['Energy'] = round(100 * cf.energy / cf.daily, 1)
    percent['Food'] = round(100 * cf.food / cf.daily, 1)
    percent['Transport'] = round(100 * cf.transport / cf.daily, 1)
    return percent



def compareCF(cf):
    '''
    Compares the footprint relative to Japan's average carbon footprint per person per year
    Average: 9.09 tonnes in 2019
    
    E.g. If cf = 8 tonnes
    "13.6% below average"
    
    If cf = 12 tonnes
    "32.0% above average"
    '''
    if cf == None:       # return nothing when there are no entries
        return ""
    
    percentDiff = round((100 * (cf.yearly - 9.09)/9.09), 1)     # percentage change to one decimal place
    return f"{percentDiff}% above average" if percentDiff >= 0 else f"{-percentDiff}% below average"



def recommend(cf):
    '''
    Recommends tips to reduce carbon footprint based on which values are represented the most
    '''
    form = cf.form
    tips = []
    
    urglist = {     # weight of each factors
        'nRoom': form['nRoom']*2,
        'nAC': form['nAC']/3 + 1,
        'nPC': form['nPC']/2,
        'nLarge': form['nLarge']*2,
        'pMeat': form['pMeat']*10 + 3,
        'nPlane': form['nPlane']*2 + 2,
        'nCar': form['nCar']/2
    }
    urg = max(urglist, key=urglist.get) # most important factors
    
    if form['nRoom'] >= 4 or urg == 'nRoom':
        tips.append("""<li class="energy">Only turn on the AC in one room at a time</li>""")
    
    if form['nAC'] >= 10 or urg == 'nAC':
        tips.append("""<li class="energy">Close the curtains to reduce heat loss</li>""")
        tips.append("""<li class="energy">Close the doors when using the AC</li>""")
        tips.append("""<li class="energy"><a href=""https://www.appropedia.org/How_to_cool_a_room_with_water target="_blank">Place a bowl of water</a> to cool the room</li>""")
        tips.append("""<li class="energy">Add double glazing to your windows</li>""")
    
    if form['nPC'] >= 10 or urg == 'nPC':
        tips.append("""<li class="energy">Reduce monitor brightness</li>""")
        tips.append("""<li class="energy">Set the computer to sleep mode when not in use</li>""")
        tips.append("""<li class="energy">Close softwares that you are not using</li>""")
        tips.append("""<li class="energy">Use <a href="<a href="https://download.cnet.com/PowerSlave/3000-2094_4-10921574.html" target="_blank">Powerslave</a> to shutdown at certain times</li>""")
        tips.append("""<li class="energy">Try some of the tips in <a href="https://www.techradar.com/news/computing/pc/the-ultimate-guide-to-reducing-your-pc-s-power-consumption-661978/3" target="_blank">this guide</a></li>""")
    
    if form['nLarge'] >= 3 or urg == 'nLarge':
        tips.append("""<li class="energy">Pull out the plugs of appliances you are not using to prevent <a href="https://massachusetts.revolusun.com/blog/is-ghost-electricity-haunting-your-electric-bill/" target="_blank">ghost electricity<a></li>""")
        tips.append("""<li class="energy">Run the washing machine in bulk</li>""")
        tips.append("""<li class="energy"><a href="https://www.organicauthority.com/live-grow/cleaning-a-refrigerator-properly" target="_blank">Clean your refrigerator</a></li>""")
        tips.append("""<li class="energy">Opt for a water and electric efficient furniture <a href="https://www.energystar.gov/products/most_efficient" target="_blank">(ie showerhead, dish washer, cloth washer)</a></li>""")
        tips.append("""<li class="energy">Opt for an energy certified <a href="https://www.energystar.gov/" target="_blank"> (ie ENERGY STAR) </a> electric furniture</li>""")
        tips.append("""<li class="energy">Run the washing machine with cold water</li>""")
    
    if form['pMeat'] >= 0.5 or urg == 'pMeat':
        tips.append("""<li class="food">Experiment with new grains, vegetables and <a href="https://www.allrecipes.com/recipes/87/everyday-cooking/vegetarian/" target="_blank">recipes</a></li>""")
        tips.append("""<li class="food">Bulk up meat dishes with beans, grains or vegetable</li>""")
        tips.append("""<li class="food">Try substituting your favourite foods for meat free versions</li>""")
        tips.append("""<li class="food">Participate in <a href="https://www.mondaycampaigns.org/meatless-monday" target="_blank">Meatless Monday</a></li>""")
        tips.append("""<li class="food">Look to the cuisines of countries with well-known vegetarian dishes</li>""")
    
    if form['nPlane'] >= 3 or urg == 'nPlane':
        tips.append("""<li class="transport">Use non-stop flights</li>""")
        tips.append("""<li class="transport">Fly economy or coach on planes</li>""")
        tips.append("""<li class="transport"><a href="https://thepointsguy.com/guide/everything-you-need-to-know-carbon-offsetting-flights/" target="_blank"> Offset your flight emissions</a></li>""")
        tips.append("""<li class="transport">Use public transports such as busses and trains</li>""")
        tips.append("""<li class="transport"><a href="https://www.nytimes.com/2017/07/27/climate/airplane-pollution-global-warming.html" target="_blank">Learn the effects of flying</a></li>""")
    
    if form['nCar'] >= 4 or urg == 'nCar':
        tips.append("""<li class="transport">Use a <a href="https://youtu.be/9RXY8TRMMzs" target="_blank">cleaning agent</a> for your cars</li>""")
        tips.append("""<li class="transport">Change your <a href="https://www.rac.co.uk/drive/advice/car-maintenance/how-to-check-your-oil/" target="_blank">engine oil</a></li>""")
        tips.append("""<li class="transport">Avoid constant breaking and accelerating when on your car</li>""")
        tips.append("""<li class="transport">Reduce the idle time of your cars</li>""")
        tips.append("""<li class="transport">Optimize your <a href="https://youtu.be/IFbx6INKc2Y" target="_blank">tire pressure</a></li>""")
    
    return random.sample(tips, min(len(tips), 10))  # pick up to 10 random tips



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
    ax.plot(dates, daily_values, color=OVERALL, label='Total')
    ax.plot(dates, energy_values, color=ENERGY, label='Energy')
    ax.plot(dates, food_values, color=FOOD, label='Food')
    ax.plot(dates, transport_values, color=TRANSPORT, label='Transport')
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
    
    ax.bar(date, transport, color=TRANSPORT, label='Transport')
    ax.bar(date, food, color=FOOD, label='Food', bottom=transport)
    ax.bar(date, energy, color=ENERGY, label='Energy', bottom=food+transport)
    ax.set_ylabel("Footprint (kg per day)")
    ax.set_xticks([])   # Hide xticks
    ax.legend(bbox_to_anchor=(0, 0, 1, 1), loc='upper left')
    
    return plotToImg(fig)