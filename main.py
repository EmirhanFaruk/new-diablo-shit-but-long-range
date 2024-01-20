
# Modification date: Mon Jul 25 18:56:08 2022

# Production date: Sun Sep  3 15:43:50 2023

import pygame
from random import randint, choice, uniform
from math import sqrt, atan, cos, sin

#Haritaya sınır koy
#Düşmanlar dışarıdan gelsin
#Market/Dalga sistemi
#Değişik silahlar
#Patlayıcılar(?)
#Farklı düşmanlar
#TAM EKRAN İÇİN DEĞİŞİKLİKLER LAZIM!!!




ww = 600
wh = 600
win = pygame.display.set_mode((ww, wh))
pygame.init()

eshot = pygame.mixer.Sound("eshot.wav")
emgshot = pygame.mixer.Sound("emgshot.wav")
pshot = pygame.mixer.Sound("pshot.wav")
cannon_shot = pygame.mixer.Sound("cannon_shot.wav")
shell_explosion = pygame.mixer.Sound("shell_explosion.wav")
explosion_list = [pygame.mixer.Sound("explode1.wav"), pygame.mixer.Sound("explode2.wav"), pygame.mixer.Sound("explode3.wav")]
#explosion_list = [pygame.mixer.Sound("boom.wav")]
music = pygame.mixer.Sound("music.mp3")
music.set_volume(20)
music.play(-1)
pygame.mixer.set_num_channels(10000)


class MiniMap:
    def __init__(self, x, y, w, h, colour, colour2):
        self.x, self.y, self.w, self.h, self.colour, self.colour2 = x, y, w, h, colour, colour2
    def get_coordinates_and_scale(self, wall, target):#300
        if target.x < wall.x + wall.w and target.x > wall.x + 300 and target.y < wall.y + wall.w and target.y > wall.y + 300:
            the_x = abs(target.x - (wall.x + 300))
            the_y = abs(target.y - (wall.y + 300))
        else:
            return (-2, -2)
        """
        walls.append(Wall(player.x - 1000, player.y - 1000, 2000, 300, (139,69,19)))#top wall
        walls.append(Wall(player.x - 1000, player.y - 1000, 300, 2000, (139,69,19)))#west wall
        walls.append(Wall(player.x + 1000, player.y - 1000, 300, 2300, (139,69,19)))#east wall
        walls.append(Wall(player.x - 1000, player.y + 1000, 2300, 300, (139,69,19)))#bottom wall
        """
        return (the_x/18, the_y/18)
        
        
        
        
    def draw(self, win, player, enemies, the_upper_wall):
        pygame.draw.rect(win, self.colour, pygame.Rect(self.x + 1, self.y + 1, self.w - 2, self.h - 2))
        for enemy in enemies:
            coords = self.get_coordinates_and_scale(the_upper_wall, enemy)
            if coords[0] + 0.5 > 0 and coords[0] + 0.5 < self.w and coords[1] + 0.5 > 0 and coords[1] + 0.5 < self.h:
                pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x + coords[0] + 0.5, self.y + coords[1] + 0.5, 3, 3))
        coords = self.get_coordinates_and_scale(the_upper_wall, player)
        pygame.draw.rect(win, (0, 0, 255), pygame.Rect(self.x + coords[0] + 0.5, self.y + coords[1] + 0.5, 3, 3))
        pygame.draw.rect(win, self.colour2, pygame.Rect(self.x, self.y, self.w, self.h), 2)

