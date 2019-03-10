import cocos.layer
import cocos.scene
import cocos.text
import cocos.sprite
import cocos.actions as ac
import pyglet.window.mouse as ms
import pygame.mixer
import time
from cocos.scenes.transitions import MoveInRTransition
from cocos.scenes.transitions import FadeBLTransition
from cocos.director import director
from pyglet.image import load, ImageGrid, Animation

import mainmenu
import assets.board.r_game as rg
from ending import ending_scene

def new_scene(r_num): # 1, 2, 3라운드 용 scene
    scene = cocos.scene.Scene()
    hud_layer=HUD(r_num)
    color_layer = RoundLayer(hud_layer, r_num)
    scene.add(color_layer, z=0)
    scene.add(hud_layer, z=1)
    director.run(MoveInRTransition(scene, duration=1.0))

def final_scene(): # 마지막 라운드 용 scene
    scene=cocos.scene.Scene()
    hud_layer=HUD(4)
    layer=RoundLayer(hud_layer, 4)
    bg=cocos.sprite.Sprite('assets/bg/final.PNG', position=(400, 300)) # Center에 위치하게 변경
    layer.add(bg)  # finalimage를 삽입
    scene.add(layer, z=0)
    scene.add(hud_layer, z=1)

    pygame.mixer.music.load('assets/sound/castle.wav') # castle 용 음악
    pygame.mixer.music.play(9)

    director.run(MoveInRTransition(scene, duration=1.0))
    while pygame.mixer.music.get_busy():
        time.sleep(1)


