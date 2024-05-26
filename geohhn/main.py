import subprocess
from moviepy.editor import *
from random import randrange
import random
import os
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HHN GeoGuessr")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

HHN29_HOUSE_LIST = ["Stranger Things 2019 ", "Nightingales: Blood Pit ", "Universal Monsters ", "Depths of Fear ", "Yeti: Terror of the Yukon ",
                    "Ghostbusters ", "Killer Klowns From Outer Space ", "Us ", "Graveyard Games ", "House of 1000 Corpses "]

HHN30_HOUSE_LIST = ["Puppet Theatre: Captive Audience ", "Beetlejuice ", "The Haunting of Hill House ", "Universal Monsters: The Bride of Frankenstein Lives ", "The Texas Chainsaw Massacre ",
                    "HHN Icons: Captured ", "Revenge of the Tooth Fairy ", "Welcome to SCarey: Horror in the Heartland ", "Case Files Unearthed: Legendary Truth ", "The Wicked Growth: Realm of the Pumpkin "]

HHN31_HOUSE_LIST = ["Universal Monsters: Legends Collide ", "Halloween ", "The Horrors of Blumhouse ", "The Weeknd: After Hours Nightmare ", "Spirits of the Coven ",
                    "Bugs: Eaten Alive ", "Fiesta de Chupacabras ", "Hellblock Horror ", "Dead Man's Pier: Winter's Wake ", "Descendants of Destruction "]

HHN32_HOUSE_LIST = ["Chucky: Ultimate Kill Count ", "The Last of Us ", "Stranger Things 4 ", "Blood Moon: Dark Offerings ", "The Exorcist: Believer ",
                    "Universal Monsters: Unmasked ", "Dr. Oddfellow's Twisted Origins ", "Dueling Dragons: Choose Thy Fate ", "YETI: Campground Kills ", "The Darkest Deal "]

HOUSE_MASTER_LIST = [HHN29_HOUSE_LIST, HHN30_HOUSE_LIST, HHN31_HOUSE_LIST, HHN32_HOUSE_LIST]

GAME_STATE = "main"

FONT_TITLE = pygame.font.Font('freesansbold.ttf', 84)
FONT_BUTTON = pygame.font.Font('freesansbold.ttf', 32)

YEAR = 29

class House:

    def __init__(self, url, name, house_length):

        self.url = url
        self.name = name
        self.house_length = house_length

def create_screen_shots():

    video_name = 'output.mp4'
 
    clip = VideoFileClip(video_name)

    for frame in range(5):
        clip.save_frame(f"output{frame}.jpg", frame)

    clip.close()


def load_video(house_object):
    try:
        url = house_object.url

        frame = randrange(15, house_object.house_length) - 5

        subprocess.call('yt-dlp -f best --download-sections "*%s-%s" --force-keyframes-at-cuts %s -o "%s"' % (frame, frame+5, url, 'output.mp4'))

        if (os.path.exists('output.mp4')):
            create_screen_shots()
        else:
            print("ERROR CREATING VIDEO EXITING")

    except(AttributeError, TypeError):

        raise AssertionError("Input must be house 'object'")
    
def delete_house_picture_and_video():
    if (os.path.exists('output.mp4')):
        os.remove('output.mp4')

    for index in range(5):
        file_name = 'output' + str(index) + '.jpg'
        if (os.path.exists(file_name)):
            os.remove(file_name)
    
def create_house_object_list():

    rtr_list = []

    file = open(os.path.join('Assets', 'house_list.txt'), "r")

    temp_list = file.read().split(',')

    for house in temp_list:
        name_grab = house.split('u=')
        name = name_grab[0][3:]

        url_grab = name_grab[1].split('t=')
        url = url_grab[0]

        time = url_grab[1]

        rtr_list.append(House(url, name, int(time)))

    return rtr_list

def draw_main_menu(gray_target):

    WIN.fill(BLACK)

    text_title = FONT_TITLE.render("HHN GeoGuessr", True, WHITE)
    text_rect = (480, 50)

    WIN.blit(text_title, text_rect)

    for scalor in range(3):
        x = 600
        y = 200*(scalor + 1) + 25*scalor

        if (scalor+1 == gray_target):
            colour = GRAY
        else:
            colour = WHITE

        pygame.draw.rect(WIN, colour, pygame.Rect(x, y, 400, 100))

    text_play = FONT_TITLE.render("Play", True, BLACK)
    text_play_rect = (710, 205)

    text_help = FONT_TITLE.render("Help", True, BLACK)
    text_help_rect = (710, 430)

    text_exit = FONT_TITLE.render("Exit", True, BLACK)
    text_exit_rect = (710, 660)

    WIN.blit(text_play, text_play_rect)
    WIN.blit(text_help, text_help_rect)
    WIN.blit(text_exit, text_exit_rect)

    pygame.display.update()

