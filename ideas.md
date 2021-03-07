# Brainstorming:

Issues caused by COVID:
    Hospitalization
    Isolation
    Logistics in infrastrucutre and communities
    Childcare? 
    Education cannot be done within classrooms
    going outside
    

https://inhabitat.com/14-apps-to-help-you-live-a-more-eco-friendly-sustainable-lifestyle/
https://footprint.wwf.org.uk/#/

# Carbon Footprint Calculator

Answer a few initial questions then answer a short question every day to track your carbon footprint
Values:
    1. Food
    2. Transport
    3. Home
    4. Others

> Footprint = (Annaual_Energy_Usage_in_KWH * Energy_Factor) + (Amount_of_Food * Food_Factor) + (Amount_of_Transport * Transport_Factor)
> 
> Energy_Factor = Tonnes of CO2 per KWH of energy (Use online statistics on what % of energy comes from where to calculate this coefficient)
> Food_Factor = Tonnes of CO2 per kg of food (different for each food, collect data on what % of food is meat, vegetables, etc)
> Transport_Factor = Tonnes of CO2 per km of transport (calculate based on what % of transport is done on what) 

## Energy Factor
*Factor*     *Source* *%*    *Normalized %*
0.968kg/kWH  Coal     26% -> 27%
0.413kg/kWH  LNG      21% -> 22%
0.219kg/kWH  LPG      
0.260kg/kWH  Petrol   40% -> 42%
0.050kg/kWH  Solar    6%  -> 6%
0.004kg/kWH  Nuclear  3%  -> 3%

Total Factor = 0.465kg/kWH = 0.000465ton/kWH

## Transport Factor
*Factor*  *Vehicle*   *Average Daily Distance*
0.17kg/km Small car   
0.22kg/km Medium car
0.27kg/km Large car
0.06kg/km Train
0.15kg/km Plane         






Questions: 
```
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
```
                
                
Points of improvements:



Project Description:
    Due to Covid-19, the topic of sustianbility has been badly neglected and so our [name of app] will solve the lack of public knowledge on sustainablity by providing a metric to individual users on their impacts of their actions.



# Website Outline

```
If file doesnt exist: 
    First time login -> Short quiz, create CFCalculator object and save object in file
    Go to main page
Else:
    Go to main Page
    Display carbon footprint (CF)
    Show tracked CF and other statistics
    Show ways to improve

    User clicks on improvement:
        Show more info/reveal description and estimated impact
    
    User changes quiz value:
        Update CF
        Update graph tracking the CF
```

Result of questionnaire -> Amount of carbon footprint/other data
                        -> Actionable ways to reduce carbon footprint (eg. stop using cars and use public transport)
                            - Based on AI or previous data set?


- Environmentally-friendly products advertising page
- Show improvements on carbon-footprint over time using a graph