class HUD(cocos.layer.Layer):
    def __init__(self, r_num):
        super(HUD, self).__init__()
        w, h=director.get_window_size()
        self.round=r_num
        self.rtext = cocos.text.Label('', (15, h-30), font_size=18, color=(0,0,0,255), font_name='Mosk Medium 500') # round 알려줌
        if self.round==4: self.rtext.element.text="Final Round"
        else: self.rtext.element.text="Round: %d" % self.round
        self.add(self.rtext)

        self.hint=cocos.text.Label('', (15, h-55), font_size=16, color=(0,0,0,255), font_name='Mosk Medium 500')
        self.add(self.hint)
        self.update_hint()

        self.set_timelimit()
        self.tl_text= cocos.text.Label('', (90, h-80), font_size=15, color=(0,0,0,255)) # 잘못된 칸 누를 때 -5 띄움
        self.time_text=cocos.text.Label("%02d:%02d" % (self.timelimit//60, self.timelimit%60), (15, h-80), font_size=18, color=(0,0,0,255), font_name='Mosk Medium 500')
        self.add(self.time_text) # 현재 남은 시간을 알려주는 text
        self.add(self.tl_text)

        self.schedule(self.update)
        self.gameover=False
        self.set_numbers() # board 옆, 위에 숫자를 씀
        self.wrong=False
        self.time_delayed=0

    def update(self, dt): # frame마다 시간 체크해서 time_text 바꿔주기
        m = self.timelimit//60; s = self.timelimit % 60
        self.time_delayed+=dt
        if self.wrong==True:
            m = self.timelimit//60; s = self.timelimit%60
            self.time_text.element.text = "%02d:%02d" % (m, s)
            self.wrong = False

        if self.time_delayed>=1: # 1초 지날 때마다 -1씩
            self.timelimit-=1
            m = self.timelimit // 60; s = self.timelimit % 60
            self.time_text.element.text = "%02d:%02d" % (m, s)
            self.time_delayed=0 # time_delayed 초기화
            self.tl_text.element.text = '' # -5라고 띄우고 있는 tl_text 초기화

        if m*60+s<=0: # 시간초과되면 Gameover
            self.time_text.element.text = "00:00"
            self.unschedule(self.update)
            self.gameover=True
            pygame.mixer.music.stop()
            gameover=pygame.mixer.Sound('assets/sound/gameover.wav')
            gameover.play()
            self.Game_Over()

    def set_timelimit(self): # 각 라운드마다 지정해놓은 제한 시간이 다름
        if self.round==1: self.timelimit=60
        elif self.round==2: self.timelimit=300
        elif self.round==3: self.timelimit=360
        elif self.round==4: self.timelimit=540

    def update_timelimit(self, wrong): # 잘못된 칸을 선택할 때마다 -5초
        if wrong==True:
            self.tl_text.element.text = '-5'
            self.timelimit -= 5
            self.wrong == True # update 함수에 반영하기 위해서

    def update_hint(self): # 각 라운드마다 해당 그림에 대한 힌트 제공
        if self.round==1:
            self.hint.element.text="Hint: Love"
        elif self.round==2:
            self.hint.element.text="Hint: Winter is coming!"
        elif self.round==3:
            self.hint.element.text="Hint: Be careful of its claws."
        elif self.round==4:
            self.hint.element.text="Hint: You win! Get this prize."

    def set_numbers(self):
        if self.round==1:
            l_num=5; b_size=64                  # l_num은 nxn에서 n의 값, b_size는 block size
            r_f=225; r_s=400; c_f=290; c_s=463  # r_f는 1행의 row 숫자 리스트의 마지막 숫자의 x값, r_s는 y값
        elif self.round==2 or self.round==3:   # c_f는 1열의 col 숫자 리스트의 마지막 숫자의 x값, c_s는 y값
            l_num=10; b_size=36
            r_f=205; r_s=420; c_f=243; c_s=453
        elif self.round==4:
            l_num=20; b_size=23
            r_f = 278; r_s = 463; c_f = 309; c_s = 485

        row, col=rg.get_numlist(self.round) # numList를 받아와서 hudlayer에 순서대로 add
        for j in range(l_num):
            for i in range(len(row[j]), 0, -1):
                text = cocos.text.Label(str(row[j][len(row[j])-i]), (r_f-14*(i-1), r_s-b_size*j), font_size=12, color=(0, 0, 0, 255))
                self.add(text)
        for j in range(l_num):
            for i in range(len(col[j]), 0, -1):
                text = cocos.text.Label(str(col[j][len(col[j])-i]), (c_f+b_size*j, c_s+15*(i-1)), font_size=12, color=(0, 0, 0, 255))
                self.add(text)

    def Game_Over(self):
        text=cocos.text.Label("Game Over!", (170, 300), font_size=70, color=(0,0,0,255), font_name='Mosk Medium 500')
        self.add(text)

    def Round_clear(self):
        text=cocos.text.Label("Round Clear!", (170, 300), font_size=70, color=(0,0,0,255), font_name='Mosk Medium 500')
        self.add(text)

    def Game_Clear(self):
        self.unschedule(self.update)
        text = cocos.text.Label("Game Clear!", (170, 300), font_size=70, color=(0, 0, 0, 255), font_name='Mosk Medium 500')
        self.add(text)


class RoundLayer(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, hud, r_num):
        super(RoundLayer, self).__init__(200, 240, 255, 255)
        self.hud=hud
        self.round=r_num
        self.making_board()
        self.colored_num=0
        if self.round==4: # 마지막 라운드
            self.dragon = Dragon(160, 240)
            self.player = cocos.sprite.Sprite('assets/player/Suy_back.png', position=(160, 45))
            self.add(self.dragon, z=1)
            self.add(self.player, z=1)
            self.fire_num=0 # 지금까지 발사한 fireball의 갯수
            self.l_red, self.l_white = Dragon.set_blood(100, 285, self.fire_num) # dragon 남은 피 설정
            self.add(self.l_red, z=1)
            self.add(self.l_white, z=2)

    def making_board(self): # 각 round에 맞는 board 만들어서 layer에 추가하기
        w, h = director.get_window_size()
        if self.round==1:
            self.color_board=[0]*25 # 그 칸을 클릭했는가를 보여주는 board. 클릭했으면 1, 안 했으면 0
            self.board = Board(272, 428, 1)
            for pixel in self.board:
                    self.add(pixel, z=1)

        if self.round==2 or self.round==3:
            self.color_board = [0]*100
            if self.round==2: self.board=Board(238, 430, 2)
            elif self.round==3: self.board=Board(238, 430, 3)
            for pixel in self.board:
                    self.add(pixel, z=1)

        if self.round==4:
            self.color_board=[0]*400
            self.board = Board(310, 470, 4)
            for pixel in self.board:
                    self.add(pixel, z=1)
                

    def checking(self, num): # rg에 있는 get_ans가 1을 리턴하면 해당 칸이 색칠해야되는 칸이 맞으므로 True를 리턴
        if rg.get_ans(num, self.round)==1: return True
        else: return False

    def on_mouse_press(self, x, y, buttons, mod):
        if self.hud.gameover==True: pass # gameover 상태이면 마우스로 클릭해도 아무런 반응이 없게 함
        elif buttons==ms.LEFT: # 왼쪽 버튼 클릭 시
            num = 0
            for pixel in self.board: # board의 pixel에 일일이 접근
                box = pixel.box # pixel의 경계
                if box[0] <= x <= box[1] and box[2] <= y <= box[3]: # pixel을 클릭했다면
                    if self.checking(num)==False and self.color_board[num]==0: # 틀림
                        x_click = pygame.mixer.Sound('assets/sound/buzzer.wav')
                        x_click.play()
                        self.hud.update_timelimit(True) # 제한 시간 줄이기
                        self.color_board[num]=1 # 클릭함으로 바꿔줌
                        pixel=rx_Block(self.round, pixel.x, pixel.y)
                        self.add(pixel, z=1)

                    if self.checking(num) and self.color_board[num]==0: #
                        l_click = pygame.mixer.Sound('assets/sound/button.wav')
                        l_click.play()
                        pixel = colored_Block(self.round, pixel.x, pixel.y)
                        self.color_board[num]=1   # 해당 number에 색깔 칠함 -> 1로 표시
                        self.colored_num+=1
                        self.add(pixel, z=1)

                        if rg.check_clear(self.colored_num, self.round): # round 클리어했는가 확인
                            if self.round==4: # 마지막 라운드인 경우
                                self.shoot()
                                self.game_clear()
                            else: # 다른 라운드인 경우
                                pygame.mixer.music.pause() # 원래 bgm 잠시 멈춤
                                r_clear=pygame.mixer.Sound('assets/sound/success.wav')
                                r_clear.play() # 성공 음악 틀기
                                self.hud.Round_clear()
                                round_clear(self.round) # 기존의 scene으로 넘어가고, 무슨 라운드를 클리어한건지 넘겨주기

                        if self.round==4 and self.colored_num%15==0:  # 15칸 씩 칠할 때 마다 드래곤 피 줄이기
                            self.shoot() # fireball shoot
                num += 1

        elif buttons==ms.RIGHT: # 오른쪽 버튼 클릭 시 X 버튼으로 바꿔줌
            num = 0
            for pixel in self.board:
                box = pixel.box
                if box[0] <= x <= box[1] and box[2] <= y <= box[3]:
                    if self.color_board[num]==0:
                        r_click = pygame.mixer.Sound('assets/sound/button.wav')
                        r_click.play()
                        pixel = x_Block(self.round, pixel.x, pixel.y)
                        self.add(pixel, z=1)
                num += 1


    def shoot(self): # 정답 square를 15개 이상 클릭했을 때마다 fireball을 쏨. 마지막 라운드 정답 칸은 148칸이므로 총 10개를 쏜다.
        fire=pygame.mixer.Sound('assets/sound/fireball.wav')
        fire.play()
        self.fire_num+=1
        fireball=FireBall(160, 100)
        self.add(fireball)
        fireball.do(ac.Delay(0.5)+ac.MoveTo((160, 240), 1.3)+ac.FadeOut(0.1)+ac.CallFunc(lambda: self.control_blood())) # dragon한테 날아감, dragon 피 조절
        self.dragon.do(ac.Delay(1.8)+ac.CallFunc(lambda: self.dragon.hit())) # dragon이 fireball을 맞으면 hit 호출

    def control_blood(self): # dragon이 fireball을 한 대씩 맞을 때마다 체력의 1/10씩 줄어듦
        self.l_red.kill()
        self.l_white.kill() # kill을 하지않으면 기존의 선이 남아있어서 항상 kill을 하고 새로 만들어줌
        self.l_red, self.l_white= Dragon.set_blood(100, 285, self.fire_num)
        self.add(self.l_red, z=1)
        self.add(self.l_white, z=2) # 하얀 선(닳은 체력)이 위에 있어야 피 모양이 자연스러움
        if self.fire_num == 10: # 마지막 fireball이므로 dragon, 피 모두 없애줌
            self.dragon.kill()
            self.l_red.kill()
            self.l_white.kill()

    def game_clear(self): # game을 clear함. ending scene으로 넘어감
        self.player.do(ac.Delay(4)+ac.MoveTo((140, 480), 2)+
                       ac.Delay(0.5)+ac.CallFunc(lambda: director.run(FadeBLTransition(ending_scene(), duration=2))))


class Block(cocos.sprite.Sprite): # board를 구성하는 하나하나의 block
    Types={
        1: ('assets/board/64.png', 64),
        2: ('assets/board/36.png', 36),
        3: ('assets/board/36.png', 36),
        4: ('assets/board/24.png', 23)}
    # 각 라운드마다 block의 사이즈가 다르다.
    # 4번 blocksize를 원래 사이즈인 24가 아니라 23으로 한 이유는 다른 block들에 비해 한 픽셀이 차지하는 크기가 상대적으로 커져서, 각 블럭 사이의 선이 너무 두꺼워졌기 때문
    # 1픽셀을 줄이면 각 블럭의 선이 겹쳐져서 한 선으로 나타나게 됨, 깔끔해보임

    def sel_type(x, y, block_type):
        image, size=Block.Types[block_type]
        return Block(image, x, y, size)

    def __init__(self, img, x, y, blk_size):
        super(Block, self).__init__(img)
        self.x=x; self.y=y
        hsize=blk_size//2 # block의 반 size
        self.box=[x-hsize, x+hsize, y-hsize, y+hsize] # box의 범위 x1, x2, y1, y2 리스트

class colored_Block(cocos.sprite.Sprite): # 왼쪽 버튼으로 맞힌 블럭
    Types={
        1: ('assets/board/64_c.png'),
        2: ('assets/board/36_c.png'),
        3: ('assets/board/36_c.png'),
        4: ('assets/board/24_c.png')}

    def __init__(self, num, x, y):
        super(colored_Block, self).__init__(colored_Block.Types[num])
        self.x=x; self.y=y

class x_Block(cocos.sprite.Sprite): # 오른쪽 버튼으로 체크한 블럭
    Types={
        1: ('assets/board/64_x.png'),
        2: ('assets/board/36_x.png'),
        3: ('assets/board/36_x.png'),
        4: ('assets/board/24_x.png')}

    def __init__(self, num, x, y):
        super(x_Block, self).__init__(x_Block.Types[num])
        self.x=x; self.y=y

class rx_Block(cocos.sprite.Sprite): # 틀려서 체크된 블럭
    Types={
        1: ('assets/board/64_rx.png'),
        2: ('assets/board/36_rx.png'),
        3: ('assets/board/36_rx.png'),
        4: ('assets/board/24_rx.png')}

    def __init__(self, num, x, y):
        super(rx_Block, self).__init__(rx_Block.Types[num])
        self.x=x; self.y=y


class Board(object): # game board
    def __init__(self, x, y, round):
        if round==1:
            self.board=[[Block.sel_type(x+i*64, y-j*64, 1) for i in range(5)]for j in range(5)]
        elif round==2 or round==3:
            self.board = [[Block.sel_type(x+i*36, y-j*36, 2) for i in range(10)] for j in range(10)]
        elif round==4:
            self.board = [[Block.sel_type(x+i*23, y-j*23, 4) for i in range(20)] for j in range(20)]

    def __iter__(self):
        for line in self.board:
            for pixel in line:
                yield pixel


class Dragon(cocos.sprite.Sprite):
    img=Animation.from_image_sequence(ImageGrid(load('assets/dragon.png'), 1, 4), 0.5)
    def __init__(self, x, y):
        super(Dragon, self).__init__(Dragon.img)
        self.x=x; self.y=y

    def hit(self): # dragon이 fireball 맞을 때마다 Hit를 적용하여 잠시 빨간색으로 변했다가 돌아옴
        self.do(Hit())
        dg_roar=pygame.mixer.Sound('assets/sound/dragon_roar.aiff') # 울부짖는 소리
        dg_roar.play()

    def set_blood(x, y, n): # dragon blood set하는 함수, shoot 상태에 따라 변함
        l_red = cocos.draw.Line((x, y), (x+120-12*n, y), (255, 0, 0, 255), 10) # shoot의 개수에 따라 점점 줄여줌
        l_white = cocos.draw.Line((x+120-12*n, y), (x+120, y), (255, 255, 255, 255), 10) # shoot의 개수에 따라 점점 늘려줌
        return l_red, l_white


class Hit(ac.IntervalAction):
    def init(self, duration=0.5):
        self.duration = duration

    def update(self, t):
        self.target.color = (255, 255 * t, 255 * t)


class FireBall(cocos.sprite.Sprite):
    def __init__(self, x, y):
        super(FireBall, self).__init__('assets/player/fireball.png')
        self.x=x; self.y=y


def round_clear(r): # round clear할 때 불러옴
    if r==1: p_x=225; p_y=120 # r은 round, p_x, p_y는 player가 새로이 위치할 곳의 x좌표, y좌표
    elif r==2: p_x=335; p_y=280;
    elif r==3: p_x=223; p_y=440;
    director.run(FadeBLTransition(mainmenu.new_game(p_x, p_y, r), duration=3)) # 기존 scene으로 돌아감