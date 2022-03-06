import pyglet
from pyglet import clock
from detonation import Detonation
from event import EventHook


class Ship(pyglet.sprite.Sprite):
    items_ship = [] # Список кораблей
    
    def __init__(self, img_file="images/ship.png", x = 0, y = 400, batch = None, group = None, len_way=0):
        self.len_way = len_way
        img = pyglet.image.load(img_file)
        img.anchor_x = img.width // 2 - 10      #якорим рисунок по центру X + смещение к хвосту
        img.anchor_y = img.height // 2          #якорим рисунок по центру Y
        super(Ship, self).__init__(img, x = x, y = y, batch = batch, group = group)        
        self.anchor_x = self.width // 2 #якорим рисунок по центру X
        self.anchor_y = self.height // 2 #якорим рисунок по центру Y
        clock.schedule_interval(self.move_ship, 1 / 80)  #Запуск перемещения по таймеру
        Ship.items_ship.append(self) # # Добавляем в список кораблей
        self.on_destroy = EventHook()
        self.on_create = EventHook()


    def move_ship(self, dt): #пересчет координаты корабля. Запускается по таймеру
        if self.x < self.len_way:
            self.x += 2
        else:
            self.x = 0
                
    def __del__(self):
        print('Ship destroyed') #проверка суицида
    
    def create(self):    
        self.on_create.fire()    

    def destroy(self):
        Detonation(x= self.x, y = self.y, batch= self.batch, group= self.group ) # Создаем объект с анимацией взрыва              
        clock.unschedule(self.move_ship) #Отмена таймера
        self.batch = None #Исключаем из пачки
        Ship.items_ship.remove(self) # Удаляем из списка кораблей
        self.on_destroy.fire() #запуск обработчика события     
        self.delete() #суицид        