class Hud:
    def __init__(self, x, y, w, h, colour, colour2):
        self.x, self.y, self.w, self.h, self.colour, self.colour2 = x, y, w, h, colour, colour2
        self.hud_texts = []
        self.hud_map = MiniMap(self.x + 250, self.y, 100, 100, (30, 110, 70), (0, 80, 40))

    def draw(self, win, texts, player, enemies, the_upper_wall):
        pygame.draw.rect(win, self.colour, pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(win, self.colour2, pygame.Rect(self.x, self.y, self.w, self.h), 2)
        for element in self.hud_texts:
            element.draw(win, texts)
        self.hud_map.draw(win, player, enemies, the_upper_wall)
        


class Blood:
    def __init__(self, x, y, r, colour, duration):
        self.x, self.y, self.r, self.colour, self.duration = x, y, r, colour, duration

    def draw(self, win, bloods):
        if self.duration == 0:
            bloods.remove(self)
            return
        self.duration -= 1
        pygame.draw.circle(win, self.colour, (self.x, self.y), self.r)
        

class Text:
    def __init__(self, x, y, text, size, colour, duration, variable, speed = 0):
        self.x, self.y, self.size, self.colour, self.duration, self.speed = x, y, size, colour, duration, speed
        self.text = text
        self.variable = variable
        self.font = pygame.font.SysFont('Comic Sans MS', self.size)
        self.text_surface = self.font.render(self.text, False, self.colour)
        self.text_width = self.text_surface.get_width()

    def draw(self, win, texts):
        if self.duration == 0:
            texts.remove(self)
        if self.duration != -1:
            self.duration -= 1
        self.text_surface = self.font.render(self.text + str(self.variable), False, self.colour)
        self.text_width = self.text_surface.get_width()
        win.blit(self.text_surface, (self.x - self.text_width/2, self.y))
        self.y -= self.speed
        return

class Magic:
    def __init__(self, x, y, r, target, source, damage):
        self.x, self.y, self.r, self.source, self.damage, self.target = x, y, r, source, damage, target
        self.counting = 0
        self.r_counting = -9
        self.exp_s = choice([pygame.mixer.Sound("explode1.wav"), pygame.mixer.Sound("explode2.wav"), pygame.mixer.Sound("explode3.wav")])
    def distance(self, target):
        return sqrt((target.x - self.x)**2 + (target.y - self.y)**2)
    def draw_mark(self, win):
        if self.counting < 100:
            self.counting += 1
            pygame.draw.line(win, (210, 0, 210), (self.source.x, self.source.y), (uniform(self.x - 10, self.x + 10), uniform(self.y - 10, self.y + 10)))
            pygame.draw.line(win, (215, 0, 215), (self.source.x, self.source.y), (uniform(self.x - 10, self.x + 10), uniform(self.y - 10, self.y + 10)))
            pygame.draw.line(win, (220, 0, 220), (self.source.x, self.source.y), (uniform(self.x - 10, self.x + 10), uniform(self.y - 10, self.y + 10)))
            pygame.draw.line(win, (200, 0, 200), (self.source.x, self.source.y), (self.x, self.y))
            pygame.draw.circle(win, (self.counting * 2, 0, self.counting * 2), (self.x, self.y), 10)
            if self.counting % 5 == 0:
                pygame.draw.circle(win, (150, 0, 0), (self.x, self.y), self.r, 2)
            else:
                pygame.draw.circle(win, (150, 0, 150), (self.x, self.y), self.r, 2)

    def draw_blast(self, win, magics, player):
        if self.source.hp <= 0 and self in magics:
            magics.remove(self)
        if self.counting >= 100 and self.counting < 120:
            if self.counting == 100:
                if self.distance(player) > 0:
                    self.exp_s.set_volume(150/self.distance(player))
                else:
                    self.exp_s.set_volume(150)
                pygame.mixer.find_channel().play(self.exp_s)

            
            self.counting += 1
            if self.r_counting > 0:
                self.r -=  self.r_counting
            self.r_counting += 1
            pygame.draw.circle(win, (100 + 5 * (self.counting%100), 200 - 10 * (self.counting%100), 0), (self.x, self.y), self.r)
            #pygame.draw.circle(win, (200 - 5 * (self.counting%100), 0, 100 + 5 * (self.counting%100)), (self.x, self.y), self.r)
            if self.distance(player) < self.r + player.r:
                player.hp -= self.damage
                if player.hp <= 0:
                    player.hp = 0
                    player.alive = False
        if self.counting >= 120 and self in magics:
            magics.remove(self)

class Big_Black_Nigga_Balls_HD:
    def __init__(self, x, y, vels, damage, bulletvel):
        self.x, self.y, self.vels = x, y, vels
        self.r = 12
        self.damage = damage
        self.counting = 0
        self.limit = 240
        self.detonation_time = randint(1, 30)
        self.start_det = False
        self.bulletvel = bulletvel
        self.exist = True
        self.explosion_sound = pygame.mixer.Sound("shell_explosion.wav")
        #equation --> y = am + b
        the = False
        if self.vels[0] == 0:
            self.vels[0] = 0.1
            the = True
        self.m = self.vels[1]/self.vels[0]
        if the:
            self.vels[0] = 0
        self.b = self.y - self.x * self.m 

    def distance_of_2(self, x1, y1, x2, y2):
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)
    def distance(self, target):
        return sqrt((target.x - self.x)**2 + (target.y - self.y)**2)
    def distancexy(self, x, y):
        return sqrt((x - self.x)**2 + (y - self.y)**2)
    def old_distance(self, target):
        return sqrt((target.x - (self.x - self.vels[0]))**2 + (target.y - (self.y - self.vels[1]))**2)

    def detect_intersection_rectangle(self, target, cases):
        for droite in target.droites:
            if droite[0] != self.m and not any(cases):
                point_dintersection_x = (droite[1] - self.b) / (self.m - droite[0])
                point_dintersection_y = point_dintersection_x * droite[0] + droite[1]
                if ((point_dintersection_x >= droite[3][0] or point_dintersection_x <= droite[2][0]) or (point_dintersection_x <= droite[3][0] or point_dintersection_x >= droite[2][0])):
                    if ((point_dintersection_y >= droite[3][1] or point_dintersection_y <= droite[2][1]) or (point_dintersection_y <= droite[3][1] or point_dintersection_y >= droite[2][1])):
                        if point_dintersection_x >= target.x - 1 and point_dintersection_x <= target.x + target.w + 1 and point_dintersection_y >= target.y - 1 and point_dintersection_y <= target.y + target.h + 1:
                            if self.distancexy(point_dintersection_x, point_dintersection_y) < self.bulletvel:
                                if (self.vels[0] >= 0 and self.x <= point_dintersection_x) or (self.vels[0] <= 0 and self.x >= point_dintersection_x):#checking x vels etc to prevent "backshooting"
                                    if (self.vels[1] >= 0 and self.y <= point_dintersection_y) or (self.vels[1] <= 0 and self.y >= point_dintersection_y):#checking y vels etc to prevent "backshooting"
                                        cases.append(True)
                                        return cases, (point_dintersection_x, point_dintersection_y), self.distancexy(point_dintersection_x, point_dintersection_y)
        return cases, (-100, -100), 99999
    def toucher(self, player, balls, walls):
        if self.detonation_time > 0:
            #equation --> y = am + b
            the = False
            if self.vels[0] == 0:
                self.vels[0] = 0.000001
                the = True
            self.m = self.vels[1]/self.vels[0]
            if the:
                self.vels[0] = 0
            self.b = self.y - self.x * self.m
            
            self.counting += 1
            if self.limit < self.counting:
                balls.remove(self)
                self.exist = False
                return
            wall_i_list = []
            wall_pd_list = []
            wall_cases = []
            for wall in walls:
                wall_cases, new_pd, new_i = self.detect_intersection_rectangle(wall, wall_cases)
                wall_i_list.append(new_i)
                wall_pd_list.append(new_pd)
            wall_min_i = min(wall_i_list) 
            wall_min_pd = wall_pd_list[wall_i_list.index(wall_min_i)]
            if self.distance(player) < self.r + player.r + 64:
                self.start_det = True
            if self.start_det and self.detonation_time > 0:
                self.detonation_time -= 1
            if any(wall_cases):
                pygame.draw.circle(win, (255, 255, 0), wall_min_pd, self.r + 2)
                balls.remove(self)
                self.exist = False
                return
        elif self.detonation_time < -10:
            balls.remove(self)
            self.exist = False
            return
    def explode(self, win, player):
        if self.detonation_time == 0:
            if self.distance(player) != 1:
                self.explosion_sound.set_volume(30/self.distance(player))
                pygame.mixer.find_channel().play(self.explosion_sound)
            else:
                self.explosion_sound.set_volume(10)
                pygame.mixer.find_channel().play(self.explosion_sound)
        if self.detonation_time <= 0:
            if self.distance(player) < self.r + player.r + abs(self.detonation_time) * 2:
                player.hp -= self.damage
                if player.hp <= 0:
                    player.alive = False
            self.detonation_time -= 1
    def avancer(self):
        if self.detonation_time > 0:
            self.x += self.vels[0]
            self.y += self.vels[1]

    def draw(self, win):
        if self.detonation_time <= 0:
            pygame.draw.circle(win, (100 + abs(self.detonation_time) * 10, 255 - abs(self.detonation_time) * 10, 0), (self.x, self.y), self.r + abs(self.detonation_time) * 2)
        else:
            pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.r)

