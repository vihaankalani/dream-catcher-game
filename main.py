import cv2
import pygame
import mediapipe as mp
import random
#init pygame
pygame.init()
#setup display
WIDTH,HEIGHT=800,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hand Controlled Dream Catcher Game")

#load assets
background=pygame.image.load("sky.webp")
player=pygame.image.load("basket.png")
star_image=pygame.image.load("star.png")
extra_life=pygame.image.load("extra_life.png")
#resize images
background=pygame.transform.scale(background,(WIDTH,HEIGHT))
player=pygame.transform.scale(player,(100,100))
star_image=pygame.transform.scale(star_image,(50,50))
extra_life=pygame.transform.scale(extra_life,(50,50))
#players dimension
player_width,player_height=100,100
player_x=WIDTH//2-player_width//2 #350
player_y=HEIGHT-120 #480
#stars setup
star_width,star_height=50,50
stars=[{"x":random.randint(0,WIDTH-star_width),"y":random.randint(-600,-50)}for _ in range (5)]
star_speed=6
#extra life setup
extraLife_width,extralife_height=50,50
extraLife={"x":random.randint(0,WIDTH-extraLife_width),"y":random.randint(-1500,-900),"active":True}
extraLife_speed=5
score=0
lives=5
game_over=False
font=pygame.font.SysFont(None,36)
game_over_font=pygame.font.SysFont(None,48)
#mediapipe  hand tracking setup
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.7)
mp_draw=mp.solutions.drawing_utils
#open cv camera setup
cap=cv2.VideoCapture(0) 
#game loop configuration
running=True
clock=pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_q:
                running=False
            if event.key==pygame.K_r and game_over:
                score=0
                lives=5
                game_over=False
                stars=[{"x":random.randint(0,WIDTH-star_width),"y":random.randint(-600,-50)}for _ in range (5)]
                extraLife={"x":random.randint(0,WIDTH-extraLife_width),"y":random.randint(-1500,-900),"active":True}
    screen.blit(background,(0,0))
    success,frame=cap.read()
    if success:
        frame=cv2.flip(frame,1)
        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=hands.process(rgb_frame)
        if results.multi_hand_landmarks and not game_over:
            for hand_landmarks in results.mutli_hand_landmarks:
                x=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                player_x=int(x*WIDTH)-player_width//2
                mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Hand tracking debug",frame)
    player_x=max(0,min(WIDTH-player_width,player_x))
    if not game_over:
        for star in stars:
            star["y"]+=star_speed
            if star["y"]>HEIGHT:
                star["x"]=random.randint(0,WIDTH-star_width)
                star["y"]=random.randint(-600,-50)
                lives-=1
            if (player_x<star["x"]+star_width and player_x+player_width>star["x"] and player_y<star["y"]+star_height and player_y+player_height>star["y"]):
                score+=1
                star["x"]=random.randint(0,WIDTH-star_width)
                star["y"]=random.randint(-600,-50)
            screen.blit(star_image,(star["x"],star["y"]))
        if extraLife["active"]:
            extraLife["y"]+=extraLife_speed
            if extraLife["y"]>HEIGHT:
                extraLife["x"]=random.randint(0,WIDTH-extraLife_width)
                extraLife["y"]=random.randint(-1500,-900)
            if (player_x<extraLife["x"]+extraLife_width and player_x+player_width>extraLife["x"] and player_y<extraLife["y"]+extralife_height and player_y+player_height>extraLife["y"]):
                lives+=1
                extraLife["x"]=random.randint(0,WIDTH-extraLife_width)
                extraLife["y"]=random.randint(-1500,-900)
            screen.blit(extra_life,(extraLife["x"],extraLife["y"]))
        if lives<=0:
            game_over=True
    screen.blit(player,(player_x,player_y))
    score_text=font.render(f"Score: {score} ",True,(255,255,255))
    lives_text=font.render(f"Lives: {lives} ",True,(255,255,255))
    screen.blit(score_text,(10,10))
    screen.blit(lives_text,(WIDTH-120,10))
    if game_over:
        go_text=game_over_font.render("Game Over!",True,(255,0,0))
        sub_text=font.render("press 'r' to restrart or 'q' to quit",True,(255,255,255))
        screen.blit(go_text,(WIDTH//2-100,HEIGHT//2-40))
        screen.blit(sub_text,(WIDTH//2-200,HEIGHT//2+10))
    pygame.display.flip()
    clock.tick(30)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()

