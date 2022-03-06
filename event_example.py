from event import EventHook

class Sun():
    def __init__(self):
        self.on_sunrise = EventHook()    
        self.on_sunset  = EventHook()    

    def sunrise(self):    
        print("День наступает")    
        self.on_sunrise.fire()    

    def sunset(self):    
        print("Ночь наступает")    
        self.on_sunset.fire()    

class Anthill():
    def anthill_open(self):    
        print("Муравейник открывается")

    def anthill_close(self):    
        print("Муравейник закрывается")

class Bat():
    def bat_sleep(self):    
        print("Летучие мыши спят")

    def bat_kill(self):    
        print("Летучие мыши убивают")


my_sun = Sun()
my_anthill = Anthill()
my_bat = Bat()

my_sun.on_sunrise += my_anthill.anthill_open
my_sun.on_sunrise += my_bat.bat_sleep

my_sun.on_sunset  += my_anthill.anthill_close
my_sun.on_sunset  += my_bat.bat_kill

#---------------------------------

# my_sun.sunrise()
my_sun.sunset()