class Bullet:
    def __init__(self, x, y, vels, source, damage, count, bulletvel):
        self.x, self.y, self.vels = x, y, vels
        self.r = 2
        self.source = source
        self.damage = damage
        self.counting = 0
        self.limit = 240
        self.number = count
        self.bulletvel = bulletvel
        self.exist = True
        #equation --> y = am + b
        the = False
        if self.vels[0] == 0:
            self.vels[0] = 0.1
            the = True
        self.m = self.vels[1]/self.vels[0]
        if the:
            self.vels[0] = 0
        self.b = self.y - self.x * self.m 

    def distance_of_2(self, x1, y1, x2, y2):
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)
    def distance(self, target):
        return sqrt((target.x - self.x)**2 + (target.y - self.y)**2)
    def distancexy(self, x, y):
        return sqrt((x - self.x)**2 + (y - self.y)**2)
    def old_distance(self, target):
        return sqrt((target.x - (self.x - self.vels[0]))**2 + (target.y - (self.y - self.vels[1]))**2)

    def detect_intersection_round(self, target, tx, ty, tr, tm, tb, cases):
        if self.distance(target) < sqrt(self.vels[0]**2 + self.vels[1]**2) and not any(cases):
            if tm != self.m and not any(cases):
                point_dintersection_x = (tb - self.b) / (self.m - tm)
                point_dintersection_y = point_dintersection_x * tm + tb
                if sqrt((point_dintersection_x - tx)**2 + (point_dintersection_y - ty)**2) < tr:
                    if (self.vels[0] >= 0 and self.x <= point_dintersection_x) or (self.vels[0] <= 0 and self.x >= point_dintersection_x):#checking x vels etc to prevent "backshooting"
                        if (self.vels[1] >= 0 and self.y <= point_dintersection_y) or (self.vels[1] <= 0 and self.y >= point_dintersection_y):#checking y vels etc to prevent "backshooting"
                            cases.append(True)
                            return cases, (point_dintersection_x, point_dintersection_y), self.distancexy(point_dintersection_x, point_dintersection_y)
        return cases, (-100, -100), 99999
    def detect_intersection_rectangle(self, target, cases):
        for droite in target.droites:
            if droite[0] != self.m and not any(cases):
                point_dintersection_x = (droite[1] - self.b) / (self.m - droite[0])
                point_dintersection_y = point_dintersection_x * droite[0] + droite[1]
                if ((point_dintersection_x >= droite[3][0] or point_dintersection_x <= droite[2][0]) or (point_dintersection_x <= droite[3][0] or point_dintersection_x >= droite[2][0])):
                    if ((point_dintersection_y >= droite[3][1] or point_dintersection_y <= droite[2][1]) or (point_dintersection_y <= droite[3][1] or point_dintersection_y >= droite[2][1])):
                        if point_dintersection_x >= target.x - 1 and point_dintersection_x <= target.x + target.w + 1 and point_dintersection_y >= target.y - 1 and point_dintersection_y <= target.y + target.h + 1:
                            if self.distancexy(point_dintersection_x, point_dintersection_y) < self.bulletvel:
                                if (self.vels[0] >= 0 and self.x <= point_dintersection_x) or (self.vels[0] <= 0 and self.x >= point_dintersection_x):#checking x vels etc to prevent "backshooting"
                                    if (self.vels[1] >= 0 and self.y <= point_dintersection_y) or (self.vels[1] <= 0 and self.y >= point_dintersection_y):#checking y vels etc to prevent "backshooting"
                                        cases.append(True)
                                        return cases, (point_dintersection_x, point_dintersection_y), self.distancexy(point_dintersection_x, point_dintersection_y)
        return cases, (-100, -100), 99999
    def toucher(self, enemies, player, bullets, texts, walls, bloods, death_text):
        #equation --> y = am + b
        the = False
        if self.vels[0] == 0:
            self.vels[0] = 0.000001
            the = True
        self.m = self.vels[1]/self.vels[0]
        if the:
            self.vels[0] = 0
        self.b = self.y - self.x * self.m
        
        self.counting += 1
        if self.limit < self.counting:
            bullets.remove(self)
            return
        wall_i_list = []
        wall_pd_list = []
        wall_cases = []
        for wall in walls:
            wall_cases, new_pd, new_i = self.detect_intersection_rectangle(wall, wall_cases)
            wall_i_list.append(new_i)
            wall_pd_list.append(new_pd)
        wall_min_i = min(wall_i_list) 
        wall_min_pd = wall_pd_list[wall_i_list.index(wall_min_i)]
        if self.source == "player":
            enemy_list = []
            for enemy in enemies:
                cases = [self.distance(enemy) < self.r + enemy.r, self.old_distance(enemy) < self.r + enemy.r]
                cases, pd1, i1 = self.detect_intersection_round(enemy, enemy.x, enemy.y, enemy.r, enemy.mh, enemy.bh, cases)
                cases, pd2, i2 = self.detect_intersection_round(enemy, enemy.x, enemy.y, enemy.r, enemy.mv, enemy.bv, cases)
                if i1 < i2:
                    le_i = i1
                    le_pd = pd1
                else:
                    le_i = i2
                    le_pd = pd2
                
                if any(cases):
                    enemy_list.append([enemy, self.old_distance(enemy)])
            if len(enemy_list) > 0:
                closest = 0
                for index in range(len(enemy_list)):
                    if self.old_distance(enemy_list[closest][0]) > self.old_distance(enemy_list[index][0]):
                        closest = index
                enemy = enemy_list[closest][0]
                if enemy:#i did this bc i hate to untab in the default editor
                    if wall_min_i < le_i:
                        pygame.draw.circle(win, (255, 255, 0), wall_min_pd, self.r)
                        bullets.remove(self)
                        return
                    enemy.bleed_time = 300
                    if self.distance_of_2(enemy.x, enemy.y, pd1[0], pd1[1]) < enemy.r:
                        bloods.append(Blood(pd1[0], pd1[1], randint(1, 3), (200, 50, 10), 300))
                    elif self.distance_of_2(enemy.x, enemy.y, pd2[0], pd2[1]) < enemy.r:
                        bloods.append(Blood(pd2[0], pd2[1], randint(1, 3), (200, 50, 10), 300))
                    else:
                        bloods.append(Blood(randint(int(enemy.x - enemy.r), int(enemy.x + enemy.r)), randint(int(enemy.y - enemy.r), int(enemy.y + enemy.r)), randint(1, 3), (200, 50, 10), 300))
                    while self.number > 0 and enemy.hp > 0:
                        self.number -= 1
                        enemy.hp -= self.damage
                        if enemy.hp <= 0:
                            texts.append(Text(randint(int(enemy.x - enemy.r * 2), int(enemy.x + enemy.r * 2)), randint(int(enemy.y - enemy.r * 2), int(enemy.y + enemy.r * 2)), "-" + str(self.damage), 10, (255, 50, 50), 30, "", 0.3))
                            break
                        else:
                            texts.append(Text(randint(int(enemy.x - enemy.r * 2), int(enemy.x + enemy.r * 2)), randint(int(enemy.y - enemy.r * 2), int(enemy.y + enemy.r * 2)), "-" + str(self.damage), 10, (255, 100, 100), 30, "", 0.3))
                    if enemy.hp <= 0:
                        enemies.remove(enemy)
                        player.hp += 1
                        player.kk += 1
                        death_text.variable, kill_text.variable = player.kk, player.kk
                        print(f"\n--------------------------\nKilled {player.kk} enemies\n-Health = {player.hp}\n-Bullet count = {player.bc}\n-Speed = {player.vel}\n-Shooting speed = 1 bullet per {player.bulletcooldown} frame(s)\n-Bullet velocity = {player.bulletvel}\n-Bullet damage multiplier = {player.bulletdmgmultiplier}")
                        chosen = False
                        da_while_blocker = 0
                        colour = (50, 255, 50)
                        if randint(1, 5) == 2:
                            while not chosen and da_while_blocker < 10:
                                dab = choice(["+max health", "+health", "+1 extra bullet", "+speed", "+shooting speed", "+bullet velocity", "+damage multiplier"])
                                da_while_blocker += 1
                                if dab == "+max health":
                                    if player.maxhp < 300:
                                        player.maxhp += 10
                                        chosen = True
                                if dab == "+health":
                                    if player.hp < player.maxhp + player.maxhp//4:
                                        player.hp += player.maxhp//4
                                        if player.hp > player.maxhp + player.maxhp//4:
                                            player.hp = player.maxhp + player.maxhp//4
                                        chosen = True
                                elif dab == "+1 extra bullet":
                                    player.bc += 1
                                    if player.bc > 2:
                                        player.bc = 2
                                    else:
                                        chosen = True
                                elif dab == "+speed":
                                    player.vel += 0.1
                                    if player.vel > 3:
                                        player.vel = 3
                                    else:
                                        chosen = True
                                elif dab == "+shooting speed":
                                    if player.bulletcooldown > 15:
                                        player.bulletcooldown -= 1
                                        chosen = True
                                elif dab == "+bullet velocity":
                                    if player.bulletvel < 29:
                                        player.bulletvel += 2
                                        chosen = True
                                elif dab == "+damage multiplier":
                                    if player.bulletdmgmultiplier < 2:
                                        player.bulletdmgmultiplier += 0.05
                                        chosen = True
                            texts.append(Text(player.x - player.r, player.y, dab, 20, colour, 50, "", 0.4))
                    if self.number < 1:
                        bullets.remove(self)
                    return
            if any(wall_cases):
                pygame.draw.circle(win, (255, 255, 0), wall_min_pd, self.r)
                bullets.remove(self)
                self.exist = False
                return
        else:
            if self.distance(player) < self.r + player.r:
                bloods.append(Blood(self.x, self.y, randint(1, 3), (255, 50, 10), 300))
                player.hp -= self.damage
                if player.hp <= 0:
                    player.hp = 0
                    player.alive = False
                    
                else:
                    texts.append(Text(randint(player.x - player.r * 2, player.x + player.r * 2), randint(player.y - player.r * 2, player.y + player.r * 2), "-" + str(self.damage), 10, (255, 100, 100), 30, "", 0.3))
                bullets.remove(self)
                return
            if any(wall_cases):
                pygame.draw.circle(win, (255, 255, 0), wall_min_pd, self.r)
                bullets.remove(self)
                self.exist = False
                return
    def avancer(self):
        self.x += self.vels[0]
        self.y += self.vels[1]

    def draw(self, win):
        coef = uniform(1, 4)
        pygame.draw.line(win, (255,255,0), (self.x, self.y), (self.x - self.vels[0]/coef, self.y - self.vels[1]/coef))#old colour: (160, 70, 70)




