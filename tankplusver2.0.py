# -*- coding: utf-8 -*-  
import pygame
from pygame.locals import *
import random
import math
from gameobjects.vector2 import Vector2
import time
from button import Button
from graphics import *
# from astar1 import *

#2 
width,height=660,660
win=GraphWin("Welcome",250,250)
win.setCoords(0,0,10,10)
win.setBackground("black")
startButton=Button(win,Point(5,5),4,1,"start")
startButton.activate()
pt=win.getMouse()
runningmode=1
while runningmode:
	if startButton.clicked(pt):
		win.close()
		pygame.init()
		#初始化
		screen=pygame.display.set_mode((width,height))
		keys=[False,False,False,False]
		playerpos=[50,200]
		arrows=[]
		direc=[0,0]
		speed=1
		bulletspeed=500
		wallwide=30
		wallheight=30
		ANT_COUNT=20
		tm_path=[]
		pathlist=[]
		badtimer=100
		badtimer1=0
		badguys=[]
		constimer=8
		tankspeed=300
		global tm
		global test_map
		#3 Load 
		gameover = pygame.image.load("img/gameover.png")
		youwin = pygame.image.load("img/youwin.png")
		p1tankD=pygame.image.load("img/p1tankD.png")
		p1tankL=pygame.image.load("img/p1tankL.png")
		p1tankR=pygame.image.load("img/p1tankR.png")
		p1tankU=pygame.image.load("img/p1tankU.png")
		p1tank=p1tankU
		enemyimg=pygame.image.load("img/p2tankD.png")
		# print pygame.image.tostring(p1tank)
		wall=pygame.image.load("img/wall/wall.png")
		walls=pygame.image.load("img/wall/walls.png")
		ant_image = pygame.image.load("img/p1tankD.png").convert_alpha()
		# leaf_image = pygame.image.load("leaf.png").convert_alpha()
		# spider_image = pygame.image.load("spider.png").convert_alpha()
		bulletimg=pygame.image.load("img/tankmissile.png")
		hit=pygame.mixer.Sound("img/hit.wav")
		fire=pygame.mixer.Sound("img/fire.wav")
		start=pygame.mixer.Sound("img/start.wav")

		#地图 （在这里可编辑地图，#代表墙） 
		tm = [  
		'......................',  
		'......................',  
		'......................',  
		'......................',  
		'........########......',  
		'........#.............',  
		'........#.............',  
		'......................',  
		'......................',  
		'......................',  
		'......................',  
		'......................',  
		'......................',  
		'..###########........#',
		'......................',
		'......................',
		'.....................#',
		'......................',
		'......................',
		'.....................#',
		'.....................#',
		'.....................#',
		'.....................#',]  
		  
		#因为python里string不能直接改变某一元素，所以用test_map来存储搜索时的地图  
		test_map = []  
		  
		######################################################### 
		class Node_Elem:  
		    """ 
		    开放列表和关闭列表的元素类型，parent用来在成功的时候回溯路径 
		    """  
		    def __init__(self, parent, x, y, dist):  
		        self.parent = parent  
		        self.x = x  
		        self.y = y  
		        self.dist = dist  
		          
		class A_Star:  
		    """ 
		    A星算法实现类 
		    """  
		    #注意w,h两个参数，如果你修改了地图，需要传入一个正确值或者修改这里的默认参数  
		    def __init__(self, s_x, s_y, e_x, e_y, w=22, h=23):  
		        self.s_x = s_x  
		        self.s_y = s_y  
		        self.e_x = e_x  
		        self.e_y = e_y  
		        self.width = w  
		        self.height = h  
		        self.open = []  
		        self.close = []  
		        self.path = []  
		          
		    #查找路径的入口函数  
		    def find_path(self):  
		        #构建开始节点  
		        p = Node_Elem(None, self.s_x, self.s_y, 0.0)  
		        while True:  
		            #扩展F值最小的节点  
		            self.extend_round(p)  
		            #如果开放列表为空，则不存在路径，返回  
		            if not self.open:  
		                return  
		            #获取F值最小的节点  
		            idx, p = self.get_best()  
		            #找到路径，生成路径，返回  
		            if self.is_target(p):  
		                return  self.make_path(p)
		            #把此节点压入关闭列表，并从开放列表里删除  
		            self.close.append(p)  
		            del self.open[idx]  
		              
		    def make_path(self,p):  
		        #从结束点回溯到开始点，开始点的parent == None  
		        while p:  
		            self.path.append((p.x, p.y))  
		            p = p.parent 
		        return self.path
		    def is_target(self, i):  
		        return i.x == self.e_x and i.y == self.e_y  
		    def get_best(self):  
		        best = None  
		        bv = 1000000 #如果你修改的地图很大，可能需要修改这个值  
		        bi = -1  
		        for idx, i in enumerate(self.open):  
		            value = self.get_dist(i)#获取F值  
		            if value < bv:#比以前的更好，即F值更小  
		                best = i  
		                bv = value  
		                bi = idx  
		        return bi, best  
		          
		    def get_dist(self, i):  
		        # F = G + H  
		        # G 为已经走过的路径长度， H为估计还要走多远  
		        # 这个公式就是A*算法的精华了。  
		        return i.dist + math.sqrt(  
		            (self.e_x-i.x)*(self.e_x-i.x)  
		            + (self.e_y-i.y)*(self.e_y-i.y))*1.2  
		          
		    def extend_round(self, p):  
		        #可以从8个方向走  
		        # xs = (-1, 0, 1, -1, 1, -1, 0, 1)  
		        # ys = (-1,-1,-1,  0, 0,  1, 1, 1)  
		        # 只能走上下左右四个方向  
		        xs = (0, -1, 1, 0)  
		        ys = (-1, 0, 0, 1)  
		        for x, y in zip(xs, ys):  
		            new_x, new_y = x + p.x, y + p.y  
		            #无效或者不可行走区域，则勿略  
		            if not self.is_valid_coord(new_x, new_y):  
		                continue  
		            #构造新的节点  
		            node = Node_Elem(p, new_x, new_y, p.dist+self.get_cost(  
		                        p.x, p.y, new_x, new_y))  
		            #新节点在关闭列表，则忽略  
		            if self.node_in_close(node):  
		                continue  
		            i = self.node_in_open(node)  
		            if i != -1:  
		                #新节点在开放列表  
		                if self.open[i].dist > node.dist:  
		                    #现在的路径到比以前到这个节点的路径更好~  
		                    #则使用现在的路径  
		                    self.open[i].parent = p  
		                    self.open[i].dist = node.dist  
		                continue  
		            self.open.append(node)  
		              
		    def get_cost(self, x1, y1, x2, y2):  
		        """ 
		        上下左右直走，代价为1.0，斜走，代价为1.4 
		        """  
		        if x1 == x2 or y1 == y2:  
		            return 1.0  
		        return 1.4  
		          
		    def node_in_close(self, node):  
		        for i in self.close:  
		            if node.x == i.x and node.y == i.y:  
		                return True  
		        return False  
		          
		    def node_in_open(self, node):  
		        for i, n in enumerate(self.open):  
		            if node.x == n.x and node.y == n.y:  
		                return i  
		        return -1  
		          
		    def is_valid_coord(self, x, y):  
		        if x < 0 or x >= self.width or y < 0 or y >= self.height:  
		            return False  
		        return test_map[y][x] != '#'  
		      
		    def get_searched(self):  
		        l = []  
		        for i in self.open:  
		            l.append((i.x, i.y))  
		        for i in self.close:  
		            l.append((i.x, i.y))  
		        return l  
		#########################################################  
		def print_test_map():  
		    global test_map
		    """ 
		    打印搜索后的地图 
		    """  
		    for line in test_map:  
		        print ''.join(line)  
		  
		def get_start_XY():  
		    return get_symbol_XY('S')  
		      
		def get_end_XY():  
		    return get_symbol_XY('E')      
		def get_symbol_XY(s): 
		    global test_map
		    # print test_map
		    for y, line in enumerate(test_map):  
		        try:  
		            x = line.index(s)  
		        except:  
		            continue  
		        else:  
		            break  
		    # print x,y
		    return x, y  
		def clear_symbol(s):
			global tm
			x,y=get_symbol_XY(s)
			print x,y
			l=list(tm[y])
			l[x]='.'
			tm[y]=''
			tm[y]=''.join(l)
		def draw_a_symbol(playerpos,s):
			global tm
			l=list(tm[int(playerpos[1]/wallheight)])
			l[int(playerpos[0]/wallwide)]=s
			tm[int(playerpos[1]/wallheight)]=''
			tm[int(playerpos[1]/wallheight)]=''.join(l)
		def get_symbol_XY_list(s):
		    global test_map
		    list2=[]  
		    for y, line in enumerate(test_map):
		        for x in range(len(line)):
		            if line[x]==s:
		        	     list2.append([x,y])

		    return list2            
		def mark_path(l):  
		    mark_symbol(l, '*')  
		      
		def mark_searched(l):  
		    mark_symbol(l, ' ')  
		      
		def mark_symbol(l, s):  
		    global test_map
		    for x, y in l:  
		        test_map[y][x] = s  
		      
		def mark_start_end(s_x, s_y, e_x, e_y):  
		    global test_map
		    test_map[s_y][s_x] = 'S'  
		    test_map[e_y][e_x] = 'E'  
		      
		def tm_to_test_map(tm1):  
		    global test_map
		    for line in tm:  
		        test_map.append(list(line))  
		def tm_to_clear_map():
		    global test_map
		    test_map=[]
		          
		def find_path():  
		    s_x, s_y = get_start_XY()  
		    e_x, e_y = get_end_XY()  
		    a_star = A_Star(s_x, s_y, e_x, e_y)  
		    tankpath=a_star.find_path() 
		    searched = a_star.get_searched()  
		    path = a_star.path 
		    #标记已搜索区域  
		    mark_searched(searched)  
		    #标记路径  
		    mark_path(path)  
		    print "path length is %d"%(len(path))  
		    print "searched squares count is %d"%(len(searched))  
		    #标记开始、结束点  
		    mark_start_end(s_x, s_y, e_x, e_y) 
		    return tankpath 
		class tank:
			def __init__(self):
				self.direction1=[0,-1]
			# def ismove(self):
			def changedirection(self,num):
				self.direction1=num
			def direction(self):
				return self.direction1
			def outside0(self,playerpos):
				if playerpos[1]<0:
						return False
				return True
			def outside1(self,playerpos):
				if playerpos[1]>height-60:
					return False
				return True
			def outside2(self,playerpos):
				if playerpos[0]<0:
					return False
				return True
			def outside3(self,playerpos):
				if playerpos[0]>width-60:
					return False
				return True
			def mark_tank(self,s):
				global tm
				global playerpos
				l=list(tm[int(playerpos[1]/wallwide)])
				l[int(playerpos[0]/wallheight)]=s
				tm[int(playerpos[1]/wallwide)]=''
				tm[int(playerpos[1]/wallwide)]=''.join(l)
		def bump_into_wall(walllist,playerpos,p1tank,d):
			for i in walllist:
				wallrect=pygame.Rect(wall.get_rect())
				wallrect.top=i[1]
				wallrect.left=i[0]
				tankrect=pygame.Rect(p1tank.get_rect())
				tankrect.left=playerpos[0]
				tankrect.top=playerpos[1]
				if wallrect.colliderect(tankrect):
					if d==0 and p1tank==p1tankU:
						return False
					if d==2 and p1tank==p1tankD:
						return False
					if d==1 and p1tank==p1tankL:
						return False
					if d==3 and p1tank==p1tankR:
						return False
			return True
		class enemy():
			def __init__(self,tank_pos,tank_dir,path,img):
				self.x=tank_pos[0]
				self.y=tank_pos[1]
				self.dir=tank_dir
				self.path=path
				self.img=img
			def find_shoot(self,t):
				isdirection=[0,0]
				global playerpos
				isdirection[0]=int(playerpos[0]/wallwide)
				isdirection[1]=int(playerpos[1]/wallheight)
				AB=Vector2.from_points((self.x,self.y),(isdirection[0],isdirection[1]))
				if (isdirection[0]-self.x+1)*(isdirection[1]-self.y+1)!=1:
					if (isdirection[0]==self.x or isdirection[1]==self.y) and AB.get_normalized()==self.dir:
						if t>0:
							# print 1
							self.shoot_tank()
			def shoot_tank(self):
				global arrows
				arrows.append([self.x*wallwide+20+40*self.dir[0],self.y*wallheight+20+40*self.dir[1],self.dir])
			def change_enemy_dir(self,direction):
				x=direction[0]-self.dir[0]
				y=direction[1]-self.dir[1]
				if x*y==0:
					degree=x*90+y*90
				elif (direction==(0,1) and self.dir==(1,0)) or (direction==(0,-1) and self.dir==(-1,0)) or (direction==(-1,0) and self.dir==(0,1)) or (direction==(1,0) and self.dir==(0,-1)):
					degree=-90
				else:
					degree=90
				self.img=pygame.transform.rotate(self.img,degree)
				self.dir=direction
				# print self.dir
			def get_enemy_position(self):
				return (self.x,self.y)
			def follow_the_path(self):
				global pathlist
				global playerpos
				global tm
				self.x=pathlist[-1][0]
				self.y=pathlist[-1][1]
				del pathlist[-1]
				print pathlist
				if pathlist:
					direction=(-1*self.x+pathlist[-1][0],-1*self.y+pathlist[-1][1])
					self.change_enemy_dir(direction)
			def draw_the_tank(self):
				screen.blit(self.img,(self.x*wallwide,self.y*wallheight))
				pygame.display.update()
			def get_enemy_img(self):
				return self.img
			def get_enemy_pos(self):
				return [self.x,self.y]
			def get_enemy_dir(self):
				return self.dir
			# def delete_enemy():

		#4
		tank=tank()
		tm_to_test_map(tm)   
		walllist=get_symbol_XY_list('#')
		for i in walllist:
			i[0]=i[0]*wallwide
			i[1]=i[1]*wallheight
		clockbutton=pygame.time.Clock()
		clockbullet=pygame.time.Clock()
		clockfps=pygame.time.Clock()
		badguys.append([random.randint(50,600), 0])
		index=0
		#搜索地图 画墙 找寻轨迹
		for badguy in badguys:
			start=(badguy[0]/wallwide,badguy[1]/wallheight)
			l=list(tm[start[1]])
			l[start[0]],x1='S',l[start[0]]
			tm[start[1]]=''
			tm[start[1]]=''.join(l)
			tm_to_clear_map()
			tank.mark_tank('E')
			tm_to_test_map(tm)   
			pathlist=find_path() 
			index+=1
			l=list(tm[start[1]])
			l[start[0]]=x1
			tm[start[1]]=''.join(l)
		enemytank=enemy(pathlist[-1],(0,1),pathlist,enemyimg)
		running = 1
		exitcode = 0
		t=time.clock()
		timer=constimer
		while running:
			#如果坦克到达目的地 则重新开始搜索
			if pathlist:
				if timer==0:
					enemytank.follow_the_path()
					timer=constimer
					#敌方坦克每隔一定时间发射炮弹
				if time.clock()-t>0.2:
					enemytank.find_shoot(t)
					t=time.clock()
				enemytank.draw_the_tank()
			else:
				clear_symbol('S')
				clear_symbol('E')
				print tm
				start=(enemytank.get_enemy_pos()[0],enemytank.get_enemy_pos()[1])
				l=list(tm[start[1]])
				l[start[0]]='S'
				tm[start[1]]=''
				tm[start[1]]=''.join(l)
				print tm
				tank.mark_tank('E')
				pathlist=[]
				print tm
				tm_to_clear_map()
				tm_to_test_map(tm)
				print tm   
				pathlist=find_path()
				enemypos1=enemytank.get_enemy_pos()
				enemydir1=enemytank.get_enemy_dir()
				enemyimg1=enemytank.get_enemy_img()
				enemytank=enemy(enemypos1,enemydir1,pathlist,enemyimg1)
				print pathlist
				print 100  
			timer-=1
			badtimer-=1
			screen.fill(0)
			screen.blit(p1tank,playerpos)
			playerheart=[playerpos[0]+20,playerpos[1]+20]
			clockfps.tick(30)
			time_pass=clockbullet.tick()
			time_pass_seconds=time_pass/1000.0
			distanced_moved=time_pass_seconds*bulletspeed
			tank_moved=time_pass_seconds*tankspeed
			for bullet in arrows:
				index=0
				bullet[0]+=distanced_moved*bullet[2][0]
				bullet[1]+=distanced_moved*bullet[2][1]
				if bullet[0]<0 or bullet[0]>640 or bullet[1]<0 or bullet[1]>640:
					arrows.pop(index)
				index+=1
				for projectile in arrows:
					screen.blit(bulletimg,(projectile[0],projectile[1]))
			index=0
			for i in walllist:
				wallrect=pygame.Rect(wall.get_rect())
				wallrect.top=i[1]
				wallrect.left=i[0]
				playerrec=pygame.Rect(p1tank.get_rect())
				playerrec.left=playerpos[0]
				playerrec.top=playerpos[1]
				enemyrect=pygame.Rect(enemytank.get_enemy_img().get_rect())
				enemyrect.left=enemytank.get_enemy_pos()[0]*wallwide
				enemyrect.top=enemytank.get_enemy_pos()[1]*wallheight
				#6.3.2 - Check for collisions
				index1=0
				for bullet in arrows:
					bullrect=pygame.Rect(bulletimg.get_rect())
					bullrect.left=bullet[0]
					bullrect.top=bullet[1]
					if wallrect.colliderect(bullrect):
						hit.play()
						walllist.pop(index)
						arrows.pop(index1)
					if playerrec.colliderect(bullrect) or playerrec.colliderect(enemyrect):
						running=0
						exitcode=0
					if enemyrect.colliderect(bullrect):
						arrows.pop(index1)
						running=0
						exitcode=1
						print 1
					index1+=1
				index+=1
			for i in walllist:
				screen.blit(wall,(i[0],i[1]))
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					exit(0)
				#判断按键操作 
				if event.type == pygame.KEYDOWN:
					if event.key==K_w:
						keys[0]=True
					elif event.key==K_a:
						keys[1]=True
					elif event.key==K_s:
						keys[2]=True
					elif event.key==K_d:
						keys[3]=True
					elif event.key==K_j:
						if clockbutton.tick()>=500:
							direc=tank.direction()
							arrows.append([playerpos[0]+20+40*direc[0],playerpos[1]+20+40*direc[1],direc])
							fire.play()
						else:
							continue	
				if event.type == pygame.KEYUP:
					if event.key==pygame.K_w:
						keys[0]=False
					elif event.key==pygame.K_a:
						keys[1]=False
					elif event.key==pygame.K_s:
						keys[2]=False
					elif event.key==pygame.K_d:
						keys[3]=False
			if keys[0] and tank.outside0(playerpos) and bump_into_wall(walllist,playerpos,p1tank,0):
				playerpos[1]-=tank_moved
				p1tank=p1tankU
				tank.changedirection([0,-1])
			elif keys[2]and tank.outside1(playerpos)and bump_into_wall(walllist,playerpos,p1tank,2):
				playerpos[1]+=tank_moved	
				p1tank=p1tankD
				tank.changedirection([0,1])
			elif keys[1] and tank.outside2(playerpos)and bump_into_wall(walllist,playerpos,p1tank,1):
				playerpos[0]-=tank_moved
				p1tank=p1tankL
				tank.changedirection([-1,0])
			elif keys[3] and tank.outside3(playerpos)and bump_into_wall(walllist,playerpos,p1tank,3):
				playerpos[0]+=tank_moved
				p1tank=p1tankR
				tank.changedirection([1,0])
			pygame.display.update()
			#结果画面输出
		if exitcode==0:
		    pygame.font.init()
		    font = pygame.font.Font(None, 24)
		    screen.blit(gameover, (0,0))
		elif exitcode==1:
		    pygame.font.init()
		    font = pygame.font.Font(None, 24)
		    screen.blit(youwin, (0,0))
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
			pygame.display.flip()
	
