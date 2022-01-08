import pygame
import random

pygame.init()  # initialize pygame
win = pygame.display.set_mode((850, 479))  # create window, the inside is tuple
pygame.display.set_caption("Penguin VS COVID")

walkRight = [pygame.image.load('PR1.png'), pygame.image.load('PR2.png'), pygame.image.load('PR3.png'),
             pygame.image.load('PR4.png'), pygame.image.load('PR5.png'), pygame.image.load('PR6.png'),
             pygame.image.load('PR7.png'), pygame.image.load('PR8.png'), pygame.image.load('PR9.png')]

walkLeft = [pygame.image.load('PL1.png'), pygame.image.load('PL2.png'), pygame.image.load('PL3.png'),
            pygame.image.load('PL4.png'), pygame.image.load('PL5.png'), pygame.image.load('PL6.png'),
            pygame.image.load('PL7.png'), pygame.image.load('PL8.png'), pygame.image.load('PL9.png')]
bg = pygame.image.load('bg_road.png')
char = pygame.image.load('PS.png')

bul = pygame.image.load('pro_bullet.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound("proFire.mp3")
hitSound = pygame.mixer.Sound("proHit.mp3")

music = pygame.mixer.music.load("proTrack.wav")
pygame.mixer.music.play(-1)

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x  # coordinate for create object/character
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # your speed
        self.up = False  # UP button
        self.down = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  # create the box area for measure collision

    def draw(self, win):  # Remind that win stand for window display at the top (not win the battle or sth)
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):  # if not standing, so it will move in some ways
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  # estimate closest value


    def hit(self):
        self.isJump = False  # debug for reset the character
        self.jumpCount = 10
        self.x = 5  # We are resetting the player position
        self.y = 301
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('Lives -1', 1, (255, 0, 0))
        win.blit(text, (426 - (text.get_width() / 2), 220))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101  # can't use break because it will not go to .quit() func at the bottom
                    pygame.quit()  # so it will 301 , it will not come inside the loop for sure

class Projectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        win.blit(bul, (self.x, self.y))

