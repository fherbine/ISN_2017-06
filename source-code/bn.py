#!/usr/bin/python3.2
# -*-coding:utf-8 -*

import os
os.chdir('/root/Desktop/')
import src
import RPi.GPIO as GPIO
import time
import sys
from random import randint

GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.IN) #fGauche
GPIO.setup(19,GPIO.IN) #fHaut
GPIO.setup(21,GPIO.IN) #fBas
GPIO.setup(20,GPIO.IN) #X
GPIO.setup(13,GPIO.IN) #fDroite
GPIO.setup(16,GPIO.IN) #V
GPIO.setup(24,GPIO.IN) #close
GPIO.setup(23,GPIO.IN) #start
GPIO.setup(22,GPIO.IN) #jGauche
GPIO.setup(17,GPIO.IN) #jHaut
GPIO.setup(27,GPIO.IN) #jBas
GPIO.setup(4,GPIO.IN)  #jDroite

quitter=src.creer_t(2,2)
chargement=src.creer_t(10,2)

def ecranBN():
    tableau=src.creer_t(11,11)
    tableau[0][0]="X"
    abc='*abcdefghijklmnopqrstuvwxyz'
    abc=abc.upper()

    for i in range(11):
        if i != 0:
            if len(str(i))==1:
                tableau[0][i]="0"+str(i)
            else: tableau[0][i]=str(i)
    for i in range(11):
        if i != 0:
            tableau[i][0]=abc[i]
    return(tableau)

tableau1=ecranBN()
tableau2=[]
tablCourant=tableau1

quitter[0][1]=' OUI'
quitter[1][1]=' NON'

chargement[1][0]='\n'*10

for i in range(10):
    chargement[0][i]='__'

def verif(x,y,liste):
    ret=True
    for i in liste:
        if (x,y) in i:
            ret=False
    return(ret)
creation=True
deplacement=True
modulex=1
moduley=1
mx=my=1
bateau=False
gpioPre=0
compteur=0
bat=0
bat6432=[0,0,0,0]
etape="Création"
fermer='Quitter ?'
posJ1=[]
xIA=randint(1,10)
yIA=randint(1,10)
posIA=[]
toutesPosIA=[]
IA=False
nBateau=True
creaIA=True
choixIA=0
p=0
eau=True
jeu=False
jeuIA=False
tour=False
message=''
posIAcombat=[[]]
fin=False
gagnant=''

