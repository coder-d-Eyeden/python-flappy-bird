import pygame as pg
import os

class Bird(pg.sprite.Sprite):
    def __init__(self):
        super(Bird,self).__init__()
        # self.img_list=[pg.image.load(r"assets/birdup.png").convert_alpha(),
        #                pg.image.load(r"assets/birddown.png").convert_alpha()]
        

        self.img_list = [
            pg.image.load(os.path.join("assets", "birdup.png")).convert_alpha(),
            pg.image.load(os.path.join("assets", "birddown.png")).convert_alpha()]


        self.image_index=0
        self.image=self.img_list[self.image_index]
        self.rect=self.image.get_rect(center=(100,100))

    
        self.y_velocity= 0
        self.gravity=15
        self.flapspeed=200
        self.anim_counter=0
        self.gravity_on=True


    def update(self,dt):
        self.playAnimation()
        
        # if self.gravity_on:
        if self.rect.y <= 0:
            self.rect.y = 0
            self.flapspeed=0
        if self.rect.y >0:
            self.flapspeed=200
            
    
    def applyGravity(self,dt):
        if self.gravity_on:
            self.y_velocity += self.gravity * dt
            self.rect.y += self.y_velocity


    def flap(self,dt):
        self.y_velocity = -self.flapspeed * dt

    def playAnimation(self):
        if self.anim_counter==5:
            self.image=self.img_list[self.image_index]
            if self.image_index == 0: self.image_index =1 
            else: self.image_index=0
            self.anim_counter=0
        
        self.anim_counter += 1

    def resetposition(self):
        self.rect.center=(100,100)
        self.y_velocity=0
        self.anim_counter=0
        self.gravity=10
        self.gravity_on=True