class Human:
    def __init__(self, x, y):
        #props(?)
        self.x = x
        self.y = y
        self.r = 16
        self.vel = 2
        self.maxhp = 100
        self.hp = self.maxhp
        self.alive = True
        self.mr, self.ml, self.mu, self.md = False, False, False, False
        self.milieu = (self.x, self.y)
        self.bulletvel = 15
        self.bulletdmglim = [20, 100]
        self.bulletdmgmultiplier = 0.1
        self.bulletcooldown = 15
        self.bulletcc = self.bulletcooldown
        self.bc = 1
        self.kk = 0
        self.hdl = 0

    def tire(self, cc, bullets):
        if not self.bulletcc >= self.bulletcooldown:
            self.bulletcc += 1
            return
        self.bulletdmg = randint(self.bulletdmglim[0], self.bulletdmglim[1])     
        self.bulletdmg *= self.bulletdmgmultiplier
        self.bulletdmg = int(self.bulletdmg)
        self.bulletcc = 0
        self.milieu = (self.x, self.y)
        pygame.mixer.find_channel().play(pshot)#pygame.mixer.Sound.play(pshot)
        #calculs
        if (cc[0] - self.milieu[0]) == 0:
            if cc[1] > self.milieu[1]:
                bullets.append(Bullet((self.x), (self.y), [0, self.bulletvel], "player", self.bulletdmg, self.bc, self.bulletvel))
            else:
                bullets.append(Bullet((self.x), (self.y), [0, -self.bulletvel], "player", self.bulletdmg, self.bc, self.bulletvel))
            return
        angle = abs(atan((cc[1] - self.milieu[1]) / (cc[0] - self.milieu[0])))
        vels = [self.bulletvel * abs(cos(angle)), self.bulletvel * abs(sin(angle))]
        
        if cc[0] < self.milieu[0]:
            vels[0] = -abs(vels[0])
        else:
            vels[0] = abs(vels[0])
        if cc[1] < self.milieu[1]:
            vels[1] = -abs(vels[1])
        else:
            vels[1] = abs(vels[1])
        bullets.append(Bullet((self.x), (self.y), vels, "player", self.bulletdmg, self.bc, self.bulletvel))
    """   
    def distance(self, sh):
        return sqrt(((sh.x + sh.w//2) - (self.x + self.w//2)) ** 2 + ((sh.y + sh.h//2) - (self.y + self.h//2)) ** 2)
    
    def distance_of_2(self, fh, sh):
        return sqrt(((sh.x + sh.w//2) - (fh.x + fh.w//2)) ** 2 + ((sh.y + sh.h//2) - (fh.y + fh.h//2)) ** 2)
    """
    
    def draw(self, win, texts):
        if self.hp > self.maxhp:
            self.hdl += 1
        if self.hdl >= 60:
            self.hdl = 0
            self.hp -= 1
        if self.hp == 0:
            self.alive = False
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(10, 10, self.maxhp + 2, 37))
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(11, 11, self.maxhp, 35))
        if self.hp > 0: 
            pygame.draw.rect(win, (70, 255, 70), pygame.Rect(11, 11, self.hp, 35))
        if self.hp > self.maxhp:
            pygame.draw.rect(win, (105,105,105), pygame.Rect(11 + self.maxhp, 11, self.hp - self.maxhp, 35))#rgb(105,105,105), (64,224,208)
        pygame.draw.circle(win, (60, 70, 170), (self.x, self.y), self.r)






