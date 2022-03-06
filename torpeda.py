import pyglet
from pyglet import clock
from ship import Ship
from event import EventHook

class Torpeda(pyglet.sprite.Sprite):
    def __init__(self, img_file="images/torpeda.png", x = 512, y = 200, batch = None, group = None):
        img = pyglet.image.load(img_file)
        img.anchor_x = img.width // 2  #якорим рисунок по центру X 
        img.anchor_y = img.height // 2 #якорим рисунок по центру Y
        super(Torpeda, self).__init__(img, x = x, y = y, batch = batch, group = group)                
        self.on_create = EventHook()
        self.on_destroy = EventHook()

    def create(self):    
        self.on_create.fire()
        clock.schedule_interval(self.move_torpeda, 1 / 80)  #Запуск перемещения по таймеру


    def check_collision(self):
        collision_ship = self.collision()
        if collision_ship != None:
            print('Столкновение') #проверка коллизии 
            collision_ship.destroy()
            self.destroy()
            return True

    def move_torpeda(self, dt): #пересчет координаты торпеды. Запускается по таймеру      
        if self.check_collision(): 
            return # выход из метода

        if self.y < 500 :
            self.y += 3
            self.scale -= 0.004 #улетающий вдаль
        else:
            self.destroy()
        
    def destroy(self):
            clock.unschedule(self.move_torpeda) #Отмена таймера
            self.batch = None #Исключаем из пачки
            self.on_destroy.fire()
            self.delete() #суицид  


    def __del__(self):
        print('Torpeda destroyed') #проверка суицида


    def distancesq(self,target): # дистанция до корабля (без корня)
        return (self.x-target.x)**2 + (self.y-target.y)**2
    
    def collision(self): #проверка на коллизии (столкновение)
        for i in  Ship.items_ship:    
            if self.distancesq(i) < (self.width/2 + i.width/2)**2: 
                return i
     
