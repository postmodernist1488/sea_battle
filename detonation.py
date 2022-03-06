import pyglet

class Detonation(pyglet.sprite.Sprite): 
    def __init__(self,  x = 0, y = 0,  batch = None, group = None):                        
        image_detonation_frames = ('images/ship_crack_00.png', 'images/ship_crack_01.png', \
            'images/ship_crack_02.png','images/ship_crack_03.png', 'images/ship_crack_04.png',\
            'images/ship_crack_05.png')
        
        #images_detonation = map(lambda img: pyglet.image.load(img), image_detonation_frames)    
        
        """ Заменил map + lambda на список для обработки img """
        images_detonation = []
        for i in image_detonation_frames:
            img = pyglet.image.load(i)
            img.anchor_x = img.width // 2 - 10  # якорим рисунок по центру X + смещение к хвосту
            img.anchor_y = img.height // 2      # якорим рисунок по центру Y
            images_detonation.append(img)
        
        animation_detonation = pyglet.image.Animation.from_image_sequence(images_detonation, 0.2, False)
        super(Detonation, self).__init__(animation_detonation,  x = x, y = y, batch = batch, group= group)        
        self.frame_index = 1           
    
    def destroy(self):                    
        self.batch = None #Исключаем из пачки        
        self.delete() #суицид     

    def on_animation_end(self): # специальное событие класса sprite - срабатывает на окончание анимации         
        self.destroy()

    def __del__(self):
        print('Detonation destroyed') #проверка суицида