class Baller:
    def __init__(self, x, y, maxhp, dmg, vel, etype):
        #props(?)
        self.etype = etype
        self.x = x
        self.y = y
        self.r = 16
        self.vel = vel
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.dmg = dmg
        self.waiting_time = 0
        self.bleed_time = 0
        self.counter = 0
        self.climit = 8#20
        self.shell_vel = 8
        self.spread = 0.1
        #equation --> y = am + b
        #"hitboxes"
        #horizontal hitbox
        self.mh = 0.1 / self.r*2
        self.bh = self.y - self.x * self.mh
        #vertical hitbox
        #m = delta y / delta x
        self.mv = self.r*2 / 0.1
        self.bv = self.y - self.x * self.mv
        
    def move(self, player, enemies, walls):
        #equation --> y = am + b
        #"hitboxes"
        #horizontal hitbox
        self.bh = self.y - self.x * self.mh
        #vertical hitbox
        #m = delta y / delta x
        self.bv = self.y - self.x * self.mv
        for wall in walls:
            if self.x + self.r  > wall.x and self.x - self.r < wall.x + wall.w and self.y + self.r > wall.y and self.y - self.r < wall.y + wall.h:
                if self.x < player.x:
                    self.x += self.vel * 2
                else:
                    self.x -= self.vel * 2
                if self.y < player.y:
                    self.y += self.vel * 2
                else:
                    self.y -= self.vel * 2
        if self.waiting_time > 0:
            self.waiting_time -= 1
        
        moved = False
        nearby_teammates = 0
        for enemy in enemies:
            if enemy != self:
                if self.distance(enemy) < self.r + enemy.r:
                    if self.x > enemy.x:
                        self.x += self.vel
                    else:
                        self.x -= self.vel
                    if self.y > enemy.y:
                        self.y += self.vel
                    else:
                        self.y -= self.vel
                    moved = True
                    #print("moved 1")
        #print(f"{self.distance(player)} > {400 + self.r} and {self.waiting_time} == 0 and {not(moved)}")
        if self.distance(player) > 400 + self.r and self.waiting_time == 0 and not(moved):
            if player.x + self.r*2 < self.x or player.x - self.r*2 > self.x:
                if player.x + self.r*2 < self.x:
                    self.x -= self.vel
                else:
                    self.x += self.vel
            if player.y + self.r*2 < self.y or player.y - self.r*2 > self.y:
                if player.y + self.r*2 < self.y:
                    self.y -= self.vel
                else:
                    self.y += self.vel
            moved = True
            #print("moved 2")

        if not(moved) and self.distance(player) <= 200 + self.r:
            if player.x + self.r*2 < self.x or player.x - self.r*2 > self.x:
                if player.x + self.r*2 < self.x:
                    self.x += self.vel
                else:
                    self.x -= self.vel
            if player.y + self.r*2 < self.y or player.y - self.r*2 > self.y:
                if player.y + self.r*2 < self.y:
                    self.y += self.vel
                else:
                    self.y -= self.vel
            moved = True
            #print("moved 3")

    def distance(self, target):
        return sqrt((target.x - self.x)**2 + (target.y - self.y)**2)

    def tire(self, player, bullets, enemies):
        #equation --> y = am + b
        #"hitboxes"
        #horizontal hitbox
        self.bh = self.y - self.x * self.mh
        #vertical hitbox
        #m = delta y / delta x
        self.bv = self.y - self.x * self.mv
        if self.distance(player) < 700:
            pygame.draw.line(win, (255, 0, 0), (self.x, self.y), (player.x, player.y))
        if self.counter >= self.climit and self.distance(player) < 700:
            self.waiting_time = 120
            self.milieu = (self.x, self.y)
            cc = [player.x, player.y]
            #if player.md:
                #cc[0] +=
            if self.distance(player) != 1:
                cannon_shot.set_volume(100/self.distance(player))
                pygame.mixer.find_channel().play(cannon_shot)
            else:
                cannon_shot.set_volume(100)
                pygame.mixer.find_channel().play(cannon_shot)

            #calculs
            if (cc[0] - self.milieu[0]) == 0:
                angle = abs(atan((cc[1] - self.milieu[1]) / choice([0.1, -0.1])))
            else:
                angle = abs(atan((cc[1] - self.milieu[1]) / (cc[0] - self.milieu[0])))
            angle = angle + uniform(-self.spread, self.spread)
            vels = [self.shell_vel * abs(cos(angle)), self.shell_vel * abs(sin(angle))]
            
            
            if cc[0] < self.milieu[0]:
                vels[0] = -abs(vels[0])
            else:
                vels[0] = abs(vels[0])
            if cc[1] < self.milieu[1]:
                vels[1] = -abs(vels[1])
            else:
                vels[1] = abs(vels[1])
            balls.append(Big_Black_Nigga_Balls_HD(self.x, self.y, vels, self.dmg, self.shell_vel))#(self.x), (self.y), vels, "enemy", self.bulletdmg, 0, self.bulletvel))
            self.counter = 0
        else:
            self.counter += 1
    def draw(self, win, bloods):
        if self.bleed_time > 0 or self.hp < self.maxhp * (15/100):#5 seconds, 300 frames
            if self.bleed_time%15 == 0:#20 or 19 blood drops
                bloods.append(Blood(randint(int(self.x - self.r), int(self.x + self.r)), randint(int(self.y - self.r), int(self.y + self.r)), randint(1, 3), (200, 50, 10), 300))
            self.bleed_time -= 1
        pygame.draw.circle(win, (30, 70, 90), (self.x, self.y), self.r)

class Magician:
    def __init__(self, x, y, maxhp, dmg, vel, etype):
        #props(?)
        self.etype = etype
        self.x = x
        self.y = y
        self.r = 16
        self.vel = vel
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.dmg = dmg
        self.waiting_time = 0
        self.bleed_time = 0
        #equation --> y = am + b
        #"hitboxes"
        #horizontal hitbox
        self.mh = 0.1 / self.r*2
        self.bh = self.y - self.x * self.mh
        #vertical hitbox
        #m = delta y / delta x
        self.mv = self.r*2 / 0.1
        self.bv = self.y - self.x * self.mv

    def move(self, player, enemies, walls):
        #equation --> y = am + b
        #"hitboxes"
        #horizontal hitbox
        self.bh = self.y - self.x * self.mh
        #vertical hitbox
        #m = delta y / delta x
        self.bv = self.y - self.x * self.mv
        for wall in walls:
            if self.x + self.r  > wall.x and self.x - self.r < wall.x + wall.w and self.y + self.r > wall.y and self.y - self.r < wall.y + wall.h:
                if self.x < player.x:
                    self.x += self.vel * 2
                else:
                    self.x -= self.vel * 2
                if self.y < player.y:
                    self.y += self.vel * 2
                else:
                    self.y -= self.vel * 2
        if self.waiting_time > 0:
            self.waiting_time -= 1
        
        moved = False
        nearby_teammates = 0
        for enemy in enemies:
            if enemy != self:
                if self.distance(enemy) < self.r + enemy.r:
                    if self.x > enemy.x:
                        self.x += self.vel
                    else:
                        self.x -= self.vel
                    if self.y > enemy.y:
                        self.y += self.vel
                    else:
                        self.y -= self.vel
                    moved = True
                    #print("moved 1")
        #print(f"{self.distance(player)} > {400 + self.r} and {self.waiting_time} == 0 and {not(moved)}")
        if self.distance(player) > 400 + self.r and self.waiting_time == 0 and not(moved):
            if player.x + self.r*2 < self.x or player.x - self.r*2 > self.x:
                if player.x + self.r*2 < self.x:
                    self.x -= self.vel
                else:
                    self.x += self.vel
            if player.y + self.r*2 < self.y or player.y - self.r*2 > self.y:
                if player.y + self.r*2 < self.y:
                    self.y -= self.vel
                else:
                    self.y += self.vel
            moved = True
            #print("moved 2")

        if not(moved) and self.distance(player) <= 200 + self.r:
            if player.x + self.r*2 < self.x or player.x - self.r*2 > self.x:
                if player.x + self.r*2 < self.x:
                    self.x += self.vel
                else:
                    self.x -= self.vel
            if player.y + self.r*2 < self.y or player.y - self.r*2 > self.y:
                if player.y + self.r*2 < self.y:
                    self.y += self.vel
                else:
                    self.y -= self.vel
            moved = True
            #print("moved 3")

    def distance(self, target):
        return sqrt((target.x - self.x)**2 + (target.y - self.y)**2)
    
    def do_magic(self, player, magics):
        #Magic(x, y, r, target, source, damage)
        #print(f"{self.distance(player)} < {450} and {self.waiting_time} == 0")
        if self.waiting_time == 0 and self.distance(player) < 450:
            magics.append(Magic(player.x, player.y, 128, player, self, self.dmg))
            self.waiting_time = 120
        elif self.waiting_time > 0:
            self.waiting_time -= 1
        
    def draw(self, win, bloods):
        if self.bleed_time > 0 or self.hp < self.maxhp * (15/100):#5 seconds, 300 frames
            if self.bleed_time%15 == 0:#20 or 19 blood drops
                bloods.append(Blood(randint(int(self.x - self.r), int(self.x + self.r)), randint(int(self.y - self.r), int(self.y + self.r)), randint(1, 3), (200, 50, 10), 300))
            self.bleed_time -= 1
        pygame.draw.circle(win, (75,0,130), (self.x, self.y), self.r)    

