import numpy as np
from PIL import Image
class Mushroom:
    def __init__(self, position):
        self.appearance = Image.open('./image/obstacles/mushroom.png').convert('RGBA').resize((60,60))
        self.value = 10
        self.position = np.array(position)
        self.outline = "#0000FF"
        self.state = 'none'
        self.collision_box = (position[0]+10, position[1]+5, position[0]+45, position[1]+45)

            
    def collision_check(self, mario):
        # collision = self.overlap(self.position, mario.collision_box)
        collision = self.overlap(mario.collision_box)
    
        if collision:
            print("the mushroom is hit")
            self.state = 'hit'
            mario.life = 0

    def overlap(self, other_position):
        '''
        경우의 수 따져서 추가 필요
        몇가지 밖에 경우의 수 아직 없음 ! 
        '''
        ego_x1, ego_y1, ego_x2, ego_y2 = self.collision_box
        other_x1, other_y1, other_x2, other_y2 = other_position
        
        maxrec_x = max(ego_x1,ego_x2)
        minrec_x = min(ego_x1,ego_x2)
        maxrec_y = max(ego_y1, ego_y2)
        minrec_y = min(ego_y1, ego_y2)
        if  (minrec_x < other_x1 < maxrec_x or minrec_x < other_x2 < maxrec_x) and (minrec_y < other_y1 < maxrec_y or minrec_y < other_y2 < maxrec_y):
            return True
        else:
            return False