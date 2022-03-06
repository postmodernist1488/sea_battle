# Пример с клавишами и перемещением рисунка
from pydoc import doc
import random
import pyglet
from time import time
from pyglet.window import key, Window
from pyglet import clock
from text_info import Text_info
from ship import Ship
from torpeda import Torpeda

game_window = Window(1024, 768, "Морской бой") #создаем главное окно
batch = pyglet.graphics.Batch() ##  создаем пачку, куда добавим объекты для прорисовки

layer_01 = pyglet.graphics.OrderedGroup(0) # задний слой
layer_02 = pyglet.graphics.OrderedGroup(1)
layer_03 = pyglet.graphics.OrderedGroup(2)
layer_04 = pyglet.graphics.OrderedGroup(3)

periscope = pyglet.sprite.Sprite (pyglet.image.load("images/periscope_no_sight.png"), batch=batch, group=layer_03)

img_sight = pyglet.image.load("images/periscope_sight3.png") 
img_sight.anchor_x = img_sight.width // 2
img_sight.anchor_y = 469
sight = pyglet.sprite.Sprite(img_sight, x = 512, y = 469, batch = batch, group = layer_03)

background = pyglet.sprite.Sprite(pyglet.image.load("images/background.png"), batch=batch, group=layer_01)
x_coordinate = game_window.width // 2   

class Game_counter(): # класс для счетчика. Счетчик содержит число и отражает его в панели
    def __init__(self, x=0, y=0):
        self._count = 0
        self._info = Text_info(text ="0", x= x, y= y, batch=batch, group=layer_04)

    @property
    def count(self):
        return self._count
    @count.setter
    def count(self, value): # Запись значения в счетчик с отображением значения на экране
        self._count = value
        self._info.text = str(self._count)

    def count_plus(self):
        self.count += 1

    def __del__(self):
        self._info.delete()

class Main_game:
    def __init__(self):
        self.torpeda_create = None
        self.torpeda_del    = None
        self.ship_create    = None        
        self.ship_del       = None

        Text_info(text ="Торпеды",    x= 300, y = 100, batch=batch, group=layer_04)        
        Text_info(text ="Корабли",    x= 300, y =  50, batch=batch, group=layer_04)        
        Text_info(text ="Всего",      x= 450, y = 150, batch=batch, group=layer_04)   
        Text_info(text ="Выпущено",   x= 600, y = 150, batch=batch, group=layer_04)   
        Text_info(text ="Уничтожено", x= 800, y = 150, batch=batch, group=layer_04)
        self.res_ti = Text_info(text ="Бой", x= 10, y = 100, batch=batch, group=layer_04)
        self.new_game()

    def __del__(self):
        print('Game destroyed') #проверка суицида

    def new_game(self):
        if not (self.res_ti.text == "ПОРАЖЕНИЕ" or self.res_ti.text == "ПОБЕДА"):
            self.destroy_game()
        self.res_ti.text = "Бой"
        clock.schedule_interval(self.create_ship, 3)  #Запуск создания корабля каждые 3 секунды
        self.torpeda_all = Game_counter(x= 450, y=  100)
        self.torpeda_all.count = 10

        self.ship_all = Game_counter(x= 450, y=  50)
        self.ship_all.count = 10

        self.torpeda_create = Game_counter(x= 600, y= 100)       
        self.torpeda_del    = Game_counter(x= 800, y= 100)
        self.ship_create    = Game_counter(x= 600, y=  50)        
        self.ship_del       = Game_counter(x= 800, y=  50)
      
    def create_ship(self, dt):
            if self.ship_create.count < self.ship_all.count:
                new_ship = Ship(x= 0, y=random.randrange(300, 520, 40 ), batch = batch, group = layer_02, len_way= game_window.width) 
                new_ship.on_destroy += self.ship_del.count_plus       
                new_ship.on_create  += self.ship_create.count_plus
                new_ship.create()

    def create_torpeda(self):
            if self.torpeda_create.count < self.torpeda_all.count:
                new_torpeda = Torpeda(x = x_coordinate, batch = batch, group = layer_02)  
                new_torpeda.on_create += self.torpeda_create.count_plus
                new_torpeda.on_destroy += self.torpeda_del.count_plus
                new_torpeda.on_destroy += self.game_result
                new_torpeda.create()       

    def destroy_game(self):
        clock.unschedule(self.create_ship) 
        del self.torpeda_create
        del self.torpeda_del
        del self.ship_create
        del self.ship_del
        for i in reversed(Ship.items_ship):
            i.destroy()

    def game_result(self):
        if self.torpeda_del.count >= self.torpeda_all.count:
            if self.ship_del.count == self.ship_all.count:
                self.res_ti.text = "ПОБЕДА"
            else:
                self.res_ti.text ="ПОРАЖЕНИЕ"
            self.destroy_game()
                
      
# -----------------------------------------------------------
@game_window.event
def on_key_press(symbol, modifiers): 
    global x_coordinate
    if symbol == key.LCTRL:  #Левый Ctrl - пуск торпеды
        main_game.create_torpeda()     
    if symbol == key.R:
        main_game.new_game()
    if symbol == key.LEFT and x_coordinate > 50:
        sight.x -= 50
        x_coordinate -= 50
    if symbol == key.RIGHT and x_coordinate < game_window.width - 50:
        sight.x += 50
        x_coordinate += 50


@game_window.event 
def on_draw(): #перерисовывает экран по каждому событию    
    game_window.clear()    
    batch.draw() 

main_game = Main_game()

pyglet.app.run()