class Enemy:
    def __init__(self, x, y, maxhp, bulletdmg, vel, etype):
        #props(?)
        self.etype = etype
        self.x = x
        self.y = y
        self.r = 16
        self.vel = vel
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.mr, self.ml, self.mu, self.md = False, False, False, False
        self.milieu = (self.x, self.y)
        self.bulletvel = 10
        self.bulletdmg = bulletdmg
        self.climit = 150
        self.bleed_time = 0
        #equation --> y = am + b
        #"hitboxes"
        #horizontal hitbox
        self.mh = 0.1 / self.r*2
        self.bh = self.y - self.x * self.mh
        #vertical hitbox
        #m = delta y / delta x
        self.mv = self.r*2 / 0.1
        self.bv = self.y - self.x * self.mv
        self.waiting_time = 0
        self.spread = 0.05
        if self.etype == "minigun guy":
            self.climit = 5
            self.bulletvel = 7
            self.spread = 0.2
        self.counter = self.climit
        self.oclimit = self.climit
        
        
    def distance(self, target):
        return sqrt((target.x - self.x)**2 + (target.y - self.y)**2)

    def give_bleed_death_bonus(self, player, enemies, texts):
        if self.hp == 0:
            chosen = False
            da_while_blocker = 0
            colour = (50, 255, 50)
            if randint(1, 5) == 2:
                while not chosen and da_while_blocker < 10:
                    dab = choice(["+max health", "+health", "+1 extra bullet", "+speed", "+shooting speed", "+bullet velocity", "+damage multiplier"])
                    da_while_blocker += 1
                    if dab == "+max health":
                        if player.maxhp < 300:
                            player.maxhp += 10
                            chosen = True
                    if dab == "+health":
                        if player.hp < player.maxhp + player.maxhp//4:
                            player.hp += player.maxhp//4
                            if player.hp > player.maxhp + player.maxhp//4:
                                player.hp = player.maxhp + player.maxhp//4
                            chosen = True
                    elif dab == "+1 extra bullet":
                        player.bc += 1
                        if player.bc > 2:
                            player.bc = 2
                        else:
                            chosen = True
                    elif dab == "+speed":
                        player.vel += 0.1
                        if player.vel > 3:
                            player.vel = 3
                        else:
                            chosen = True
                    elif dab == "+shooting speed":
                        if player.bulletcooldown > 15:
                            player.bulletcooldown -= 1
                            chosen = True
                    elif dab == "+bullet velocity":
                        if player.bulletvel < 29:
                            player.bulletvel += 2
                            chosen = True
                    elif dab == "+damage multiplier":
                        if player.bulletdmgmultiplier < 2:
                            player.bulletdmgmultiplier += 0.05
                            chosen = True
                texts.append(Text(player.x - player.r, player.y, dab, 20, colour, 50, "", 0.4))
                enemies.remove(self)
                return
    
    def move(self, player, enemies, walls):
        for wall in walls:
            if self.x + self.r  > wall.x and self.x - self.r < wall.x + wall.w and self.y + self.r > wall.y and self.y - self.r < wall.y + wall.h:
                if self.x < player.x:
                    self.x += self.vel * 2
                else:
                    self.x -= self.vel * 2
                if self.y < player.y:
                    self.y += self.vel * 2
                else:
                    self.y -= self.vel * 2
        if self.waiting_time > 0:
            self.waiting_time -= 1
        
        moved = False
        nearby_teammates = 0
        for enemy in enemies:
            if enemy != self:
                if self.distance(enemy) < self.r + enemy.r:
                    if self.x > enemy.x:
                        self.x += self.vel
                    else:
                        self.x -= self.vel
                    if self.y > enemy.y:
                        self.y += self.vel
                    else:
                        self.y -= self.vel
                    moved = True
                if self.distance(enemy) < 64:
                    nearby_teammates += 1
                    
        if nearby_teammates == 0 and not(moved) and self.hp < self.maxhp * (15/100):
            self.waiting_time = 0
            if self.x > player.x:
                self.x += self.vel/2
            else:
                self.x -= self.vel/2
            if self.y > player.y:
                self.y += self.vel/2
            else:
                self.y -= self.vel/2
            moved = True
        if nearby_teammates == 0 and self.hp < self.maxhp/4:
            self.climit = self.oclimit * 2
        else:
            if self.etype == "minigun guy":
                self.climit = 5
            else:
                self.climit = 150

                
        if self.distance(player) > 164 + self.r and self.waiting_time == 0 and not(moved) and self.distance(player) > 64 + self.r:
            if player.x + self.r*2 < self.x or player.x - self.r*2 > self.x:
                if player.x + self.r*2 < self.x:
                    self.x -= self.vel
                else:
                    self.x += self.vel
            if player.y + self.r*2 < self.y or player.y - self.r*2 > self.y:
                if player.y + self.r*2 < self.y:
                    self.y -= self.vel
                else:
                    self.y += self.vel
            moved = True

        if not(moved) and self.distance(player) <= 64 + self.r:
            if player.x + self.r*2 < self.x or player.x - self.r*2 > self.x:
                if player.x + self.r*2 < self.x:
                    self.x += self.vel
                else:
                    self.x -= self.vel
            if player.y + self.r*2 < self.y or player.y - self.r*2 > self.y:
                if player.y + self.r*2 < self.y:
                    self.y += self.vel
                else:
                    self.y -= self.vel
            moved = True
    
    def tire(self, player, bullets, enemies):
        #equation --> y = am + b
        #"hitboxes"
        #horizontal hitbox
        self.bh = self.y - self.x * self.mh
        #vertical hitbox
        #m = delta y / delta x
        self.bv = self.y - self.x * self.mv
        if self.counter >= self.climit and (self.distance(player) < 200 or (self.etype == "minigun guy" and self.distance(player) < 500)):
            self.waiting_time = 180
            if self.etype == "minigun guy":
                self.waiting_time = 120
            self.milieu = (self.x, self.y)
            cc = [player.x, player.y]
            #if player.md:
                #cc[0] +=
            try:
                if self.etype == "minigun guy":
                    emgshot.set_volume(200/self.distance(player))
                    pygame.mixer.find_channel().play(emgshot)
                else:
                    eshot.set_volume(100/self.distance(player))
                    pygame.mixer.find_channel().play(eshot)
            except:
                if self.etype == "minigun guy":
                    emgshot.set_volume(200/1)
                    pygame.mixer.find_channel().play(emgshot)
                else:
                    eshot.set_volume(100/1)
                    pygame.mixer.find_channel().play(eshot)
            #calculs
            if (cc[0] - self.milieu[0]) == 0:
                """
                if cc[1] > self.milieu[1]:
                    bullets.append(Bullet((self.x), (self.y), [0, self.bulletvel], "enemy", self.bulletdmg, 0, self.bulletvel))
                else:
                    bullets.append(Bullet((self.x), (self.y), [0, -self.bulletvel], "enemy", self.bulletdmg, 0, self.bulletvel))
                self.counter = 0
                return
                """
                angle = abs(atan((cc[1] - self.milieu[1]) / choice([0.1, -0.1])))
            else:
                angle = abs(atan((cc[1] - self.milieu[1]) / (cc[0] - self.milieu[0])))
            da_spread = uniform(-self.spread, self.spread)
            angle += da_spread
            vels = [self.bulletvel * abs(cos(angle)), self.bulletvel * abs(sin(angle))]
            
            
            if cc[0] < self.milieu[0]:
                vels[0] = -abs(vels[0])
            else:
                vels[0] = abs(vels[0])
            if cc[1] < self.milieu[1]:
                vels[1] = -abs(vels[1])
            else:
                vels[1] = abs(vels[1])
            bullets.append(Bullet((self.x), (self.y), vels, "enemy", self.bulletdmg, 0, self.bulletvel))
            self.counter = 0
        else:
            self.counter += 1
            
    def draw(self, win, bloods):
        #print(self.bleed_time, self.hp, self.maxhp)
        if self.bleed_time > 0 or self.hp < self.maxhp * (15/100):#5 seconds, 300 frames
            if self.bleed_time%15 == 0:#20 or 19 blood drops
                bloods.append(Blood(randint(int(self.x - self.r), int(self.x + self.r)), randint(int(self.y - self.r), int(self.y + self.r)), randint(1, 3), (200, 50, 10), 300))
            self.bleed_time -= 1
            if self.hp < self.maxhp * (15/100):
                self.hp = self.hp - (self.maxhp * (1/2000))
                if self.bleed_time == 0:
                    self.bleed_time = 300
            if self.hp < 0:
                self.hp = 0
        if self.etype == "minigun guy":
            pygame.draw.circle(win, (61, 12, 2), (self.x, self.y), self.r)
        else:
            pygame.draw.circle(win, (232, 190, 172), (self.x, self.y), self.r)
        
    

