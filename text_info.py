
import pyglet

    
class Text_info(pyglet.text.Label):
    def __init__(self, text, x = 0, y = 0, batch = None, group=None ):                     
        super(Text_info, self).__init__(text = text, 
                                        font_name='Times New Roman',
                                        font_size=24, 
                                        x=x,
                                        y= y, 
                                        anchor_x='left', 
                                        anchor_y='baseline',
                                        batch = batch, 
                                        group=group)             
       
       #!!!! добавить свойства для изменения текста 
    def update(self, text_value_new=""):
        self.text = text_value_new