def draw_play_menu(state, index):

    image = ""
    image_scale = (1600, 900)

    if (state == "display"):
        image = pygame.transform.scale(pygame.image.load(f"output{str(index)}.jpg"), image_scale)
        WIN.blit(image, (0, 0))

        pygame.draw.rect(WIN, WHITE, pygame.Rect(100, 750, 300, 100))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(650, 750, 300, 100))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(1200, 750, 300, 100))

        text_next = FONT_TITLE.render("Next", True, BLACK)
        text_next_rect = (1255, 760)

        text_prev = FONT_TITLE.render("Prev", True, BLACK)
        text_prev_rect = (155, 760)

        text_guess = FONT_TITLE.render("Guess", True, BLACK)
        text_guess_rect = (668, 760)

        WIN.blit(text_next, text_next_rect)
        WIN.blit(text_prev, text_prev_rect)
        WIN.blit(text_guess, text_guess_rect)
        
        pygame.display.update()
    else:
        index = draw_guess_menu(index)

    return state, index

def draw_guess_menu(index):

    WIN.fill(BLACK)

    pygame.draw.rect(WIN, WHITE, pygame.Rect(100, 750, 300, 100))

    text_back = FONT_TITLE.render("Back", True, BLACK)
    text_back_rect = (155, 760)

    WIN.blit(text_back, text_back_rect)

    if (index == 0):

        for scalor in range(4):
            x = 125 + 350*scalor
            y = 100
            pygame.draw.rect(WIN, WHITE, pygame.Rect(x, y, 300, 100))

            text_hhn = FONT_TITLE.render(f"HHN{str(29+scalor)}", True, BLACK)
            text_hhn_rect = (130 + 350*scalor, 110)

            WIN.blit(text_hhn, text_hhn_rect)
    else:

        scaled_img = (225, 150)

        image = ""

        for scalor in range(10):
            image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', f"hhn{YEAR}{scalor+1}.png")), scaled_img)

            if (scalor <= 4):
                x = 30 + 325*scalor
                y = 100
            else:
                x = 30 + 325*(scalor - 5)
                y = 400
                
            WIN.blit(image, (x, y))


    pygame.display.update()

    return index

def draw_guessed_menu(house_guess, real_house):

    WIN.fill(BLACK)

    if (house_guess == real_house):
        text_title = FONT_TITLE.render("YOU WON!!", True, WHITE)
        text_rect = (520, 50)
    else:
        text_title = FONT_TITLE.render("YOU LOST!", True, WHITE)
        text_rect = (520, 50)

    pygame.draw.rect(WIN, WHITE, pygame.Rect(100, 750, 300, 100))
    pygame.draw.rect(WIN, WHITE, pygame.Rect(1200, 750, 300, 100))

    text_playagain = FONT_BUTTON.render("Play Again", True, BLACK)
    text_playagain_rect = (1255, 785)

    text_menu = FONT_BUTTON.render("Main Menu", True, BLACK)
    text_menu_rect = (155, 785)

    WIN.blit(text_playagain, text_playagain_rect)
    WIN.blit(text_menu, text_menu_rect)
    WIN.blit(text_title, text_rect)

    temp_count = 0

    for year in HOUSE_MASTER_LIST:
        if real_house in year:
            break
        temp_count += 1

    target_index_house = HOUSE_MASTER_LIST[(29+temp_count)-29].index(real_house)

    image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', f"hhn{29+temp_count}{target_index_house+1}.png")), (500, 300))

    WIN.blit(image, (520, 300))

    
    pygame.display.update()

def draw_loading():
    WIN.fill(BLACK)

    text_title = FONT_TITLE.render("LOADING!!", True, WHITE)
    text_rect = (520, 50)

    WIN.blit(text_title, text_rect)

    pygame.display.update()

def create_new_target_house(house_list):
    draw_loading()
    house = random.choice(house_list)
    target_name = house.name
    load_video(house)

    return target_name
    
