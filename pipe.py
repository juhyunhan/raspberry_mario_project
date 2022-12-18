import numpy as np
from PIL import Image
class Pipe:
    def __init__(self, position):
        self.appearance = Image.open('./image/obstacles/green.png').convert('RGBA').resize((80,100))
        self.value = 10
        self.position = np.array(position)
        self.outline = "#0000FF"
        self.state = 'none'
        self.collision_box = [position[0]+14, position[1]+20, position[0]+65, position[1]+90]
