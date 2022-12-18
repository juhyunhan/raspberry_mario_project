from display import Display
from PIL import Image, ImageDraw
import time
from coin import Coin
from character import Mario
from stage import Map
def main():
    display = Display()
  
           
    mario = Mario([15, 150])
    game_map = Map(stage = 1)
    while True:
                
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False, 'jump_pressed':False}

        # 명령어 받기
        if not display.button_L.value: #left pressed
            command['left_pressed'] = True
        if not display.button_R.value: #right pressed
            command['right_pressed'] = True
        if not display.button_A.value :
            command['jump_pressed'] = True
        
        # 명령에 따라 마리오 이동            

        game_map.process(command)
        
        render_image = game_map.rendering()
            

        # showing_image.paste(resizedcoin, (coin_location_x, coin_location_y),resizedcoin)
        
        # showing_image.paste(resizedcoin2, (coin_location_x2, coin_location_y2),resizedcoin2)

        display.disp.image(render_image)
        time.sleep(0.001)
        
    
        
if __name__ == "__main__":
    main()