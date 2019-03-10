from cocos.director import director
import pyglet.font
import pyglet.resource
import pyglet.window
from mainmenu import new_menu
import pygame.mixer
import time

if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load('assets/sound/duskwalkin.wav') # 기본 bgm
    pygame.mixer.music.play(50) # 51번 반복이면 무한 반복과 거의 비슷함. fadeout 시켜줄 때까지 계속 반복할 거임

    pyglet.resource.reindex()
    pyglet.font.add_file('assets/Mosk Ultra-Bold 900.ttf')
    pyglet.font.add_file('assets/Mosk Medium 500.ttf')

    director.init(width=800, height=600, caption='Logic Square')
    director.run(new_menu())

    while pygame.mixer.music.get_busy(): # 그냥 play를 하면 켜고 바로 stop 되므로 music이 실행되는 동안 time.sleep(1)을 호출
        time.sleep(1)