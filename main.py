from display import Display
from PIL import Image, ImageDraw
import time

def main():
    display = Display()
    # image = Image.new("RGB", (display.width, display.height))
    # draw = ImageDraw.Draw(image)
    # draw.rectangle((0, 0, display.width, display.height), outline=0, fill=(255, 255, 255))
    #display.disp.image(image)
    
    my_image = Image.open('./image/background/back0.png').convert('RGBA')
    resized_image = my_image.resize((240, 240))
    copyed_image = resized_image.copy()
    
    standmario_image = Image.open('./image/mario/standmario.png').convert('RGBA')
    jumpmario_image = Image.open('./image/mario/jumpmario.png').convert('RGBA')
    resizedstand_character = standmario_image.resize((60, 60))
    resizedjump_character = jumpmario_image.resize((60, 60))
    mario_location_x = 90
    mario_location_y = 150
    resized_image.paste(resizedstand_character, (mario_location_x, mario_location_y), resizedstand_character)
    display.disp.image(resized_image)
    
    
    while True:
        draw_charcter = resizedstand_character
        mario_location_y = 150
        
        showing_image = copyed_image.copy()
        if not display.button_L.value: #left pressed
            mario_location_x = mario_location_x - 5
        if not display.button_R.value: #right pressed
            mario_location_x = mario_location_x + 5
        if not display.button_A.value :
            draw_charcter = resizedjump_character
            mario_location_y = mario_location_y - 35
        
        showing_image.paste(draw_charcter, (mario_location_x, mario_location_y), draw_charcter)
        display.disp.image(showing_image)
        time.sleep(0.01)
        
    
        
if __name__ == "__main__":
    main()