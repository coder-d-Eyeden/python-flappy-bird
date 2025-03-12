import asyncio
import pygame as pg
import time
from pipe import Pipe
from bird import Bird
import os


pg.init()

class Game:
    def __init__(self):
        self.width=600
        self.height=767
        self.scale_factor=1.5
        self.win=pg.display.set_mode((self.width,self.height))
        self.caption=pg.display.set_caption("Tuntuni Pakhi")
        self.move_speed=300
        self.clock=pg.time.Clock()
        pg.mixer.init()
        self.is_enter_pressed=False
        self.pipes=[]
        self.start_monitoring=False
        self.score= 0
        self.font = pg.font.Font(os.path.join("assets", "font.ttf"), 20)

        #Loading the Background
        self.bg_img=pg.transform.scale_by(pg.image.load(os.path.join('assets','bg.png')).convert(),self.scale_factor)
        #Loading the Ground
        self.ground1=pg.transform.scale_by(pg.image.load(os.path.join('assets','ground.png')).convert(),self.scale_factor)
        self.ground2=pg.transform.scale_by(pg.image.load(os.path.join('assets','ground.png')).convert(),self.scale_factor)
       

        self.score_text=self.font.render("Score: 0",True,(255,255,255))
        self.score_text_rect=self.score_text.get_rect(center=(90,30))

        self.restart_text=self.font.render("Restart",True,(0,0,0))
        self.restart_text_rect=self.restart_text.get_rect(center=(300,650))

        self.enter_text=self.font.render("Press Enter to start",True,(255,255,255))
        self.enter_text_rect=self.enter_text.get_rect(center=(300,250))

        self.fly_text=self.font.render("Press space bar to fly",True,(255,255,255))
        self.fly_text_rect=self.fly_text.get_rect(center=(300,300))

        # self.dead_sound=pg.mixer.Sound(r"assets\sfx\dead.wav")
        # self.flap_sound=pg.mixer.Sound(r"assets\sfx\flap.wav")
        # self.score_sound=pg.mixer.Sound(r"assets\sfx\score.wav")
        # self.falling_sound=pg.mixer.Sound(r"assets\sfx\falling.mp3")

        self.dead_sound = pg.mixer.Sound(os.path.join("assets", "sfx", "dead.wav"))
        self.flap_sound = pg.mixer.Sound(os.path.join("assets", "sfx", "flap.wav"))
        self.score_sound = pg.mixer.Sound(os.path.join("assets", "sfx", "score.wav"))
        self.falling_sound = pg.mixer.Sound(os.path.join("assets", "sfx", "falling.mp3"))


        self.pipe_generate_counter=60
        self.onscreen_text=True
        self.bird=Bird()
        self.gravity=False
        self.is_game_started=True
        

        
        self.background()
        self.gameloop()
        
    

    def restartGame(self):
        self.score=0
        self.score_text=self.font.render("Score: 0",True,(255,255,255))
        self.is_enter_pressed=False
        self.is_game_started=True
        self.bird.resetposition()
        self.pipes.clear()
        self.gravity=False
        pg.mixer.Sound.stop(self.falling_sound)
        self.onscreen_text=True


#Checking Collision
    def check_collision(self,dt):
        if len(self.pipes) !=0:


            if (self.bird.rect.bottom > self.ground1_rect.y):
                self.is_enter_pressed=False
                self.dead_sound.play(0,0,5)
                self.bird.gravity_on=False
                self.is_game_started=False

            if self.bird.rect.colliderect(self.pipes[0].rect_down) or self.bird.rect.colliderect(self.pipes[0].rect_up):
                self.is_enter_pressed=False
                self.gravity=True
                self.is_game_started=False
                # self.dead_music()
                self.dead_sound.play(0,0,5)
                self.falling_sound.play(0,0,1)
                 #here the problem was when bird collide with the pipe the update function stops so the bird also 
                #stopped in the middle air but i want to apply the gravity.so to make the applyGravity() independent of the update_everything() function 
                #I make another another variable gavity which is false from the beginning.
               
    def check_score(self):
        if len(self.pipes)>0:
            if ((self.bird.rect.left > self.pipes[0].rect_down.left) and
                (self.bird.rect.right < self.pipes[0].rect_down.right) and not self.start_monitoring):
                
                self.start_monitoring=True
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring=False
                self.score += 1
                self.score_text=self.font.render(f"Score: {self.score}",True,(255,255,255))
                # self.score_music()
                self.score_sound.play()
                
