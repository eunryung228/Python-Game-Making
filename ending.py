import cocos.layer
import cocos.scene
import cocos.text
import pygame
import pyglet.app
import cocos.actions as ac

from cocos.director import director

def ending_scene(): # game을 clear하면 불러오는 ending scene
    pygame.mixer.music.fadeout(1000) # 기존의 음악을 fadeout
    pygame.mixer.music.load('assets/sound/successful.wav') # ending bgm
    pygame.mixer.music.play()
    scene = cocos.scene.Scene()
    color_layer = EndingLayer()
    scene.add(color_layer, z=0)
    scene.add(EndingMenu(), z=1)
    return scene


class EndingMenu(cocos.menu.Menu): # ending menu
    def __init__(self):
        super(EndingMenu, self).__init__('Logic Square')
        self.font_title['font_name'] = 'Mosk Ultra-Bold 900'
        self.font_title['font_size'] = 64
        self.font_item['font_name'] = 'Mosk Ultra-Bold 900'
        self.font_item_selected['font_name'] = 'Mosk Ultra-Bold 900'

        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = list()
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('Quit', lambda: self.end_game()))
        self.create_menu(items, ac.ScaleTo(1.15, duration=0.25), ac.ScaleTo(1.0, duration=0.25))

    def end_game(self):
        pygame.mixer.music.fadeout(500)
        pyglet.app.exit()
        # 그냥 exit 하면 음악이 멈추지 않으므로 fadeout 시킨 후 exit 호출


class EndingLayer(cocos.layer.ColorLayer):
    def __init__(self):
        super(EndingLayer, self).__init__(0, 120, 120, 245)
        self.add_text()

    def add_text(self):
        w, h = director.get_window_size()
        mosk = 'Mosk Medium 500'
        white=(255, 255, 255, 255)
        self.t1 = cocos.text.Label('Game Clear!', font_size=50, font_name='Mosk Ultra-Bold 900', color=white)
        self.t1.position = (220, h//2)
        self.t2 = cocos.text.Label('Thank you for playing this game.', font_size=20, font_name=mosk)
        self.t2.position = (220, h//2-50)
        self.t3 = cocos.text.Label('made by ryaner', font_size=15, font_name=mosk) # ryaner -> nickname
        self.t3.position = (655, 10)
        self.add(self.t1); self.add(self.t2); self.add(self.t3)