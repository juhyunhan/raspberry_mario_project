import numpy as np
from PIL import Image
class Coin:
    def __init__(self, position):
        self.appearance = Image.open('./image/obstacles/coin.png').convert('RGBA').resize((30,30))
        self.value = 10
        self.position = np.array(position)
        self.outline = "#0000FF"
        self.state = 'none'
        self.collision_box = (position[0]+4, position[1]+2, position[0]+26, position[1]+26)

            
    def collision_check(self, mario):
        # collision = self.overlap(self.position, mario.collision_box)
        collision = self.overlap(mario.collision_box)
    
        if collision:
            print("the coin is hit!")
            self.state = 'hit'

    def overlap(self, other_position):
        '''
        경우의 수 따져서 추가 필요
        몇가지 밖에 경우의 수 아직 없음 ! 
        '''
        ego_x1, ego_y1, ego_x2, ego_y2 = self.collision_box
        other_x1, other_y1, other_x2, other_y2 = other_position
        
        
        #동전이 마리오의 오른쪽 상단에 위치
        maxrec_x = max(ego_x1,ego_x2)
        minrec_x = min(ego_x1,ego_x2)
        maxrec_y = max(ego_y1, ego_y2)
        minrec_y = min(ego_y1, ego_y2)
        if  (minrec_x < other_x1 < maxrec_x or minrec_x < other_x2 < maxrec_x) and (minrec_y < other_y1 < maxrec_y or minrec_y < other_y2 < maxrec_y):
            return True
        else:
            return False