os.system('clear')
src.ecranDem()
time.sleep(5)
while 1:
    src.afficher(tablCourant,etape)
    print(posIA)
    print("position du curseur:"+str((tablCourant[moduley][0],modulex)))
    if creation==True:print('bateau 6 cases: '+str(bat6432[0])+'/1\nbateau 4 cases: '+ str(bat6432[1])+'/2\nbateau 3 cases: '+ str(bat6432[2])+'/3\nbateau 2 cases: '+ str(bat6432[3])+'/4')
    if 0<= compteur < 1:bat=6
    elif 1 <= compteur < 3:bat=4
    elif 3 <= compteur < 6:bat=3
    elif 6 <= compteur < 10:bat=2
    elif compteur>=10:
        creation=False
        deplacement=False
        IA=True
    if GPIO.input(24):
        quitter[0][0]='>>'
        mx=modulex
        my=moduley
        modulex=moduley=0
        while GPIO.input(23)!=True:
            src.afficher(quitter,fermer)
            if GPIO.input(17) and moduley>0:
                quitter=src.deplacement(quitter,modulex,moduley,modulex,moduley-1,">")
                moduley -=1
            elif GPIO.input(27) and moduley<1:
                quitter=src.deplacement(quitter,modulex,moduley,modulex,moduley+1,">")
                moduley+=1
            time.sleep(0.1)
        if moduley==0:
            sys.exit(0)
        else:
            modulex=mx
            moduley=my
            quitter[1][0]='  '
            
    if deplacement == True:
        if GPIO.input(17) and moduley > 1:
            tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex,moduley-1,"_")
            moduley=moduley-1
        elif GPIO.input(27) and moduley < 10:
            tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex,moduley+1,"_")
            moduley=moduley+1
        elif GPIO.input(4) and modulex < 10:
            tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex+1,moduley,"_")
            modulex=modulex+1
        elif GPIO.input(22) and modulex > 1:
            tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex-1,moduley,"_")
            modulex=modulex-1
        elif creation == True:
            if GPIO.input(16):
                tablCourant[moduley][modulex]="██"
                posJ1.append([(modulex,moduley)])
                pionx=modulex
                piony=moduley
                src.afficher(tablCourant,etape)
                while bateau is not True:
                    if GPIO.input(17) and moduley > bat and (gpioPre==0 or gpioPre==27):
                        tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex,moduley-(bat-1),"_")
                        src.afficher(tablCourant,etape)
                        print("position du curseur:"+str((tablCourant[moduley][0],modulex)))
                        gpioPre=17
                        moduley -= bat
                    elif GPIO.input(27) and moduley < 11-bat and (gpioPre==0 or gpioPre==17):
                        tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex,moduley+(bat-1),"_")
                        src.afficher(tablCourant,etape)
                        print("position du curseur:"+str((tablCourant[moduley][0],modulex)))
                        gpioPre=27
                        moduley+=bat
                    elif GPIO.input(4) and modulex < 11-bat and (gpioPre==0 or gpioPre==22):
                        tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex+(bat-1),moduley,"_")
                        src.afficher(tablCourant,etape)
                        print("position du curseur:"+str((tablCourant[moduley][0],modulex)))
                        gpioPre=4
                        modulex+=bat
                    elif GPIO.input(22) and moduley > bat and (gpioPre==0 or gpioPre==4):
                        tablCourant=src.deplacement(tablCourant,modulex,moduley,modulex-(bat-1),moduley,"_")
                        src.afficher(tablCourant,etape)
                        print("position du curseur:"+str((tablCourant[moduley][0],modulex)))
                        gpioPre=22
                        modulex-=bat
                    elif GPIO.input(16):
                        if gpioPre==17:
                            for i in range(bat-1):
                                if tablCourant[piony-(1+i)][pionx]!="██":
                                    tablCourant[piony-(1+i)][pionx]="██"
                                    posJ1[compteur].append((pionx,piony-(1+i)))
                            bateau = True
                        elif gpioPre==27:
                            for i in range(bat-1):
                                if tablCourant[piony+(1+i)][pionx]!="██":
                                    tablCourant[piony+(1+i)][pionx]="██"
                                    posJ1[compteur].append((pionx,piony+(1+i)))
                            bateau=True
                        elif gpioPre==4:
                            for i in range(bat-1):
                                if tablCourant[piony][pionx+(1+i)]!="██":
                                    tablCourant[piony][pionx+(1+i)]="██"
                                    posJ1[compteur].append((pionx+(1+i),piony))
                            bateau=True
                        elif gpioPre==22:
                            for i in range(bat-1):
                                if tablCourant[piony][pionx-(1+i)]!="██":
                                    tablCourant[piony][pionx-(1+i)]="██"
                                    posJ1[compteur].append((pionx-(1+i),piony))
                            bateau=True
                        if bateau == True:
                            if bat==6:bat6432[0]+=1
                            elif bat==4:bat6432[1]+=1
                            elif bat==3:bat6432[2]+=1
                            elif bat==2:bat6432[3]+=1
                    time.sleep(0.1)
                bateau=False
                gpioPre=0
                compteur+=1
        elif jeu==True:
            if GPIO.input(16):
                src.afficher(tablCourant,etape)
                for i in posIA:
                    if (modulex,moduley)in i:
                        eau = False
                if eau == True:
                    tablCourant[moduley][modulex]="~~"
                    message='a l\'eau'
                    tour=True
                else:
                    tablCourant[moduley][modulex]="▒▒"
                    tour=True
                    for i in range(len(posIA)):
                        if (modulex,moduley) in posIA[i]:
                            del posIA[i][posIA[i].index((modulex,moduley))]
                            if len(posIA[i])==0:message='touché, coulé'
                            else: message = 'touché'
                src.afficher(tablCourant,etape)
                print('\n\n\n')
                print(message)
                time.sleep(2)
            eau=True
            if tour==True:
                jeuIA=True
                IA=True
                jeu=False
                deplacement=False
                tour=False
    nBateau=True                
    time.sleep(0.1)
    if IA==True:
        if creaIA==True:
            src.afficher(chargement,'L\'ennemi place ses bateau ...')
            while p<10:
                time.sleep(0.1)
                chargement[0][p]='██'
                src.afficher(chargement,'L\'ennemi place ses bateau ...')
                posIA.append([])
                if p==0:
                    xIA=randint(1,10)
                    yIA=randint(1,10)
                    choixIA=randint(1,4)
                    posIA[p].append((xIA,yIA))
                    if choixIA==1 and xIA+5<=10 and verif(xIA+1,yIA,posIA):
                        for i in range(1,6):
                            xIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==2 and xIA-5>=1 and verif(xIA-1,yIA,posIA):
                        for i in range(1,6):
                            xIA-=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==3 and yIA+5<=10 and verif(xIA,yIA+1,posIA):
                        for i in range(1,6):
                            yIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==4 and yIA-5>=1 and verif(xIA,yIA-1,posIA):
                        for i in range(1,6):
                            yIA-=1
                            posIA[p].append((xIA,yIA))
                    else:
                        del posIA[p]
                        p-=1
                elif 0<p<=2:
                    xIA=randint(1,10)
                    yIA=randint(1,10)
                    choixIA=randint(1,4)
                    posIA[p].append((xIA,yIA))
                    if choixIA==1 and xIA+3<=10 and verif(xIA+1,yIA,posIA):
                        for i in range(1,4):
                            xIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==2 and xIA-3>=1 and verif(xIA-1,yIA,posIA):
                        for i in range(1,4):
                            xIA-=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==3 and yIA+3<=10 and verif(xIA,yIA+1,posIA):
                        for i in range(1,4):
                            yIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==4 and yIA-3>=1 and verif(xIA,yIA-1,posIA):
                        for i in range(1,4):
                            yIA-=1
                            posIA[p].append((xIA,yIA))
                    else:
                        del posIA[p]
                        p-=1
                elif 2<p<=5:
                    xIA=randint(1,10)
                    yIA=randint(1,10)
                    choixIA=randint(1,4)
                    posIA[p].append((xIA,yIA))
                    if choixIA==1 and xIA+2<=10 and verif(xIA+1,yIA,posIA):
                        for i in range(1,3):
                            xIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==2 and xIA-2>=1 and verif(xIA-1,yIA,posIA):
                        for i in range(1,3):
                            xIA-=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==3 and yIA+2<=10 and verif(xIA,yIA+1,posIA):
                        for i in range(1,3):
                            yIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==4 and yIA-2>=1 and verif(xIA,yIA-1,posIA):
                        for i in range(1,3):
                            yIA-=1
                            posIA[p].append((xIA,yIA))
                    else:
                        del posIA[p]
                        p-=1
                elif 5<p<=9:
                    xIA=randint(1,10)
                    yIA=randint(1,10)
                    choixIA=randint(1,4)
                    posIA[p].append((xIA,yIA))
                    if choixIA==1 and xIA+1<=10 and verif(xIA+1,yIA,posIA):
                        for i in range(1,2):
                            xIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==2 and xIA-1>=1 and verif(xIA-1,yIA,posIA):
                        for i in range(1,2):
                            xIA-=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==3 and yIA+1<=10 and verif(xIA,yIA+1,posIA):
                        for i in range(1,2):
                            yIA+=1
                            posIA[p].append((xIA,yIA))
                    elif choixIA==4 and yIA-1>=1 and verif(xIA,yIA-1,posIA):
                        for i in range(1,2):
                            yIA-=1
                            posIA[p].append((xIA,yIA))
                    else:
                        del posIA[p]
                        p-=1
                p+=1
            creaIA=False
            IA=False
            deplacement=True
            compteur=0
            tableau2=ecranBN()
            tablCourant = tableau2
            etape='Combat !'
            jeu=True
        elif jeuIA==True:
            xIA=randint(1,10)
            yIA=randint(1,10)
            while verif(xIA,yIA,posIAcombat)is not True:
                xIA=randint(1,10)
                yIA=randint(1,10)
            posIAcombat[0].append((xIA,yIA))
            tablCourant = tableau1
            src.afficher(tablCourant,etape)
            for i in range(len(posJ1)):
                if (xIA,yIA) in posJ1[i]:
                    eau=False
            if eau==True:
                tableau1[yIA][xIA]='~~'
                message='a l\'eau'
                tour=True
            else:
                tableau1[yIA][xIA]='▒▒'
                tour=True
                for i in range(len(posJ1)):
                        if (xIA,yIA) in posJ1[i]:
                            del posJ1[i][posJ1[i].index((xIA,yIA))]
                            if len(posJ1[i])==0:message='touché, coulé'
                            else: message = 'touché'
            src.afficher(tablCourant,etape)
            time.sleep(0.5)
            print('\n\n\n')
            print(message)
            time.sleep(1.5)
            if tour==True:
                jeuIA=False
                deplacement=True
                jeu=True
                IA=False
                eau=True
                tour=False
                tablCourant = tableau2
    if etape=='Combat !':
        for i in range(len(posIA)):
            if len(posIA[i])!=0:
                fin=False
                gagnant=' Bravo,vous avez gagné !'
                break
            else:
                fin=True
                
        for i in range(len(posJ1)):
            if len(posJ1[i])!=0:
                fin=False
                gagnant=' Dommage, l\'ordinateur est vainqueur !'
                break
            else:
                fin=True
        if fin==True:break
print(gagnant)
input('')
