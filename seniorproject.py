import pygame
import time
import random
import sys
import math
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

clock = pygame.time.Clock()
WIN_W = 32*32
WIN_H = 32*20
fps = 60
black = (0,0,0)
white = (255,255,255)
screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
tile_width = tile_height = 32
#sound = {}
#sound["gamestart"] = pygame.mixer.Sound("sound/gamestart.wav")
#sound["victory"] = pygame.mixer.Sound("sound/victory.wav")
#sound["hit1"] = pygame.mixer.Sound("sound/hit1.wav")
#sound["hit2"] = pygame.mixer.Sound("sound/hit2.wav")
#sound["chestopen"] = pygame.mixer.Sound("sound/chestopen.mp3")
#sound["gameover"] = pygame.mixer.Sound("sound/gameover.mp3")
tile_G = pygame.image.load("tile_G2.png").convert_alpha()
tile_M = pygame.image.load("tile_M.png").convert_alpha()
tile_W = pygame.image.load("tile_W.png").convert_alpha()
tile_T = pygame.image.load("tile_T.png").convert_alpha()
tile_C = pygame.image.load("tile_C.gif").convert_alpha()
tile_D = pygame.image.load("tile_D.png").convert_alpha()
bandit = pygame.image.load("bandit.gif").convert_alpha()
monster = pygame.image.load("soldier.gif").convert_alpha()
hero_image = pygame.image.load("hero.png").convert_alpha()
dagger = pygame.image.load("dagger.png").convert_alpha()
sword = pygame.image.load("sword.jpg").convert_alpha()
bigsword = pygame.image.load("bigsword.png").convert_alpha()
potion = pygame.image.load("potion.png").convert_alpha()
lightarmor = pygame.image.load("lightarmor.png").convert_alpha()
heavyarmor = pygame.image.load("heavyarmor.png").convert_alpha()
battlebackground1 = pygame.image.load("level1battleback.png").convert()
battlebackground = pygame.transform.scale(battlebackground1, (WIN_W, WIN_H))
battlebackrect = battlebackground.get_rect()
battlebackrect = battlebackrect.move(0,0)
hero_right_face = pygame.transform.scale(hero_image, (32, 32))
hero_left_face = pygame.transform.flip(hero_right_face, True, False)
hero_right_face_big = pygame.transform.scale(hero_image, (96,96))
hero_left_face_big = pygame.transform.flip(hero_right_face_big, True, False)
shield = pygame.image.load("shield.png").convert_alpha()
type = 0
mtype = 0
kills = 0
fighting = False



pygame.init()