def main():

    global GAME_STATE, YEAR

    house_list_major = create_house_object_list()

    game = True

    target_name = create_new_target_house(house_list_major)

    sub_state = "display"
    index_val = 0

    guessed_house = "no"

    while game:

        mouse_menu_num = -1

        mouse = pygame.mouse.get_pos()

        mouse_x = mouse[0]
        mouse_y = mouse[1]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if (GAME_STATE == "main" and 600 <= mouse_x <= 1000):

                    if (200 <= mouse_y <= 300):
                        GAME_STATE = "play"
                    elif (425 <= mouse_y <= 525):
                        print("help")
                    elif (650 <= mouse_y <= 750):
                        game = False
                elif (GAME_STATE == "guessed"):
                    if (750 <= mouse_y <= 850):
                        if (100 <= mouse_x <= 400):
                            target_name = create_new_target_house(house_list_major)
                            GAME_STATE = "main"
                        elif (1200 <= mouse_x <= 1500):
                            target_name = create_new_target_house(house_list_major)
                            GAME_STATE = "play"
                elif(sub_state == "display" and 750 <= mouse_y <= 850):

                    if (100 <= mouse_x <= 400):
                        if (index_val - 1 == -1):
                            index_val = 4
                        else:
                            index_val = index_val - 1
                    elif (1200 <= mouse_x <= 1500):
                        if (index_val + 1 == 5):
                            index_val = 0
                        else:
                            index_val = index_val + 1
                    elif (650 <= mouse_x <= 950):
                        index_val = 0
                        sub_state = "guess_menu"
                elif(sub_state == "guess_menu"):

                    if (index_val == 0):
                        if (100 <= mouse_x <= 400 and 750 <= mouse_y <= 850):
                            sub_state = "display"
                        elif (100 <= mouse_y <= 200):
                            if (125 <= mouse_x <= 425):
                                YEAR = 29
                                index_val = 1
                            elif (475 <= mouse_x <= 775):
                                YEAR = 30
                                index_val = 1
                            elif (825 <= mouse_x <= 1125):
                                YEAR = 31
                                index_val = 1
                            elif (1175 <= mouse_x <= 1475):
                                YEAR = 32
                                index_val = 1
                    elif (index_val == 1 and 100 <= mouse_x <= 400 and 750 <= mouse_y <= 850):
                        index_val = 0
                    elif (index_val == 1 and GAME_STATE != "guessed"):
                        house_year_list = HOUSE_MASTER_LIST[YEAR-29]

                        if (100 <= mouse_y <= 250):
                            if (30 <= mouse_x <= 255):
                                guessed_house = house_year_list[0]
                            elif (355 <= mouse_x <= 580):
                                guessed_house = house_year_list[1]
                            elif (680 <= mouse_x <= 905):
                                guessed_house = house_year_list[2]
                            elif (1005 <= mouse_x <= 1230):
                                guessed_house = house_year_list[3]
                            elif (1330 <= mouse_x <= 1555):
                                guessed_house = house_year_list[4]
                        elif (400 <= mouse_y <= 550):
                            if (30 <= mouse_x <= 255):
                                guessed_house = house_year_list[5]
                            elif (355 <= mouse_x <= 580):
                                guessed_house = house_year_list[6]
                            elif (680 <= mouse_x <= 905):
                                guessed_house = house_year_list[7]
                            elif (1005 <= mouse_x <= 1230):
                                guessed_house = house_year_list[8]
                            elif (1330 <= mouse_x <= 1555):
                                guessed_house = house_year_list[9]

                        if (guessed_house != "no"):
                            GAME_STATE = "guessed"
                            delete_house_picture_and_video()
                            index_val = 0
                            sub_state = "display"
                            guessed_house == "no"

                        


        if (600 <= mouse_x <= 1000):

            if (200 <= mouse_y <= 300):
                mouse_menu_num = 1
            elif (425 <= mouse_y <= 525):
                mouse_menu_num = 2
            elif (650 <= mouse_y <= 750):
                mouse_menu_num = 3

        if(GAME_STATE == "main"):
            draw_main_menu(mouse_menu_num)
        elif(GAME_STATE == "play"):
            sub_state, index_val = draw_play_menu(sub_state, index_val)
        elif(GAME_STATE == "guessed"):
            draw_guessed_menu(guessed_house, target_name)


    # pumpkin = random.choice(house_list_major)

    # load_video(pumpkin)

    # print(pumpkin.name)

    pygame.quit()

    delete_house_picture_and_video()


if __name__ == "__main__":
    main()