#Updating the Window
    def update_everything(self,dt):
         if self.gravity:
             self.bird.applyGravity(dt)
             #when there is no collision the grevity remain false and this code does not execute. but when the collision happes 
             #gravity becomes true and is enter pressed become false. so the update func stops but not the applygravity()
         if self.is_enter_pressed:
            
            self.moving_ground(dt)
            self.generate_pipes(dt)
        
            self.check_collision(dt)
            self.bird.applyGravity(dt)
            self.bird.update(dt)
            self.onscreen_text=False
            

#Displaying Every thing
    def draw_everything(self):
        #Showing the Background Image
        self.win.blit(self.bg_img,(0,-300))

        #Drawing Pipes
        for pipe in self.pipes:
            pipe.draw_pipe(self.win)

        #Showing the Ground
        self.win.blit(self.ground1,self.ground1_rect)
        self.win.blit(self.ground1,self.ground2_rect)
        self.win.blit(self.bird.image,self.bird.rect)
        self.win.blit(self.score_text,self.score_text_rect)
        if not self.is_game_started :
            self.win.blit(self.restart_text,self.restart_text_rect)
        if self.onscreen_text :
            self.win.blit(self.enter_text,self.enter_text_rect)
            self.win.blit(self.fly_text,self.fly_text_rect)
            
#Back Ground
    def background(self):
        

        #To get the Positon of the ground Image
        self.ground1_rect=self.ground1.get_rect()
        self.ground2_rect=self.ground2.get_rect()

        #Setting the positon of the Ground
        self.ground1_rect.x=0
        self.ground2_rect.x=self.ground1_rect.right
        self.ground1_rect.y=self.ground2_rect.y=568

#Moving Ground
    def moving_ground(self,dt):
        self.ground1_rect.x -= int(self.move_speed *dt)
        self.ground2_rect.x -= int(self.move_speed *dt)

        if self.ground1_rect.right < 0:
            self.ground1_rect.x=self.ground2_rect.right
        if self.ground2_rect.right <0:
            self.ground2_rect.x=self.ground1_rect.right

#Generating  Pipes
    def generate_pipes(self,dt):
        if self.pipe_generate_counter>100:
            self.pipes.append(Pipe(self.scale_factor,self.move_speed))
            self.pipe_generate_counter=30
        self.pipe_generate_counter+=1

        for pipe in self.pipes:
            pipe.update(dt)
        
        if len(self.pipes) != 0:
            if self.pipes[0].rect_up.right <0:
                self.pipes.pop(0)
    
    async def gameloop(self):
            last_time=time.time()
            is_running=True
            while is_running:
                new_time=time.time()
                dt=new_time-last_time
                last_time=new_time
                # print(dt)
                # print("1")
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        is_running=False
                    if event.type == pg.KEYDOWN and self.is_game_started:
                        if event.key == pg.K_RETURN:
                            self.is_enter_pressed=True
                        if event.key == pg.K_SPACE and self.is_enter_pressed:
                            self.bird.flap(dt)
                            # self.flap_music()
                            self.flap_sound.play()
                            
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                            self.restartGame()

                
                self.update_everything(dt)
                self.draw_everything()
                pg.display.update()
                self.clock.tick(60)
                self.check_score()
                await asyncio.sleep(0.01)
    
async def main():
    game =Game()
    await game.gameloop()

if __name__=='__main__':
    asyncio.run(main())