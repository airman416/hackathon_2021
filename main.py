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
                food waste                                          nFood
                recycled trash                                      nRecycle
'''

QUIZLIST = [
    "How many bedroom(s) and living room(s) do you have at home?",
    "How many hour(s) per day do you have the AC on?",
    "How many people are you living with"
    "How many hours per day is your computer on?"
    "How many large electronic appliances do you have? (Refregirators, Washing machines, etc.)"
    "How many times per year do you travel by an airplane?"
    "How many hours per week do you drive?"
    "How many hours per week do you use public transportation? (Trains, busses)"
    "How many windows are there in your home?"
    "At what temperature is your AC set at?"
]

MCQLIST = [
    ("What % of your food goes to waste?", ("0~5%", "6~10%", "11~30%", "More than 30%")),
    ("Which materials do you recycle?", ("Plastic", "Cans", "Paper", "Bottles", "Glass")),
]