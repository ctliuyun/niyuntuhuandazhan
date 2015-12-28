# -*- coding: UTF-8 -*-
# 1 - 引用pygame模块 -

import pygame
from pygame.locals import *
import math
import random


# 2 - 初始化游戏 设置一个640,480的窗口 -

pygame.init()

width, height = 640, 480

screen = pygame.display.set_mode((width, height))

# 定义窗口的标题
pygame.display.set_caption('倪云-兔兔大战獾獾')

# 定义玩家精度，箭头数与命中数。
acc = [0,0]

# 定义箭头群
arrows=[]

# 设置控制按键 WASD
keys = [False,False,False,False]

# 设置玩家位置
playerpos = [100,100]

# 獾定时器,每隔一段时间就新生成一个獾
badtimer=100
badtimer1=0
badguys=[[640,100]]

# 地堡的健康值
healthvalue=194

# 声音模块初始化
pygame.mixer.init()

# 3 - 加载声音、图片 -

# 3.1 - 加载声音
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
# 设置音量大小
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
# 加载背景声音
pygame.mixer.music.load('resources/audio/moonlight.wav')
#循环播放
pygame.mixer.music.play(-1, 0.0)
# 设置背景音乐的声音大小
pygame.mixer.music.set_volume(0.25)

# 加载图片兔子图片
player = pygame.image.load("resources/images/dude2.png")

# 加载背景图片
grass = pygame.image.load("resources/images/grass.png")
# 加载地堡图片
castle = pygame.image.load("resources/images/castle.png")
# player=pygame.image.load("resources/images/dude.png")

# 加载箭头的图片
arrow = pygame.image.load("resources/images/bullet.png")

# 加载獾的图片
badguyimg1 = pygame.image.load("resources/images/badguy.png")
# 复制了獾的图片
badguyimg = badguyimg1

# 加载血条图片
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

# 加载输赢图片
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")


# 4 - 开始循环 -
running = 1
exitcode = 0
while running:
    badtimer-=1
    # 5 开始绘制前，清除屏幕

    screen.fill(0)

    # 6 绘制屏幕，放置背景，兔子，地堡

    
    #  绘制背景，利用双层循环将背景图片铺满屏幕
    for x in range(width/grass.get_width()+1):
        for y in range(height/grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
    # - 绘制地堡，四个地堡          
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345))


    #创建一个字体
    #font=pygame.font.SysFont('SimHei',36)
    #创建要显示的文本
    #text=u'中国' #unicode编码
    #创建一个字体表面
    #text_surf = font.render(text,True,(255,0,0))
    #pygame.font.init()
    #font = pygame.font.SysFont('楷体',14)
    # 64位windows 无法使用 SysFont 来使用中文字体
    font = pygame.font.Font('resources/font/MSYHMONO.ttf',14)
    survivedtext = font.render(u"倪云 兔兔大战獾獾 方向控制：WSAD 射击：鼠标左键",True,(0,0,0))
    textRect = survivedtext.get_rect()
    #textRect.topright=[600,475]
    textRect.bottomright=[500,475]
    screen.blit(survivedtext,textRect)
 



    
    #screen.blit(player, playerpos)

    # 6.1 - 控制兔子的位置和旋转
    position = pygame.mouse.get_pos()

    # 加32和26，是取兔子图片的中点的坐标,算出兔子的角度和弧度
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    
    #playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    # 旋转兔子
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    # 算出兔子旋转后的位置
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    # 绘制兔子
    screen.blit(playerrot, playerpos1)
    # 6.2 - 绘制箭头
    index=0
    for bullet in arrows:
        
        # 10为箭头的速度
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        # 如果箭头超过屏幕就删除掉
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
        #arrow1 = pygame.transform.rotate(arrow,360-bullet[0]*57.29)
        #screen.blit(arrow1,(bullet[1],bullet[2]))
        # 绘制箭头
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow,360-projectile[0]*57.29)
            screen.blit(arrow1,(projectile[1],projectile[2]))
            #velx=math.cos(projectile[0])*10
            #vely=math.sin(projectile[0])*10
            #projectile[1]+=velx
            #projectile[2]+=vely

    # 6.3 - 绘制獾

    # 如果定时器结束那么就生成一个獾

    if badtimer==0:
        badguys.append([640,random.randint(50,430)])
        # 控制獾生成的速度，越往后越快，但控制在30的速度上 100-35*2
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    for badguy in badguys:
        # 如果獾的位置跑出左边的屏幕，就删除掉
        if badguy[0]<-64:
            badguys.pop(index)
        # 獾向左边移动7个点    
        badguy[0]-=7
        # 6.3.1 撞到地堡的獾，减少地堡的健康值健康然后删除掉獾
        badrect=pygame.Rect(badguyimg.get_rect())
        badrect.top=badguy[1] #确定獾的矩形块的位置，以便和下面箭头的位置比较
        badrect.left=badguy[0]
        if badrect.left<64:
            #播放撞击地堡的声音
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        # 6.3.2 如果箭头遇到獾就杀死它
        index1=0
        for bullet in arrows:
            bullrect =pygame.Rect(arrow.get_rect())
            bullrect.top=bullet[2] #确定箭头的矩形块的位置，以便和上面獾的位置比较
            bullrect.left=bullet[1]
            # 判断箭头的矩形和獾的矩形是否交叉，交叉就是命中了
            if badrect.colliderect(bullrect):
                #播放命中的声音
                enemy.play()
                acc[0]+=1
                badguys.pop(index)
                arrows.pop(index1)
            index1+=1    
    # 6.3.3 下一个獾
        index+=1
        
    # 绘制獾    
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    # 6.4 - 增加一个计时器
    font = pygame.font.Font(None,24)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2),True,(0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext,textRect)
    # 6.5 - 绘制血条
    screen.blit(healthbar,(5,5))
    for health1 in range(healthvalue):
        screen.blit(health,(health1+8,8))
  
    # 7 更新屏幕

    pygame.display.flip()

    # 8 检查事件
    for event in pygame.event.get():

        # 检查事件是否是X按钮

        if event.type == pygame.QUIT:    

        # 如果是，就退出游戏            
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0]=True
            elif event.key == K_a:
                keys[1]=True
            elif event.key == K_s:
                keys[2]=True
            elif event.key == K_d:
                keys[3]=True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                 keys[0]=False
            elif event.key == pygame.K_a:
                 keys[1]=False
            elif event.key == pygame.K_s:
                 keys[2]=False
            elif event.key == pygame.K_d:
                 keys[3]=False
        # 如果点击鼠标就射出一支箭
        if event.type == pygame.MOUSEBUTTONDOWN:
            #播放射箭的声音
            shoot.play()
            #获取鼠标位置
            position=pygame.mouse.get_pos()
            # 计数
            acc[1]+=1
            # 计算箭头的旋转角度放入arrows数组
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
            

    # 9 移动兔子
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    elif keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5

        
    #10 - 输赢检查
    # 如果时间超过    
    if pygame.time.get_ticks()>=90000:
        running=0
        exitcode=1
    # 如果血条为0    
    if healthvalue<=0:
        running=0
        exitcode=0
    # 计算命中率    
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
    else:
        accuracy=0
    # 11 - 输赢结果        
if exitcode==0:
    pygame.font.init()
    font = pygame.font.Font('resources/font/MSYHMONO.ttf', 24)
    text = font.render(u"命中率: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font('resources/font/MSYHMONO.ttf', 24)
    text = font.render(u"命中率: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
   