class Wall:
    def __init__(self, x, y, w, h, colour):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.center = [self.x + self.w/2, self.y + self.h/2]
        self.colour = colour
        #equation --> y = am + b
        #"hitboxes"
        #the top horizontal line
        self.th = self.get_droite_equation((self.x, self.y), (self.x + self.w, self.y))
        #the bottom horizontal line
        self.bh = self.get_droite_equation((self.x, self.y + self.h), (self.x + self.w, self.y + self.h))
        #the western vertical line
        self.wv = self.get_droite_equation((self.x, self.y), (self.x, self.y + self.h))
        #the eastern vertical line
        self.ev = self.get_droite_equation((self.x + self.w, self.y), (self.x + self.w, self.y + self.h))

        self.droites = [self.th, self.bh, self.wv, self.ev]
        return

    def get_droite_equation(self, point1, point2):
        delta_y = point2[1] - point1[1]
        delta_x = point2[0] - point1[0]
        if delta_y == 0:
            delta_y = 0.1
        if delta_x == 0:
            delta_x = 0.1
        m = delta_y / delta_x
        b = point1[1] - point1[0] * m
        return [m, b, point1, point2]

    def update_b(self, point1, m):
        return point1[1] - point1[0] * m

    def update_bs(self):
        self.droites[0][1] = self.update_b((self.x, self.y), self.droites[0][0])
        self.droites[1][1] = self.update_b((self.x, self.y + self.h), self.droites[1][0])
        self.droites[2][1] = self.update_b((self.x, self.y), self.droites[2][0])
        self.droites[3][1] = self.update_b((self.x + self.w, self.y), self.droites[3][0])
        
    def detect_collision(self, player):
        if player.mr and player.x >= self.x - player.r - player.vel and player.x <= self.x:
            if player.y >= self.y - player.r and player.y <= self.y + self.h + player.r:
                player.mr = False
        if player.ml and player.x <= self.x + self.w + player.r + player.vel and player.x >= self.x + self.w:
            if player.y >= self.y - player.r and player.y <= self.y + self.h + player.r:
                player.ml = False
        if player.mu and player.y <= self.y + self.h + player.r + player.vel and player.y >= self.y + self.h:
            if player.x >= self.x - player.r and player.x <= self.x + self.w + player.r:
                player.mu = False
        if player.md and player.y >= self.y - player.r - player.vel and player.y <= self.y:
            if player.x >= self.x - player.r and player.x <= self.x + self.w + player.r:
                 player.md = False
        return

    def draw(self, win):
        self.center = [self.x + self.w/2, self.y + self.h/2]
        pygame.draw.rect(win, self.colour, pygame.Rect(self.x, self.y, self.w, self.h))


