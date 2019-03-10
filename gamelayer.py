import cocos.layer
import cocos.scene
import cocos.text
import cocos.tiles
import cocos.sprite
import cocos.actions as ac
import pygame
from cocos.director import director
from gameround import new_scene
from gameround import final_scene

def callMusic(): # bgm 다시 재생
    pygame.mixer.music.unpause()

def opendoor(): # 성문 열 때 재생
    pygame.mixer.music.fadeout(1000)
    opendoor = pygame.mixer.Sound('assets/sound/castledoor.wav')
    opendoor.play()

Types = {
    1: ('assets/num/num1.png'),
    2: ('assets/num/num2.png'),
    3: ('assets/num/num3.png') }

class GameLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, x, y, r):
        super(GameLayer, self).__init__()
        w, h=director.get_window_size()
        bg=cocos.sprite.Sprite('assets/bg/backimage.png')
        bg.set_position(w//2, h//2) # Center에 위치하게 조정
        self.add(bg) # background image를 삽입, image에서 sprite를 move하니까 이미지가 조금 깨짐.
        self.change_clr(r) # round clear 변경
        self.create_player(x, y)
        self.create_round()

    def change_clr(self, num): # round clear 변경
        self.cleared = [0, 0, 0]
        for i in range(num):
            self.cleared[i]=1

    def on_mouse_press(self, x, y, buttons, mod):
        if 248<=x<=312:
            if 88<=y<=152 and self.cleared[0]==0: # 아무 단계도 클리어 안 한 경우에만 가능
                self.go_to_round(1)
            if 248<=y<=312 and self.cleared[0]==1 and self.cleared[1]==0: # 1단계 클리어 한 경우에만 가능
                self.go_to_round(2)
            if 408<=y<=472 and self.cleared[0]==1 and self.cleared[1]==1 and self.cleared[2]==0: # 1, 2단계 클리어 한 경우에만 가능
                self.go_to_round(3)

    def create_player(self, x, y):
        self.player=Player(x, y)
        self.add(self.player)
        if self.cleared[0]==1: # 1단계 깨면 hat 얻음
            hat = cocos.sprite.Sprite('assets/player/hat.png')
            self.player.add(hat) # hat 삽입
            if self.cleared[2]!=1: # hat 말풍선 삽입
                hb = cocos.sprite.Sprite('assets/player/hat_bubble.png')
                self.player.add(hb)
                hb.do(ac.Delay(3.5) + ac.CallFunc(lambda: callMusic()) + ac.FadeOut(0.5))
        if self.cleared[1]==1: # 2단계 깨면 staff 얻음
            staff=cocos.sprite.Sprite('assets/player/staff.png')
            self.player.add(staff) # staff 삽입
            if(self.cleared[2] != 1): # staff 말풍선 삽입
                sb = cocos.sprite.Sprite('assets/player/staff_bubble.png')
                self.player.add(sb)
                sb.do(ac.Delay(3.5)+ ac.CallFunc(lambda: callMusic()) + ac.FadeOut(0.5))
        if self.cleared[2]==1: # 3단계 깨면 key 얻음
            key=cocos.sprite.Sprite('assets/player/key.png', position=(223, 450))
            self.add(key, z=1) # key 삽입
            key.do(ac.Delay(3)+ ac.CallFunc(lambda: callMusic())+ac.MoveTo((223, 420), 1.5) + ac.Delay(0.5) + ac.FadeOut(1))
            kb = cocos.sprite.Sprite('assets/player/key_bubble.png')
            self.player.add(kb) # key 말풍선 삽입
            kb.do(ac.Hide()+ac.Delay(6.0)+ac.Show()+ac.FadeIn(1.0)+ac.Delay(0.8)+ac.FadeOut(1.0)) # key가 player에게로 옴
            self.player.do(ac.Delay(9.0)+ac.MoveTo((160, 440), 0.5)+ac.MoveTo((164, 480), 0.5) +
                           ac.CallFunc(lambda: opendoor())+ac.Delay(2)+ac.CallFunc(lambda:final_scene()))
            # key를 얻고 castle로 다가가고 난 뒤, castle용 음악과 함께 final round를 띄움

    def create_round(self): # round 만들어주기
        self.r1=Round(Types[1], 280, 120)
        self.r2 = Round(Types[2], 280, 280)
        self.r3 = Round(Types[3], 280, 440)
        self.add(self.r1); self.add(self.r2); self.add(self.r3)

    def go_to_round(self, r_num): # round 블럭으로 이동하고 game round로 이동
        if r_num==1:
            self.player.do(ac.MoveTo((320, 120), 1.5)+ac.CallFunc(lambda: new_scene(r_num)))
        if r_num==2:
            self.player.do(ac.MoveTo((123, 120), 0.5)+ac.MoveTo((123, 280), 0.7)+ac.MoveTo((240, 280), 0.5)+ac.CallFunc(lambda: new_scene(r_num)))
        if r_num==3:
            self.player.do(ac.MoveTo((720, 280), 1.5)+ac.MoveTo((720, 440), 0.7)+ac.MoveTo((320, 440), 1.5)+ac.CallFunc(lambda: new_scene(r_num)))


class Player(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__('assets/player/Suy.png')
        self.x=x; self.y=y

class Round(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Round, self).__init__(image)
        self.x=x; self.y=y

'''
class BackgroundLayer():
    def __init__(self):
        bg = cocos.tiles.load('assets/bg/logic_square.tmx')
        self.layer1=bg['road']
        self.layer2=bg['castle']
        self.layer1.set_view(0, 0, self.layer1.px_width, self.layer1.px_height)
        self.layer2.set_view(0, 0, self.layer2.px_width, self.layer2.px_height)
''' # BackgroundLayer를 GameLayer에서
    # 아예 Background Image로 대체하면서 주석 처리함
    # 실행하는 데 무려 1분 40초가 걸림, 타일맵이 무거운 건가?

def new_game(x, y, r):
    game_layer=GameLayer(x, y, r)
    #game_layer=cocos.layer.Layer()
    #game_layer.add(bg_layer.layer1) 원래 tile로 하려고 했는데 너무 느려서 주석 처리함
    #game_layer.add(bg_layer.layer2)
    return cocos.scene.Scene(game_layer)