import numpy as np
from PIL import Image
import math
class Mario:
    def __init__(self, position):
        self.stand_image = Image.open('./image/mario/standmario.png').convert('RGBA').resize((60, 60))
        self.walk1_image = Image.open('./image/mario/walk1.png').convert('RGBA').resize((60, 60))
        self.walk2_image = Image.open('./image/mario/walk2.png').convert('RGBA').resize((60, 60))
        self.jump_image = Image.open('./image/mario/jumping.png').convert('RGBA').resize((60, 60))
        self.victory_image = Image.open('./image/mario/victory.png').convert('RGBA').resize((120, 200))
        self.appearance = self.stand_image
        self.state = None
        self.position = np.array(position)
        self.collision_box = [self.position[0]+15, self.position[1], self.position[0]+45, self.position[1]+60]
        self.jump_count = 0
        self.jump_count2 = 0
        self.jump_state = 'release'
        self.walk_count = 0
        self.direction = 'right'
        self.life = 1
        self.die_ani_count = 30
        self.pipe_ani_count = 10
        self.go_pipe_state = False
        self.stage = 1
    def set_position(self, position, stage):
        self.stage = stage
        self.position = np.array(position)
        self.collision_box = [self.position[0]+15, self.position[1], self.position[0]+45, self.position[1]+60]
    
    def die_animation(self):
        if self.die_ani_count > 20: # 0 ~ 4 : 5 
            self.position[1] -= 15
            
        elif self.die_ani_count > 0:
            self.position[1] += 15
            
        self.die_ani_count -= 1
    
    def go_pipe(self):
        if self.pipe_ani_count > 0:
            self.position[1] += 2
            
        self.pipe_ani_count -= 1
        
    def move(self, map_info, command = None):
        if self.state == 'finish':
            self.appearance = self.victory_image
            return
            
        if self.life == 0:
            self.die_animation()
            if self.die_ani_count == 0:
                self.state = 'die'
                return
        
        if self.state == 'go_pipe':
            self.go_pipe()
            if self.pipe_ani_count == 0:
                self.go_pipe_state = True
                self.state = 'move'
                return
            
        elif self.state == 'jump':
            if command['left_pressed']:
                if max(map_info[self.collision_box[0]:self.collision_box[0]+5]) >= self.collision_box[3]:
                    self.position[0] -= 5
                    self.collision_box[0] -= 5
                    self.collision_box[2] -= 5
                self.appearance = self.jump_image.transpose(Image.FLIP_LEFT_RIGHT)
                
                    
            if command['right_pressed']:
                if max(map_info[self.collision_box[2]-5:self.collision_box[2]]) >= self.collision_box[3]:
                    self.position[0] += 5
                    self.collision_box[0] += 5
                    self.collision_box[2] += 5
                self.appearance = self.jump_image

            if self.jump_count2 < self.jump_count: # 0 ~ 4 : 5 
                self.position[1] -= 15
                self.collision_box[1] -= 15
                self.collision_box[3] -= 15
                self.jump_count2 += 1
    
            if self.jump_count2 == self.jump_count:
                self.state = 'move'
                self.jump_count = 0
                self.jump_count2 = 0
            
                
        else:
            if self.collision_box[3] < max(map_info[self.collision_box[0]:self.collision_box[2]]):
                self.position[1] += 15
                self.collision_box[1] += 15
                self.collision_box[3] += 15
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['down_pressed']:
                pipe = np.array(map_info[self.collision_box[0]:self.collision_box[2]])
                check = pipe < 210
                if check.sum() == len(pipe) and self.collision_box[3] < 170 and self.stage == 4:
                    print("DDDWOWDNDWODWNODWNWDO")
                    self.state = 'go_pipe'
                    

            
            if command['left_pressed']:
                self.direction = 'left'
                if max(map_info[self.collision_box[0]:self.collision_box[0]+5]) >= self.collision_box[3]:
                    self.position[0] -= 5
                    self.collision_box[0] -= 5
                    self.collision_box[2] -= 5
                    
                if self.walk_count == 0:
                    self.appearance = self.walk1_image.transpose(Image.FLIP_LEFT_RIGHT)
                    self.walk_count = 1

                elif self.walk_count == 1:
                    self.appearance = self.walk2_image.transpose(Image.FLIP_LEFT_RIGHT)
                    self.walk_count = 0
                
            if command['right_pressed']:
                self.direction = 'right'
                print(max(map_info[self.collision_box[2]-5:self.collision_box[2]]))
                print(self.collision_box[3])
                if max(map_info[self.collision_box[2]-5:self.collision_box[2]]) >= self.collision_box[3]:
                    self.position[0] += 5
                    self.collision_box[0] += 5
                    self.collision_box[2] += 5
                if self.walk_count == 0:
                    self.appearance = self.walk1_image
                    self.walk_count = 1
                elif self.walk_count == 1:
                    self.appearance = self.walk2_image
                    self.walk_count = 0
                    
            if command['jump_pressed']:
                if self.jump_count < 20:
                    print(self.jump_count)
                    self.jump_count += 1
                self.jump_state = 'hold'
            
            else:
                if self.jump_count > 2:
                    if self.jump_count % 2 == 1:
                        self.jump_count += 1
                    if self.jump_state == 'hold':
                        self.jump_state = 'release'
                        self.state = 'jump'
                        if self.direction == 'right':
                            self.appearance = self.jump_image
                            
                        elif self.direction == 'left':
                            self.appearance = self.jump_image.transpose(Image.FLIP_LEFT_RIGHT)
                    else:    
                        if not command['left_pressed'] and not command['right_pressed']:
                            if self.direction == 'right':
                                self.appearance = self.stand_image
                                
                            elif self.direction == 'left':
                                self.appearance = self.stand_image.transpose(Image.FLIP_LEFT_RIGHT)
                
                else:
                    self.jump_count = 0