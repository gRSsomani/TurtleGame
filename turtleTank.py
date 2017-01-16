# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 23:23:45 2016

@author: Gaurav Somani
"""

import turtle
from random import randint
from math import sqrt
import winsound

turtle.setundobuffer(None)

turtle.setup(1000,660)
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Turtle-Tank")
wn.bgpic("backgroundPS.gif")

turtle.register_shape("turtleP.gif")
turtle.register_shape("spriteR.gif")
turtle.register_shape("bulletS.gif")

#gunshot = open("GunsoundS.wav","rb")
#explosion = open("explosionS.wav","rb")


##########Game Area##############
bpen = turtle.Turtle()
bpen.speed(0)
#colors = ["blue", "red"]
bpen.penup()
bpen.pensize(5)
bpen.setposition(-400,-300)
bpen.pendown()
#border
for _ in xrange(2):
    bpen.color("blue")
    bpen.fd(800)
    bpen.lt(90)
    bpen.color("red")
    bpen.fd(600)
    bpen.lt(90)
bpen.hideturtle()
###################################


class score(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        #self.screen = screen
        self.color("white")
        self.setpos(-400,300)
        self.points = -1
        
    def display_score(self, kills):
        if not self.points == kills:
            self.clear()
            s = "Your Score : "+str(kills)
            self.write(s, move= False, align = "left", font = ("Times New Roman", 18, "bold italic"))
            self.points = kills
            #self.ht()


class bullet(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        #self.screen = screen
        self.shape('bulletS.gif')
        #self.color('yellow')
        self.stepsize = 40
        self.setheading(90)
        #self.shapesize(0.5,0.5)
        self.state = "load"
        self.ht()
    
    def out(self):
        return self.ycor() >= 300
    
    def move(self):
        y = self.ycor() + self.stepsize
        self.sety(y)
        if self.out():
            self.ht()
            self.state = "load"


class shooter(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.shape('turtleP.gif')
        #self.color('red')
        #self.screen = screen
        self.sety(-270)
        self.seth(90)
        self.stepsize = 20
        self.kills = 0
        self.bullet_buffer = []
        
    def right_move(self):
        tempx = self.xcor() + self.stepsize
        if tempx <= 380:
            self.setx(tempx)
        else:
            self.setx(-380)
    
    def left_move(self):
        tempx = self.xcor() - self.stepsize
        if tempx >= -380:
            self.setx(tempx)
        else:
            self.setx(380)

    def fire_bullet(self):
        for bull in self.bullet_buffer:
            if bull.state == "load":
                bull.showturtle()
                bull.setpos(self.xcor(), self.ycor())
                bull.state = "fire"
                #winsound.PlaySound(gunshot.read(), winsound.SND_MEMORY)
                winsound.PlaySound('GunsoundS.wav',winsound.SND_FILENAME|winsound.SND_NOWAIT,)
                bull.move()
                break

    def fight(self,monsters):
        for bullets in self.bullet_buffer:
            if bullets.state == "fire":
                bullets.move()
                for enemy in monsters:
                    if collision(bullets, enemy):
                        #winsound.PlaySound(explosion.read(), winsound.SND_MEMORY)
                        winsound.PlaySound('explosionS.wav',winsound.SND_FILENAME|winsound.SND_NOWAIT,)
                        enemy.respawn()
                        self.kills += 1
                        bullets.ht()
                        bullets.state = "load"      


class monster(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        #self.screen = screen
        self.shape('spriteR.gif')
        #self.color('green')
        self.stepsize = 4
        self.setpos(randint(-370, 370), randint(200, 290))
    
    def move(self):
        x = self.xcor() + self.stepsize
        self.setx(x)
        if abs(x) >= 370:
            for enemy in monsters:
                enemy.sety(enemy.ycor()-40)
                enemy.stepsize *= -1

    def respawn(self):
        self.ht()
        self.setpos(randint(-370, 370), randint(200, 290))
        self.st()
    

def collision(object1, object2):
    distance = sqrt((object1.xcor()-object2.xcor())**2 + (object1.ycor()-object2.ycor())**2)
    if distance <= 15:
        return True
    return False


player = shooter()
monsters = []
scoring  = score()

for _ in xrange(10):
    monst = monster()
    monsters.append(monst)

for _ in xrange(5):
    player.bullet_buffer.append(bullet())


def leftmovement():
    player.left_move()

def rightmovement():
    player.right_move()

def fire():
    player.fire_bullet()


turtle.listen()
turtle.onkey(leftmovement, "Left")
turtle.onkey(rightmovement, "Right")
turtle.onkey(fire, "space")


gameover = False
while not gameover:
    for enemy in monsters:
        enemy.move()
        if collision(enemy, player) or enemy.ycor() <= player.ycor():
            #winsound.PlaySound(explosion.read(), winsound.SND_MEMORY)
            winsound.PlaySound('explosionS.wav',winsound.SND_FILENAME|winsound.SND_NOWAIT,)
            gamepen = turtle.Turtle()
            gamepen.color("green")
            gamepen.write("GAME OVER : Score= "+str(player.kills), font = ("Arial bold italic", 30), align = "center")
            gamepen.ht()
            gameover = True
            
    player.fight(monsters)
    scoring.display_score(player.kills)

turtle.mainloop() 
