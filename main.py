#####################################################################################################################################################
########################                                    HEADER                              #####################################################
#####################################################################################################################################################
#information
#iAQ Sensor Range:  co2: (450-2000) ppm,      tvoc: (125-600) ppb

print('setting parameters and importing libraries...')

########################################################### IMPORTS #################################################################################
from functions_and_modules import *
#me = SingleInstance() #from tendo - prevents multiple script instances
##########################################################   SETUP  #################################################################################
#setup is executed once at startup
#setting permissions (necessary for sending image)
print('setting permissions...')
os.system('sudo chmod -R 777 .')

#pin declaration:
#lamp and pump are connected to the double relais module
#fan1: humidity regulation, fan2: inhouse ventilation (air movement)

dht1_pin = 4
buzzer_pin = 22
iaq_address = 90

dht1 = Adafruit_DHT.DHT22
buzzer = io.TonalBuzzer(buzzer_pin)


#variable initialisation:
errorcounter = 0
temperature = 0
humidity = 0
tvoc = 0
co2 = 0
gas = 0
hours = 0
hours_old = 0
minutes = 0
minutes_old = 0
cycles = 0                 #cyclenumber for debugging
wateringcycles = 0
emergencystate = False
lampstate = False
humidity_list = []
temperature_list = []
timestamp_list = []
seconds_since_start_list = []
co2_list = []
tvoc_list = []

#parameter declaration:
main_delay = 1             #delay in seconds for main loop






start_time = round(set_starttime(), 1)

print('starting up...\n')



hours = gethours()
minutes = getminutes()
oldhours = hours
oldminutes = minutes
##########################################################   MAIN LOOP  #################################################################################

while(True):
    try:
        #get actual time:
        hours = gethours()
        minutes = getminutes()
        timestamp = gettimestamp()




        #Measurements every 2 cycles:
        if cycles%2==0:
            (humidity, temperature) = DHT_read(dht1, dht1_pin, bot, chat_id)
            humidity = round(humidity, 2)
            temperature = round(temperature, 2)
            (co2, tvoc) = i2c_iAq_read(iaq_address)

            


        #watering
        if(((hours==8 or hours==10 or hours==14 or hours==19) and hours!=oldhours and watering_active==True and emergencystate==False)):
            watering(pump, pumptime)
            wateringcycles = wateringcycles + 1

        #deleting first element of lists if length exceeds 50k
        if len(seconds_since_start_list)>50000:
            humidity_list = humidity_list[1:]
            temperature_list = temperature_list[1:]
            timestamp_list = timestamp_list[1:]
            seconds_since_start_list = seconds_since_start_list[1:]
            co2_list = co2_list[1:]
            tvoc_list = tvoc_list[1:]


        #logging data
        if (cycles%2==0):
            humidity_list.append(humidity)
            temperature_list.append(temperature)
            timestamp_list.append(timestamp)
            seconds_since_start_list.append(int(round(time_since_start(start_time), 0)))
            co2_list.append(co2)
            tvoc_list.append(tvoc)

            

        #printing out information
        print('Humidity: {}'.format(humidity) + ' %')
        print('Temperature: {}'.format(temperature) + ' deg')
        print('Co2: {}'.format(co2) + ' ppm')
        print('TVOC: {}'.format(tvoc) + ' ppb')
        print('Cycles: {}'.format(cycles))
        print('Seconds since program start: {}'.format(int(round(time_since_start(start_time), 0))))



        oldhours = hours
        oldminutes = minutes
        cycles = cycles + 1   
        sleep(main_delay)  #main delay
        
    except:
        print('some shit just got real.')