class Enemy(object):
    walk = [pygame.image.load('cvd1.png'), pygame.image.load('cvd2.png'), pygame.image.load('cvd3.png'),
                 pygame.image.load('cvd4.png'), pygame.image.load('cvd5.png'), pygame.image.load('cvd6.png'),
                 pygame.image.load('cvd7.png'), pygame.image.load('cvd8.png'), pygame.image.load('cvd9.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # This will define where our enemy starts and the end of their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10  # health for the enemy
        self.visible = True

    def draw(self, win):
        self.move()  # this for call the bottom func
        if self.visible:  # means if the character not dead, if it dead so disappear and = False
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walk[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walk[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  # Red
            pygame.draw.rect(win, (0, 128, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 5 * self.health, 10))  # Green
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # estimate closest value


    def move(self):
        if self.vel > 0:  # moving right
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:  # Change direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:  # moving left
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        print('Hit!')


# main loop
def main():
    font = pygame.font.SysFont("microsoftsansserif", 16, True)  # the third argument is for activate bold
    lost_font = pygame.font.SysFont("microsoftsansserif", 70, True)
    win_font = pygame.font.SysFont("microsoftsansserif", 70, True)
    man = Player(5, 301, 73, 64)
    shootLoop = 0
    bullets = []
    covids = []
    lives = 5
    score = 0
    lost = False
    lost_count = 0
    winner = False
    FPS = 27
    run = True

    def redrawGameWindow():
        win.blit(bg, (0, 0))  # built-in func for the paste every image include background too
        text = font.render('Score: ' + str(score), 1, (0, 0, 0))  # 1 is for anti-aliasing, just do it
        win.blit(text, (700, 10))
        man.draw(win)

        lives_label = font.render(f"Lives: {lives}", 1, (0, 128, 0))  # color
        win.blit(lives_label, (10, 10))  # position

        if len(covids) >= 1 or len(bullets) >= 1:
            for i in range(4):
                covids[i].draw(win)

            for bullet in bullets:
                bullet.draw(win)


        if lost:
            lost_label = lost_font.render("Game Over", 1, (0, 0, 0))
            win.blit(lost_label, (852 / 2 - lost_label.get_width() / 2, 220))

        if winner:
            winner_label = win_font.render("You are the Winner", 1, (0, 0, 0))
            win.blit(winner_label, (852 / 2 - winner_label.get_width() / 2, 220))

        pygame.display.update()

    while run:  # pygame must run in the loop
        clock.tick(FPS)  # 27 frame per sec
        redrawGameWindow()

        # for Lost the game
        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # for Win the game
        if score >= 60:
            winner = True
            lives = lives
            score = score

        for i in range(4):
            covids.append(Enemy(random.randint(95, 722), random.randint(370, 389), 64, 64, 780))
            # the collision between Man and Enemy cause damage
            if covids[i].visible == True:
                if man.hitbox[1] < covids[i].hitbox[1] + covids[i].hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                        covids[i].hitbox[1]:
                    if man.hitbox[0] + man.hitbox[2] > covids[i].hitbox[0] and man.hitbox[0] < covids[i].hitbox[0] + \
                            covids[i].hitbox[2]:
                        # if you are win, there sre no collision between player and enemy and no lives decrease and the game will be flow continuously
                        if not winner:
                            man.hit()
                            lives -= 1


            # the collision between Bullet and Enemy
            for bullet in bullets:
                if covids[i].visible == True:
                    if bullet.y - 6 < covids[i].hitbox[1] + covids[i].hitbox[3] and \
                            bullet.y + 6 > covids[i].hitbox[1]:  # for y
                        if bullet.x + 6 > covids[i].hitbox[0] and \
                                bullet.x - 6 < covids[i].hitbox[0] + covids[i].hitbox[2]:  # for x
                            hitSound.play()
                            covids[i].hit()

                            if not winner:  # if you are not win, so score add but if you are win, the score are constantly at 60
                                score += 1
                            bullets.pop(bullets.index(bullet))
                elif covids[i].visible == False:
                    covids.pop(i)

                if bullet.x < 800 and bullet.x > 0:
                    bullet.x += bullet.vel  # The bullets will move plus its vel
                else:
                    bullets.pop(bullets.index(bullet))


        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # press Keys zone
        keys = pygame.key.get_pressed()  # receive the key button and you saw the bottom, it will be list
        if keys[pygame.K_SPACE] and shootLoop == 0:
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1

            if len(bullets) < 10:  # cannot exceed 10 bullets on the screen
                bullets.append(
                    Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), facing))
                # This will create a bullet starting at the middle of the character

            shootLoop = 1

        # Left, Right ...
        if keys[pygame.K_LEFT] and man.x > man.vel:
            if keys[pygame.K_UP] and man.y - man.vel > 365 - man.height:
                man.y -= man.vel
                man.up = True
                man.down = False
                man.standing = False
                man.x -= man.vel ## same
                man.left = True
                man.right = False
            elif keys[pygame.K_DOWN] and man.y + man.vel < 462 - man.height:
                man.y += man.vel
                man.up = False
                man.down = True
                man.standing = False
                man.x -= man.vel ## same
                man.left = True
                man.right = False
            else:
                man.x -= man.vel  ## same
                man.left = True
                man.right = False
                man.standing = False

        elif keys[pygame.K_RIGHT] and man.x < 800 - man.width - man.vel:
            if keys[pygame.K_UP] and man.y - man.vel > 365 - man.height:
                man.y -= man.vel
                man.up = True
                man.down = False
                man.standing = False
                man.x += man.vel
                man.left = False
                man.right = True
            elif keys[pygame.K_DOWN] and man.y + man.vel < 462 - man.height:
                man.y += man.vel
                man.up = False
                man.down = True
                man.standing = False
                man.x += man.vel
                man.left = False
                man.right = True
            else:
                man.x += man.vel
                man.right = True
                man.left = False
                man.standing = False

        elif keys[pygame.K_UP] and man.y - man.vel > 365 - man.height:
            man.y -= man.vel
            man.up = True
            man.down = False
            man.standing = False
        elif keys[pygame.K_DOWN] and man.y + man.vel < 462 - man.height:
            man.y += man.vel
            man.down = True
            man.up = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0

def main_menu():
    title_font = pygame.font.SysFont("microsoftsansserif", 80, True)
    run = True
    while run:
        win.blit(bg, (0, 0))
        title_label = title_font.render("Click to Start", 1, (255, 255, 255))
        win.blit(title_label, (852/2 - title_label.get_width()/2, 220))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