def enemy_wave_spawner(enemies, walls, enemy_counter, enemy_counter_limit, wave, enemy_randomizer_lims, wave_text):
    enemy_counter += 1
    daw_counter = 0
    if enemy_counter == enemy_counter_limit or len(enemies) == 0:
        enemy_counter_limit += 120
        wave += 1
        wave_text.variable += 1
        #print("-----------------------------------------")
        for j in range(int(wave * 1.3)):
            enemy_randomizer = [uniform(enemy_randomizer_lims[0], enemy_randomizer_lims[1]), int(uniform(enemy_randomizer_lims[2], enemy_randomizer_lims[3]))]
            enemy_spawn = choice(walls)
            
            if enemy_spawn.x >= 0:
                da_x = randint(int(enemy_spawn.x), int(enemy_spawn.x + enemy_spawn.w))
            elif enemy_spawn.x < 0 and enemy_spawn.x + enemy_spawn.w >= 0:
                da_x = randint(int(enemy_spawn.x), int(enemy_spawn.x + enemy_spawn.w))
            elif enemy_spawn.x < 0 and enemy_spawn.x + enemy_spawn.w < 0:
                da_x = -abs(randint(int(enemy_spawn.x - enemy_spawn.w), int(enemy_spawn.x)))
            if enemy_spawn.y >= 0:
                da_y = randint(int(enemy_spawn.y), int(enemy_spawn.y + enemy_spawn.h))
            elif enemy_spawn.y < 0 and enemy_spawn.y + enemy_spawn.h >= 0:
                da_y = randint(int(enemy_spawn.y), int(enemy_spawn.y + enemy_spawn.h))
            else:
                da_y = -abs(randint(int(enemy_spawn.y - enemy_spawn.h), int(enemy_spawn.y)))
            #print("------------------------------")
            #print(f"{enemy_spawn.x}, {enemy_spawn.y}, {enemy_spawn.w}, {enemy_spawn.h}\n{da_x}, {da_y}")
            #print(f"{enemy_spawn.x} < {da_x} < {enemy_spawn.x + enemy_spawn.w},  {enemy_spawn.y} < {da_y} < {enemy_spawn.y + enemy_spawn.w}")
            #print(da_x, da_y)
            #x, y, maxhp, bulletdmg, vel, etype)
            #magician(x, y, maxhp, dmg, vel, etype)
            if wave >= 10 and wave%5 == 0:
                if daw_counter%2 == 0:
                    enemies.append(Enemy(da_x, da_y, enemy_randomizer[0] * 2, enemy_randomizer[1] // 4, 1, "minigun guy"))#-1, randint(1, 3)))
                else:
                    enemies.append(Magician(da_x, da_y, enemy_randomizer[0] / 2, enemy_randomizer[1], 1, "magician"))#-1, randint(1, 3)))
                daw_counter += 1
            elif randint(1, 15) == 2 and wave >= 10:
                enemies.append(Baller(da_x, da_y, enemy_randomizer[0], enemy_randomizer[1] // 3, 1, "baller"))
            elif randint(1, 10) == 2 and wave >= 5:
                enemies.append(Magician(da_x, da_y, enemy_randomizer[0] / 2, enemy_randomizer[1], 1, "magician"))#-1, randint(1, 3)))
            elif randint(1, 7) == 2 and wave >= 3:
                enemies.append(Enemy(da_x, da_y, enemy_randomizer[0] * 2, enemy_randomizer[1] // 4, 1, "minigun guy"))#-1, randint(1, 3)))
            else:
                enemies.append(Enemy(da_x, da_y, enemy_randomizer[0], enemy_randomizer[1], randint(1, 3), "normal"))#-1, randint(1, 3)))
            for i in range(len(enemy_randomizer_lims)):
                if i == 0:
                    enemy_randomizer_lims[i] = enemy_randomizer_lims[i] * 0.5 + 10
                elif i == 1:
                    enemy_randomizer_lims[i] = enemy_randomizer_lims[i] * 0.5 + 50
                elif i == 2:
                    enemy_randomizer_lims[i] = enemy_randomizer_lims[i] * 0.5 + 2
                elif i == 3:
                    enemy_randomizer_lims[i] = enemy_randomizer_lims[i] * 0.5 + 15
            enemy_counter = 0

    return enemies, enemy_counter, wave, enemy_randomizer_lims




player = Human(300, 300)
humans = [player]
bullets = []
enemies = []#Enemy(10, 10, 100, -10000, 2)]
texts = []
bloods = []
walls = []
magics = []
balls = []

walls.append(Wall(player.x - 1000, player.y - 1000, 2000, 300, (139,69,19)))#top wall
walls.append(Wall(player.x - 1000, player.y - 1000, 300, 2000, (139,69,19)))#west wall
walls.append(Wall(player.x + 1000, player.y - 1000, 300, 2300, (139,69,19)))#east wall
walls.append(Wall(player.x - 1000, player.y + 1000, 2300, 300, (139,69,19)))#bottom wall

hud = Hud(0, wh * (5/6), ww, wh * (1/6), (128,128,128), (105,105,105))



death_text =  Text(300, 200, "GAME OVER! Killed ", 30, (255, 0, 0), -1, player.kk)
wave_text =  Text(500, 500, "WAVE ", 15, (0, 0, 0), -1, 0)#(150, 150, 0), -1, 0)
kill_text =  Text(500, 550, "KILLED ", 15, (0, 0, 0), -1, 0)#(150, 150, 0), -1, 0)

hud.hud_texts.append(wave_text)
hud.hud_texts.append(kill_text)

clock = pygame.time.Clock()
running = True
#ayeee = 0
#compteur = 0
enemy_counter = 0
enemy_counter_limit = 1200
enemy_randomizer_lims = [30, 50, 1, 10]
wave = 0
shooting = False
shooting_speed = 1
fps = 60
p_l, p_r, p_u, p_d = False, False, False, False
while running:
    #if enemies:
        #print((enemies[0].x, enemies[0].y))
    clock.tick(fps)
    if player.alive or True:
        enemies, enemy_counter, wave, enemy_randomizer_lims = enemy_wave_spawner(enemies, walls, enemy_counter, enemy_counter_limit, wave, enemy_randomizer_lims, wave_text)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
        if player.alive:
            if event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:# and pygame.FINGERMOVE:#mouse_pos = pygame.mouse.get_pos()
                shooting = True
                player.bulletcc = player.bulletcooldown
            elif event.type == pygame.FINGERUP or event.type == pygame.MOUSEBUTTONUP:
                shooting = False
                player.cc = player.bulletcooldown
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    p_l = True
                    player.ml = True
                if event.key == pygame.K_RIGHT:
                    p_r = True
                    player.mr = True
                if event.key == pygame.K_UP:
                    p_u = True
                    player.mu = True
                if event.key == pygame.K_DOWN:
                    p_d = True
                    player.md = True
                for wall in walls:
                    wall.detect_collision(player)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    p_l = False
                    player.ml = False
                if event.key == pygame.K_RIGHT:
                    p_r = False
                    player.mr = False
                if event.key == pygame.K_UP:
                    p_u = False
                    player.mu = False
                if event.key == pygame.K_DOWN:
                    p_d = False
                    player.md = False
        else:
            player.ml, player.md, player.mu, player.mr = False, False, False, False
            shooting = False

    if True in [player.md, player.mu, player.mr, player.ml]:
        if player.ml:
            for liste in [bullets, enemies, texts, walls, bloods, magics, balls]:
                for element in liste:
                    element.x += player.vel
        if player.mr:
            for liste in [bullets, enemies, texts, walls, bloods, magics, balls]:
                for element in liste:
                    element.x -= player.vel
        if player.mu:
            for liste in [bullets, enemies, texts, walls, bloods, magics, balls]:
                for element in liste:
                    element.y += player.vel
        if player.md:
            for liste in [bullets, enemies, texts, walls, bloods, magics, balls]:
                for element in liste:
                    element.y -= player.vel

    if shooting:
        mouse_pos = pygame.mouse.get_pos()
        player.tire(mouse_pos, bullets)
        
        
    if player.alive:
        if p_l:
            player.ml = True
        if p_r:
            player.mr = True
        if p_d:
            player.md = True
        if p_u:
            player.mu = True
    else:
        player.ml = False
        player.mr = False
        player.md = False
        player.mu = False
    for wall in walls:
        wall.detect_collision(player)
        
    if not running:
        break
    win.fill((50, 130, 90))#30, 30, 30))#(160, 70, 70))
    for magic in magics:
        magic.draw_mark(win)
    for blood in bloods:
        blood.draw(win, bloods)
    for bullet in bullets:
        bullet.toucher(enemies, player, bullets, texts, walls, bloods, death_text)
        bullet.avancer()
        if bullet.exist:
            bullet.draw(win)
    for ball in balls:
        ball.toucher(player, balls, walls)
        ball.explode(win, player)
        ball.avancer()
        if ball.exist:
            ball.draw(win)
    for enemy in enemies:
        if enemy.etype == "normal" or enemy.etype == "minigun guy":
            enemy.move(player, enemies, walls)
            enemy.draw(win, bloods)
            enemy.tire(player, bullets, enemies)
            enemy.give_bleed_death_bonus(player, enemies, texts)
        elif enemy.etype == "magician":
            enemy.move(player, enemies, walls)
            enemy.draw(win, bloods)
            enemy.do_magic(player, magics)
        elif enemy.etype == "baller":
            enemy.move(player, enemies, walls)
            enemy.tire(player, bullets, enemies)
            enemy.draw(win, bloods)
    for wall in walls:
        wall.update_bs()
        wall.draw(win)
    for magic in magics:
        magic.draw_blast(win, magics, player)
    for human in humans:
        human.draw(win, texts)
    for text in texts:
        text.draw(win, texts)
    if not player.alive:
        death_text.draw(win, texts)
    wave_text.draw(win, texts)
    kill_text.draw(win, texts)
    hud.draw(win, texts, player, enemies, walls[0])

    pygame.display.flip()










