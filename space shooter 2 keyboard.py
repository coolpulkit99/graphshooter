import matplotlib.pyplot as plt
import matplotlib.patches as shapes
import _thread
import os
import numpy
from time import sleep
import keyboard
import math
import random
valgyro=0
initialpoints = [[-1, 0], [0, 1], [1, 0]]  #normal triangle [[-1, 0], [0, 1], [1, 0]]   if initialpoints array size<points array size =shape creation on keyboard action
counter = 32 # Below 32 everything in ASCII is gibberish
bulletshoot=False
bulletmove=[0,0]
anglecounter=0
bulletspeed=1
bulletspeed2=0.5
bulletradius=.3
deadcircles=0
circleparams=[[5,5],2,'gray']
shooteranglechanger=7
colors=['gold','silver','purple','black','orange']
maxgraphrange=[-20,20]
maxcircleparams=[3,15]
maxcircleradius=[2,3]
while True:
    something=False
    if(keyboard.is_pressed('Esc')):
        exit() 
        something=True
    if(keyboard.is_pressed('t')):
        circleparams[0][0]=random.randint(maxcircleparams[0],maxcircleparams[1])*[-1,1][random.randint(0,1)]
        circleparams[0][1]=random.randint(maxcircleparams[0],maxcircleparams[1])*[-1,1][random.randint(0,1)]
        circleparams[1]=random.randint(maxcircleradius[0],maxcircleradius[1])
        circleparams[2]=colors[random.randint(0,4)]
        
    if(keyboard.is_pressed('right')):
        anglecounter -=shooteranglechanger
        something=True
    if(keyboard.is_pressed('left')):
        anglecounter +=shooteranglechanger
        something=True
    if(something):
        valgyro=anglecounter
        print (valgyro) # Read the newest output from the Arduino
    #sleep(.0001) # Delay for one tenth of a second
    plt.ion()
    plt.figure(1)
    plt.clf()
    plt.axes(xlim=(maxgraphrange[0],maxgraphrange[1]), ylim=(maxgraphrange[0],maxgraphrange[1]))#grid size initially -10 10 -10 10 
    plt.text(14,18,"Score:"+str(deadcircles))
    plt.text(11,-19,"Controls:\n<-: Rotate Left\n->: Rotate right\nSpace: Shoot\nT:Skip Obstacle")
    points = [[-1, 0], [0, 1], [1, 0]]     #normal triangle [[-1, 0], [0, 1], [1, 0]]   
    def updateshooter():
        for ik1 in range(len(initialpoints)):
            points[ik1][0]=initialpoints[ik1][0]*numpy.cos(numpy.radians(valgyro))-initialpoints[ik1][1]*numpy.sin(numpy.radians(valgyro))
            points[ik1][1]=initialpoints[ik1][0]*numpy.sin(numpy.radians(valgyro))+initialpoints[ik1][1]*numpy.cos(numpy.radians(valgyro))#-45 from all valgyro values bullet correction    
        polygon=plt.Polygon(points)#pos_shooter)
        plt.gca().add_patch(polygon)
    
    def objects():
        circle=shapes.Circle((5,5), 2)
    
        
#updateshooter(points)
    
    circle=shapes.Circle((circleparams[0][0],circleparams[0][1]), circleparams[1],color=circleparams[2])#used blue color before

    plt.gca().add_patch(circle)
    updateshooter()#points)
    
    if(keyboard.is_pressed("space")):
        bulletshoot=True
        bulletx =points[1][0]
        bullety =points[1][1]
        bulletmove[0]=numpy.cos(numpy.radians(valgyro+45))-numpy.sin(numpy.radians(valgyro+45))
        bulletmove[1]=numpy.cos(numpy.radians(valgyro+45))+numpy.sin(numpy.radians(valgyro+45))
        
    if(bulletshoot):
        bullet=shapes.Circle((bulletx+bulletmove[0]*bulletspeed,bullety+bulletmove[1]*bulletspeed), bulletradius,color='yellow')#used green color before
        plt.gca().add_patch(bullet)
        distcirclebullet=math.sqrt((bulletx+bulletmove[0]*bulletspeed-circleparams[0][0])**2+(bullety+bulletmove[1]*bulletspeed-circleparams[0][1])**2)
        if(distcirclebullet<=circleparams[1]+bulletradius):
            circle=shapes.Circle((circleparams[0][0],circleparams[0][1]), circleparams[1],color='red')
            plt.gca().add_patch(circle)
            bulletshoot=False
            deadcircles+=1
            circleparams[0][0]=random.randint(maxcircleparams[0],maxcircleparams[1])*[-1,1][random.randint(0,1)]
            circleparams[0][1]=random.randint(maxcircleparams[0],maxcircleparams[1])*[-1,1][random.randint(0,1)]
            circleparams[1]=random.randint(maxcircleradius[0],maxcircleradius[1])
            circleparams[2]=colors[random.randint(0,4)]
    if(deadcircles>=10):
        maxgraphrange=[-30,30]
        maxcircleparams=[5,25]
        maxcircleradius=[2,4]

    polygon=plt.Polygon([[circleparams[0][0],circleparams[0][1]],[points[1][0],points[1][1]],[points[1][0]+.1,points[1][1]+.1],[circleparams[0][0]+.1,circleparams[0][1]+.1]])#pos_shooter)
    plt.gca().add_patch(polygon)

    bulletmove[0]+=bulletmove[0]*bulletspeed2
    bulletmove[1]+=bulletmove[1]*bulletspeed2
    

    #plt.pause(0.5)
    plt.show(block=False)
    plt.pause(0.00000000000000005)
#plt.show()
    #plt.show()
    #plt.figure.canvas.draw()
    #plt.close(1)
    #plt.close('all')
    #plt.clf()
