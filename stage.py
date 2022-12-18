from coin import Coin
from pipe import Pipe
from character import Mario
from mushroom import Mushroom
from star import Star
from PIL import Image, ImageDraw, ImageFont
import numpy as np
class Map:
    def __init__(self, stage):
        self.map_view = Image.open('./image/background/back0.png').convert('RGBA').resize((240, 240))
        self.finish_map = Image.open('./image/background/last2.png').convert('RGBA').resize((240, 240))
        self.stage = stage
        self.mario = Mario([0, 0])
        self.coins = []
        self.pipes = []
        self.mushrooms = []
        self.stars = []
        self.change_stage(stage_number = stage)
        self.score = 0
        self.game_state = 'keeping'
        self.fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        
    def change_stage(self, stage_number):
        if stage_number == 1:
            self.set_stage1(self.stage)
        
        elif stage_number == 2:
            self.set_stage2(self.stage)
        
        elif stage_number == 3:
            self.set_stage3(self.stage)
        
        elif stage_number == 4:
            self.set_stage4(self.stage)
            
        elif stage_number == 5:
            self.set_stage5()
            
            
    def get_map_collision_area(self):
        collision_area = np.empty(240)
        collision_area.fill(210)#ground height
        for pipe in self.pipes:
            collision_area[pipe.collision_box[0]-15:pipe.collision_box[2]+15] = pipe.collision_box[1]
            
        return collision_area
    
    def process(self, command):
        map_info = self.get_map_collision_area()
        self.mario.move(map_info, command)
        if self.mario.state == 'die':
            self.game_state = 'done'
        
        for coin in self.coins:
            coin.collision_check(self.mario)
            if coin.state == 'hit':
                self.score += 10
                self.coins.remove(coin)
        
        for mushroom in self.mushrooms:
            mushroom.collision_check(self.mario)
            mushroom.move()
        
        for star in self.stars:
            star.collision_check(self.mario)
            if star.state == 'hit':
                self.mario.state = 'finish'
                self.game_state = 'finish'
                
        if self.stage == 1:
            if self.mario.position[0] > 170:
                self.change_stage(2)
                
        elif self.stage == 2:
            if self.mario.position[0] < 10:
                self.change_stage(1)
                
            elif self.mario.position[0] > 170:
                self.change_stage(3)
                
        elif self.stage == 3:
            if self.mario.position[0] < 10:
                self.change_stage(2)
            elif self.mario.position[0] > 170:
                self.change_stage(4)

        if self.mario.go_pipe_state == True:
            self.mario.go_pipe_state = False
            self.change_stage(5)
            
    def rendering(self):
        if self.stage == 5:
            background = self.finish_map.copy()
        else:
            background = self.map_view.copy()
            
        if self.game_state == 'done':
            background = Image.new("RGB", (240, 240))
            checking_draw = ImageDraw.Draw(background)
            checking_draw.rectangle((0, 0, 240, 240), fill='#000000')
            checking_draw.text((20, 100), 'Game Over!', font=self.fnt, fill='#FFFFFF')

            
        else:
            checking_draw = ImageDraw.Draw(background)

            #코인(Object) 관련 그림 그리기
            for coin in self.coins:
                background.paste(coin.appearance, (coin.position[0], coin.position[1]), coin.appearance)
            
            for mushroom in self.mushrooms:
                background.paste(mushroom.appearance, (mushroom.position[0], mushroom.position[1]), mushroom.appearance)
            
            for star in self.stars:
                background.paste(star.appearance, (star.position[0], star.position[1]), star.appearance)

            #릭터 관련 그림 그리기
            background.paste(self.mario.appearance, (self.mario.position[0], self.mario.position[1]), self.mario.appearance)
            
            for pipe in self.pipes:
                background.paste(pipe.appearance, (pipe.position[0], pipe.position[1]), pipe.appearance)

            
            
            checking_draw.text((190, 5), str(self.score), font=self.fnt, fill='#000000')

        return background
        
    def set_stage1(self, from_):
        if from_ == 2:
            self.mario.set_position([160, 150], self.stage)
        else:
            self.mario.set_position([15, 150], self.stage)
        self.coins = [Coin([90, 90]), Coin([120, 90]), Coin([150, 90])]
        self.mushrooms = []
        self.pipes = []
        self.stage = 1
        
        
    def set_stage2(self, from_):
        if from_ == 1:
            self.mario.set_position([15, 150], self.stage)
        else:
            self.mario.set_position([160, 150], self.stage)

        self.mushrooms = []
        self.coins = [Coin([100, 70])]
        self.pipes = [Pipe([80, 130])]
        self.stage = 2
        
        
    def set_stage3(self, from_):
        if from_ == 2:
            self.mario.set_position([15, 150], self.stage)
        else:
            self.mario.set_position([160, 150], self.stage)
        self.coins = [Coin([100, 70])]
        self.mushrooms = [Mushroom([100, 170])]
        self.pipes = [Pipe([40, 130]), Pipe([140, 130])]
        self.stage = 3

        
    def set_stage4(self, from_):
        if from_ == 3:
            self.mario.set_position([15, 150], self.stage)
        else:
            self.mario.set_position([160, 150], self.stage)

        self.pipes = [Pipe([130, 130])]
        self.coins = []
        self.mushrooms = [Mushroom([100, 170], moveable=True)]
        self.stage = 4

        
    def set_stage5(self):
        self.stage = 5
        self.pipes = []
        self.coins = []
        self.mushrooms = []
        self.stars = [Star([85, 150])]
        self.mario.set_position([15, 20], self.stage)