class Hero(pygame.sprite.Sprite):
    def __init__(self, health, strength, defense, speed, weapon, armor, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.health = health
        self.weapon = weapon
        self.armor = armor
        self.basestrength = strength
        self.basedefense = defense
        self.basebattlespeed = speed
        self.speed = 4
        self.strength = self.weaponstats()
        self.defense = self.armordefense()
        self.battlespeed = self.armorspeed()
        self.image = pygame.image.load("hero.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = WIN_H/2
        self.direction = 0
        self.key = 0
        self.exp = 0
        self.level = 0
        self.nextlvlreq = 100
        self.energy = 0
        self.hittimer = 0
        self.defending = 0

    def weaponstats(self):
        newstrength = 0
        if self.weapon == "Hands":
            newstrength = self.basestrength
        if self.weapon == "Dagger":
            newstrength = self.basestrength + 2
        if self.weapon == "Sword":
            newstrength = self.basestrength + 4
        if self.weapon == "Big Sword":
            newstrength = self.basestrength + 7
        if self.weapon == "420_Bong_420":
            newstrength = self.basestrength + 69
        return newstrength
    def armordefense(self):
        newdefense = 0
        if self.armor == "None":
            newdefense = self.basedefense
        if self.armor == "Light Armor":
            newdefense = self.basedefense + 1
        if self.armor == "Heavy Armor":
            newdefense = self.basedefense + 3
        return newdefense
    def armorspeed(self):
        newspeed = 0
        if self.armor == "None":
            newspeed = self.basebattlespeed
        if self.armor == "Light Armor":
            newspeed = self.basebattlespeed - 1
        if self.armor == "Heavy Armor":
            newspeed = self.basebattlespeed - 3
        return newspeed
    def update(self, nopasstile_group, chest_group, monster_group, kills, tile_group, fighting):
        up = left = right = down = False
        if fighting == True:
            if self.defending == 1:
                self.speed = 3
            if self.defending == 0:
                self.speed = 7
        else:
            self.speed = 4

        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.y > 0 and fighting == False:
            self.rect.y -= self.speed
            up = True
        if key[pygame.K_DOWN] and self.rect.y < WIN_H - 32 and fighting == False:
            self.rect.y += self.speed
            down = True
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            left = True
        if key[pygame.K_RIGHT] and self.rect.x < WIN_W - 32:
            self.rect.x += self.speed
            right = True
        self.imagedirection(left, right, fighting)
        self.collide(nopasstile_group, up, down, left, right, chest_group, monster_group, kills, tile_group, fighting)
    def collide(self, nopasstile_group, up, down, left, right, chest_group, monster_group, kills, tile_group, fighting):
        for p in nopasstile_group:
            if fighting == False:
                if pygame.sprite.collide_rect(self, p) and right:
                    self.rect.x -= 4
                if pygame.sprite.collide_rect(self, p) and left:
                    self.rect.x += 4
                if pygame.sprite.collide_rect(self, p) and down:
                    self.rect.y -= 4
                if pygame.sprite.collide_rect(self, p) and up:
                    self.rect.y += 4
        for c in chest_group:
            if pygame.sprite.collide_rect(self, c) and c.opened == 0 and pygame.key.get_pressed()[pygame.K_z] and self.key > 0:
                randnumb = random.randrange(2,6)
                if randnumb == 1:
                    if self.weapon == "Hands":
                        self.weapon = "Dagger"
                        self.strength = self.weaponstats()
                        prize = "a Dagger"
                        self.chestopen(prize, randnumb, tile_group, chest_group, nopasstile_group, monster_group)
                    else:
                        print ("You already had a Dagger or something better.")
                if randnumb == 2:
                    if self.weapon == "Hands" or self.weapon == "Dagger":
                        self.weapon = "Sword"
                        self.strength = self.weaponstats()
                        prize = "a Sword"
                        self.chestopen(prize, randnumb, tile_group, chest_group, nopasstile_group, monster_group)
                    else:
                        print ("You already had a Sword or something better.")
                if randnumb == 3:
                    if self.weapon != "Big Sword":
                        self.weapon = "Big Sword"
                        self.strength = self.weaponstats()
                        prize = "a Big Sword"
                        self.chestopen(prize, randnumb, tile_group, chest_group, nopasstile_group, monster_group)
                    else:
                        print ("You already had a Big Sword or something better.")
                if randnumb == 4:
                    if self.armor == "None":
                        self.armor = "Light Armor"
                        self.defense = self.armordefense()
                        prize = "some Light Armor"
                        self.chestopen(prize, randnumb, tile_group, chest_group, nopasstile_group, monster_group)
                    else:
                        print ("You already had Light armor or something better.")
                if randnumb == 5:
                    if self.armor != "Heavy Armor":
                        self.armor = "Heavy Armor"
                        self.defense = self.armordefense()
                        prize = "some Heavy Armor"
                        self.chestopen(prize, randnumb, tile_group, chest_group, nopasstile_group, monster_group)
                    else:
                        print ("You already had Heavy Armor or better.")
                if randnumb == 6:
                    self.health += random.randrange(10,21)
                    prize = "a Potion! You now have " + str(self.health) + " health!"
                    self.chestopen(prize, randnumb, tile_group, chest_group, nopasstile_group, monster_group)
                c.opened = 1
                self.key -= 1
            if pygame.sprite.collide_rect(self, c) and c.opened == 0 and pygame.key.get_pressed()[pygame.K_z] and self.key == 0:
                print("You need a key to open this chest!")
        for m in monster_group:
            if pygame.sprite.collide_rect(self, m) and fighting == False:
                m.rect.y = -100
                self.battle(m, kills, nopasstile_group, chest_group, monster_group, tile_group, right, left)

    def chestopen(self, prize, randnumb, tile_group, chest_group, nopasstile_group, monster_group):
        #sound["chestopen"].play()
        prizesprite = pygame.transform.scale(sword, (64,64))
        chestfont = pygame.font.Font(None, 50)
        chesttitle = chestfont.render("You got " + str(prize), 1, (75,0,130))
        chesttitlepos = chesttitle.get_rect()
        chesttitlepos.x = screen.get_rect().centerx - 300
        chesttitlepos.y = screen.get_rect().centery - 130
        if randnumb == 1:
            prizesprite = pygame.transform.scale(dagger, (92,92))
        if randnumb == 2:
            prizesprite = pygame.transform.scale(sword, (92,92))
        if randnumb == 3:
            prizesprite = pygame.transform.scale(bigsword, (92,92))
        if randnumb == 4:
            prizesprite = pygame.transform.scale(lightarmor, (92,92))
        if randnumb == 5:
            prizesprite = pygame.transform.scale(heavyarmor, (92,92))
        if randnumb == 6:
            prizesprite = pygame.transform.scale(potion, (92,92))
        prizespritepos = prizesprite.get_rect()
        prizespritepos.x = screen.get_rect().centerx - 48
        prizespritepos.y = screen.get_rect().centery
        for i in range(150):
            screen.fill(white)
            tile_group.draw(screen)
            chest_group.draw(screen)
            nopasstile_group.draw(screen)
            monster_group.draw(screen)
            screen.blit(self.image, (self.rect.x, self.rect.y))
            screen.blit(prizesprite, prizespritepos)
            screen.blit(chesttitle, chesttitlepos)


            clock.tick(fps)
            pygame.display.flip()


    def imagedirection(self, left, right, fighting):
        if fighting == True:
            pass
        else:
            if right and fighting == False:
                self.image = hero_right_face
            elif left and fighting == False:
                self.image = hero_left_face


    def battle(self, m, kills, nopasstile_group, chest_group, monster_group, tile_group, right, left):
        fighting = True
        leveluptext = ""
        #sound
        savespotx = self.rect.x
        savespoty = self.rect.y
        time.sleep(1)
        screen.fill(black)
        self.energy = 0
        self.image = pygame.transform.scale(hero_image, (96,96))
        self.rect.x = 256 - 96
        self.rect.y = 224
        m.image = pygame.transform.scale(m.image, (96,96))
        m.rect.x = 768
        m.rect.y = 224
        if m.type == "monster":
            m.image = pygame.transform.scale(m.image, (192,192))
            m.rect.y = 224-64

        battlefont = pygame.font.Font(None, 80)
        battletitle = battlefont.render("PRESS 'Z' TO ATTACK", 1, (255,0,0))
        battletitlepos = battletitle.get_rect()
        battletitlepos.centerx = screen.get_rect().centerx
        battletitlepos.centery = screen.get_rect().centery + 200
        battlefont2 = pygame.font.Font(None, 80)
        battletitle2 = battlefont2.render("PRESS 'X' TO DEFEND", 1, white)
        battletitlepos2 = battletitle2.get_rect()
        battletitlepos2.centerx = screen.get_rect().centerx
        battletitlepos2.centery = screen.get_rect().centery + 150
        victoryfont = pygame.font.Font(None, 100)
        victorytitle1 = victoryfont.render("YOU WON THE FIGHT!!!!", 1, (0,0,255))
        victorytitle2 = victoryfont.render("YOU HAVE DIED.", 1, (255,0,0))
        victorytitlepos = victorytitle1.get_rect()
        victorytitlepos.centerx = screen.get_rect().centerx
        victorytitlepos.centery = screen.get_rect().centery - 130
        expfont = pygame.font.Font(None, 50)
        exptitle = expfont.render(leveluptext, 1, (0,0,255))
        exptitlepos = exptitle.get_rect()
        exptitlepos.centerx = screen.get_rect().centerx - 400
        exptitlepos.centery = screen.get_rect().centery - 130
        herodamage = self.strength - m.defense
        enemydamage = m.strength - self.defense
        shieldimage = pygame.transform.scale(shield, (64,64))
        herodefense = self.defense
        if self.weapon == "Hands":
            pass
        if self.weapon == "Dagger":
            weaponimagebase = pygame.transform.scale(dagger, (64,64))
        if self.weapon == "Sword":
            weaponimagebase = pygame.transform.scale(sword, (64,64))
        if self.weapon == "Big Sword":
            weaponimagebase = pygame.transform.scale(bigsword, (64,64))
        if herodamage <= 0:
            herodamage = 1
        if (enemydamage * 2) <= 0:
            enemydamage = 1
        while fighting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                    sys.exit()
            self.energy += 1
            herodamage = self.strength - m.defense
            enemydamage = m.strength - self.defense
            if herodamage <= 0:
                herodamage = 1
            if (enemydamage * 2) <= 0:
                enemydamage = 1
            if m.type == "monster":
                m.energy += .6
            else:
                m.energy += .9
            self.hittimer += 1
            if self.energy >= 100:
                self.energy = 100
            if m.energy >= 100:
                m.energy = 100
            if self.hittimer >= 40:
                self.hittimer = 40
            healthfont = pygame.font.Font(None, 50)
            herohealth = healthfont.render(str(self.health) + "HP", 1, (0,255,0))
            herohealthpos = herohealth.get_rect()
            herohealthpos.x = self.rect.x
            herohealthpos.y = self.rect.y - 150
            monsterhealth = healthfont.render(str(m.health) + "HP", 1, (255,0,0))
            monsterhealthpos = monsterhealth.get_rect()
            monsterhealthpos.x = m.rect.x
            monsterhealthpos.y = m.rect.y - 150
            energyfont = pygame.font.Font(None, 35)
            heroenergy = energyfont.render(str(self.energy), 1, (255,255,0))
            heroenergypos = heroenergy.get_rect()
            heroenergypos.x = self.rect.x
            heroenergypos.y = self.rect.y - 75
            monsterenergy = energyfont.render(str(m.energy), 1, (255,255,0))
            monsterenergypos = monsterenergy.get_rect()
            monsterenergypos.x = m.rect.x
            monsterenergypos.y = m.rect.y - 75
            if pygame.key.get_pressed()[pygame.K_x]:
                self.defense = int(herodefense * 2)
                self.defending = 1
            else:
                self.defense = herodefense
                self.defending = 0
            if pygame.key.get_pressed()[pygame.K_z] and pygame.key.get_pressed()[pygame.K_x] == 0:
                weaponimage = pygame.transform.rotate(weaponimagebase, -115)
                if abs((self.rect.x + 60) - m.rect.x) <= 70 and self.hittimer >= 40:
                    #sound
                    m.health -= int(herodamage * (float(self.energy)/float(80)))
                    self.hittimer = 0
                    self.energy = 0
                else:
                    #sound
                    self.hittimer = 0
                    self.energy = 0
            else:
                weaponimage = pygame.transform.rotate(weaponimagebase, -45)
            if m.energy >= 100:
                m.hitanimation += 1
                if m.hitanimation > 1 and m.hitanimation <= 6:
                    m.rect.x -= 9
                if m.hitanimation == 8:
                    if abs(m.rect.x - (self.rect.x + 60)) <= 70:
                        self.health -= enemydamage
                if m.hitanimation > 10 and m.hitanimation <= 15:
                    m.rect.x += 9
                if m.hitanimation == 16:
                    m.energy = 0
                    m.hitanimation = 0
            if self.weapon != "Hands":
                weaponimagepos = weaponimage.get_rect()
                weaponimagepos.centerx = self.rect.x + 96
                weaponimagepos.centery = self.rect.y + 48
            shieldimagepos = shieldimage.get_rect()
            shieldimagepos.centerx = self.rect.x + 32
            shieldimagepos.centery = self.rect.y + 64
            if m.health <= 0:
                #sound["victory"].play()
                self.rect.x = WIN_W/2 - 48
                self.rect.y = 224
                self.exp += m.exp
                m.rect.y = -500
                for i in range(180):
                    screen.blit(battlebackground, battlebackrect)
                    screen.blit(self.image, self.rect)
                    screen.blit(victorytitle1, victorytitlepos)
                    clock.tick(fps)
                    pygame.display.flip()
                for i in range(1,11):
                    print(self.exp)
                    if self.exp >= self.nextlvlreq:
                        self.level += 1
                        if self.level == 1:
                            self.nextlvlreq = 200
                        if self.level == 2:
                            self.nextlvlreq = 300
                        if self.level == 3:
                            self.nextlvlreq = 400
                        if self.level == 4:
                            self.nextlvlreq = 500
                        if self.level == 5:
                            self.nextlvlreq = 600
                        if self.level == 6:
                            self.nextlvlreq = 700
                        if self.level == 7:
                            self.nextlvlreq = 800
                        if self.level == 8:
                            self.nextlvlreq = 900
                        if self.level == 9:
                            self.nextlvlreq = 1000
                        if self.level == 10:
                            self.nextlvlreq = 1100
                        self.basestrength += random.randrange(2,4)
                        self.basedefense += random.randrange(1,3)
                        self.weaponstats()
                        self.armordefense()
                        leveluptext = "YOU HAVE LEVELED UP! YOU ARE NOW LEVEL" + str(self.level)
                        exptitle = expfont.render(leveluptext, 1, (0,0,255))
                        for i in range(180):
                            screen.blit(battlebackground, battlebackrect)
                            screen.blit(self.image, self.rect)
                            screen.blit(exptitle, exptitlepos)

                            clock.tick(fps)
                            pygame.display.flip()
                self.rect.x = savespotx
                self.rect.y = savespoty
                self.image = pygame.transform.scale(self.image, (32,32))
                kills += 1
                self.key += 1
                fighting = False
            if self.health <= 0:
                #sound["gameover"].play()
                self.rect.x = WIN_W/2 - 48
                self.rect.y = 224
                self.image = pygame.transform.rotate(self.image,90)
                m.rect.y = -500
                for i in range(180):
                    screen.blit(battlebackground, battlebackrect)
                    screen.blit(self.image, self.rect)
                    screen.blit(victorytitle2, victorytitlepos)
                    clock.tick(fps)
                    pygame.display.flip()
                sys.exit()

            self.update(nopasstile_group, chest_group, monster_group, kills, tile_group, fighting)
            screen.blit(battlebackground, battlebackrect)
            screen.blit(self.image, self.rect)
            if self.weapon != "Hands":
                screen.blit(weaponimage, weaponimagepos)
            screen.blit(m.image, m.rect)
            screen.blit(battletitle, battletitlepos)
            screen.blit(battletitle2, battletitlepos2)
            screen.blit(herohealth, herohealthpos)
            screen.blit(monsterhealth, monsterhealthpos)
            screen.blit(heroenergy, heroenergypos)
            screen.blit(monsterenergy, monsterenergypos)
            if self.defending == 1:
                screen.blit(shieldimage, shieldimagepos)

            clock.tick(fps)
            pygame.display.flip()

    def __str__(self):
        return "Health: " + str(self.health) + ", Strength: " + str(self.strength) + ", Defense: " + str(self.defense) + ", Speed: " + str(self.speed) + ", Weapon: " + str(self.weapon) + ", Armor: " + str(self.armor)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, Type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_width, tile_height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = self.type(Type)
        self.opened = 0
    def type(self, Type):
        if Type == "G":
            self.image = pygame.transform.scale(tile_G, (32,32))
            type = "G"
        if Type == "M":
            self.image = pygame.transform.scale(tile_M, (32,32))
            type = "M"
        if Type == "T":
            self.image = pygame.transform.scale(tile_T, (32,32))
            type = "T"
        if Type == "W":
            self.image = pygame.transform.scale(tile_W, (32,32))
            type = "W"
        if Type == "C":
            self.image = pygame.transform.scale(tile_C, (32,32))
            type = "C"
        if Type == "D":
            self.image = pygame.transform.scale(tile_D, (32,32))
            type = "D"
        return type
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, Type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32,32)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = self.type(Type, x, y)
        self.energy = 0
        self.hitanimation = 0
    def type(self, Type, x, y):
        if Type == "bandit":
            self.image = pygame.transform.scale(bandit, (32,32))
            self.health = random.randrange(35,51)
            self.strength = random.randrange(5,9)
            self.defense = random.randrange(3,8)
            self.speed = 4
            self.exp = random.randrange(50,81)
            mtype = "bandit"
        if Type == "monster":
            self.image = pygame.transform.scale(monster, (92,92))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            mtype = "monster"
            self.health = random.randrange(80,121)
            self.strength = random.randrange(10, 19)
            self.defense = random.randrange(8, 14)
            self.speed = 2
            self.exp = random.randrange(70,101)
        return mtype



def main():
    pygame.display.set_caption("the realest video game out there")
    intro = play = endscreen = True
    clock = pygame.time.Clock()
    elapsedtime = 0
    tile_group = pygame.sprite.Group()
    chest_group = pygame.sprite.Group()
    nopasstile_group = pygame.sprite.Group()
    room1 = [
        "MMMMMMMMMMMMMMMMMMMMMMMMMMMDMMMM", #1
        "MMMMMMMMMMMMMMMGGGGGGGGGGGGGGGGG", #2
        "MMMMMMMMMMMMMMMGGGGGGGGGGGGGGGGG", #3
        "MMMMMMMMMMMMMMCTGGGGGGGGGGGGGGGG", #4
        "MMMMMMMMMMMGGTGGGGTGGGGGGGGGGGGG", #5
        "GTCGGTGGGGGGTGGGGGGGGGGGGGGGGGGG", #6
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG", #7
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG", #8
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGTGGGG", #9
        "GGGGGGGGGTGGGGGGGGGGGGGGGGGGGGGG", #10
        "GGGGGGGGGGGGGGGGTGGGGGGGGGGGGGGG", #11
        "GGGGGGGGGGGGGGGGGGGGGGGGGTGGTGGG", #12
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG", #13
        "GGGGGGGGGGTGGGGGGGGGGGGGGGGGGGGG", #14
        "GGGGGTGCGGGGGGGGGGGGGGGGGGGGGGWW", #15
        "GGGGGGGGGGGGGGGGGGGGGGTGGGWWWWWW", #16
        "GGGGGGGGGGGGGGGGGTGGGGGGGWWWWWWW", #17
        "GGGTGGGGGGGGGGGGGGGGWWWWWWWWWWWW", #18
        "GGGGGGGGGGGGGGTGGGGWWWWWWWWWWWWW", #19
        "GGGGGGGGGGGGGGGGGWWWWWWWWWWWWWWW", #20
    ]
    x = y = 0
    for row in room1:
        for col in row:
            if col == "M":
                p = Tile(x, y, "M")
                nopasstile_group.add(p)
            if col == "G":
                p = Tile(x, y, "G")
                tile_group.add(p)
            if col == "T":
                p = Tile(x, y, "T")
                nopasstile_group.add(p)
            if col == "C":
                p = Tile(x, y, "C")
                chest_group.add(p)
            if col == "R":
                p = Tile(x, y, "R")
                nopasstile_group.add(p)
            if col == "W":
                p = Tile(x, y, "W")
                nopasstile_group.add(p)
            if col == "D":
                p = Tile(x, y, "D")
                nopasstile_group.add(p)
            x += 32
        y += 32
        x = 0

    m1 = Monster(480, 224, "bandit")
    m2 = Monster(224, 448, "bandit")
    m3 = Monster(960, 320, "bandit")
    b1 = Monster(832, 32, "monster")
    monster_group = pygame.sprite.Group()
    monster_group.add(m1, m2, m3, b1)
    hero = Hero(100, 7, 2, 7, "Dagger", "None", "MachoMan")




    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                pygame.display.flip()
                #sound["beep"].play()
                pygame.time.wait(1)
                intro = False
        introfont = pygame.font.Font(None, 100)
        introfont2 = pygame.font.Font(None, 60)
        introtitle = introfont.render("WELCOME TO MY GAME", 1, black)
        introtitle2 = introfont2.render("PRESS ENTER OR CLICK TO START", 1, black)
        introtitlepos = introtitle.get_rect()
        introtitle2pos = introtitle.get_rect()
        introtitlepos.centerx = screen.get_rect().centerx
        introtitlepos.centery = screen.get_rect().centery-200
        introtitle2pos.centerx = screen.get_rect().centerx+50
        introtitle2pos.centery = screen.get_rect().centery+200
        screen.fill(white)
        screen.blit(introtitle,introtitlepos)
        screen.blit(introtitle2,introtitle2pos)


        clock.tick(fps)
        pygame.display.flip()

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
                sys.exit()
        elapsedtime += 1


        monster_group.update()
        hero.update(nopasstile_group, chest_group, monster_group, kills, tile_group, fighting)
        chest_group.update()
        tile_group.update(hero)
        nopasstile_group.update(hero)
        screen.fill(white)
        tile_group.draw(screen)
        chest_group.draw(screen)
        nopasstile_group.draw(screen)
        monster_group.draw(screen)
        screen.blit(hero.image, (hero.rect.x, hero.rect.y))



        clock.tick(fps)
        pygame.display.flip()


if __name__ == "__main__":
    main()