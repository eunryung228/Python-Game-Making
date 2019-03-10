import cocos.menu
import cocos.scene
import cocos.layer
import cocos.actions as ac
from cocos.director import director
from cocos.scenes.transitions import FadeTRTransition
import pyglet.app
import pygame
from gamelayer import new_game


class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Logic Square')
        self.font_title['font_name'] = 'Mosk Ultra-Bold 900'
        self.font_title['font_size'] = 64
        self.font_item['font_name'] = 'Mosk Ultra-Bold 900'
        self.font_item_selected['font_name'] = 'Mosk Ultra-Bold 900'

        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = list()
        items.append(cocos.menu.MenuItem('Start Game', lambda: self.on_new_game()))
        items.append(cocos.menu.MenuItem('How to play?', lambda: self.how_to_play())) # 도움말
        items.append(cocos.menu.MenuItem('Quit', lambda: self.end_game()))
        self.create_menu(items, ac.ScaleTo(1.15, duration=0.25), ac.ScaleTo(1.0, duration=0.25))

    def on_new_game(self): # 새로운 게임 시작
        director.run(FadeTRTransition(new_game(768, 120, 0), duration=2))

    def how_to_play(self): # 도움말 메뉴를 불러옴
        director.run(help_menu())

    def end_game(self):
        pygame.mixer.music.fadeout(500)
        pyglet.app.exit()
        # 그냥 pyglet.app.exit()를 실행할 시에는 pygame의 music이 멈추지 않아서 fadeout을 시켜준 뒤에 exit 함수를 실행함


class HelpMenu(cocos.menu.Menu):
    def __init__(self):
        super(HelpMenu, self).__init__('How to play?')
        self.font_title['font_name'] = 'Mosk Ultra-Bold 900'
        self.font_title['font_size'] = 50
        self.font_item['font_name'] = 'Mosk Ultra-Bold 900'
        self.font_item_selected['font_name'] = 'Mosk Ultra-Bold 900'

        items = list()
        items.append(cocos.menu.MenuItem('\n', "")) # Back To Menu를 맨 아래에 위치시키고 싶은데
        items.append(cocos.menu.MenuItem('\n', "")) # position 설정을 어떻게 해야할지 모르겠어서..
        items.append(cocos.menu.MenuItem('\n', "")) # 빈 menuitem을 공간마다 추가해줌
        items.append(cocos.menu.MenuItem('\n', "")) # 실행하는 함수는 따로 없음
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('\n', ""))
        items.append(cocos.menu.MenuItem('Back To Menu', lambda:self.back_to_menu())) # mainmenu로 돌아감
        self.create_menu(items, ac.ScaleTo(1.10, duration=0.25), ac.ScaleTo(1.0, duration=0.25))

    def back_to_menu(self):
        director.run(new_menu())


class HUD(cocos.layer.Layer): # menu 위에 올라갈 hud
    def __init__(self):
        super(HUD, self).__init__()
        self.add_text()

    def add_text(self):
        w,h=director.get_window_size()
        mosk='Mosk Medium 500'
        self.t1=cocos.text.Label('The number which is located on the top of the board means that', font_size=17, font_name=mosk)
        self.t1.position=(85, h-125)
        self.t2 = cocos.text.Label('the number of squares to be painted consecutively.', font_size=17, font_name=mosk)
        self.t2.position = (85, h - 155)
        self.t3=cocos.text.Label('When several numbers are together, at least one unpainted', font_size=17, font_name=mosk)
        self.t3.position = (85, h - 185)
        self.t4= cocos.text.Label('square must exist between the painted squares.', font_size=17, font_name=mosk)
        self.t4.position = (85, h - 215)
        self.t5= cocos.text.Label("⦁ If you think that you can't paint the square, you can mark 'X'", font_size=17, font_name=mosk)
        self.t5.position = (75, h - 260)
        self.t6= cocos.text.Label("  by clicking the right-mouse button on that square.", font_size=17, font_name=mosk)
        self.t6.position = (75, h - 290)
        self.t7=cocos.text.Label("⦁ If you want to paint the square, click the left-mouse button.", font_size=17, font_name=mosk)
        self.t7.position = (75, h - 320)
        self.t8=cocos.text.Label("⦁ When all squares to be painted are painted, one round is cleared.", font_size=17, font_name=mosk)
        self.t8.position = (75, h - 350)
        self.t9=cocos.text.Label("⦁ After you clear 3 rounds, you can go to the Logic's Castle.", font_size=17, font_name=mosk)
        self.t9.position = (75, h - 380)
        self.t10=cocos.text.Label("Kill a Logic's Castle's dragon, and be a hero!", font_size=21, font_name=mosk)
        self.t10.position = (115, h - 440)
        self.add(self.t1); self.add(self.t2); self.add(self.t3); self.add(self.t4); self.add(self.t5)
        self.add(self.t6); self.add(self.t7); self.add(self.t8); self.add(self.t9); self.add(self.t10)


def new_menu(): # main menu
    scene = cocos.scene.Scene()
    color_layer = cocos.layer.ColorLayer(0, 120, 120, 245)
    scene.add(MainMenu(), z=1)
    scene.add(color_layer, z=0)
    return scene

def help_menu(): # help menu
    scene=cocos.scene.Scene()
    color_layer = cocos.layer.ColorLayer(0, 120, 120, 245)
    scene.add(HelpMenu(), z=1)
    scene.add(color_layer, z=0)
    scene.add(HUD(), z=1)
    return scene