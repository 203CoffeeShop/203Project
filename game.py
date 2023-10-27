import pygame
from config import *
from sys import exit
import math

pygame.init()

#Creating the window
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
#FPS
clock = pygame.time.Clock()

#Loads images
background = pygame.transform.scale(pygame.image.load("background.png").convert(), (WIN_WIDTH, WIN_HEIGHT))

#Player information
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("player.png").convert_alpha(), 0, PLAYER_SIZE)
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = 8
        self.shoot = False
        self.shoot_cooldown = 0
        self.health = 100
        
    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - self.hitbox_rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    def player_hit(self):
        hits = pygame.sprite.spritecollide(self, enemy_group, False)
        if hits:
            self.health = self.health - 1
            if self.health <= 0:
                self.kill()

            print("hit")
            print(self.health)
            pygame.display.update()

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed

        if self.velocity_x != 0 and self.velocity_y != 0: #moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)
        
        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot - False

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            spawn_bullet_pos = self.pos
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)


    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

#Bullet information
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.05)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.x_velocity = math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_velocity = math.sin(self.angle * (2*math.pi/360)) * self.speed
        self.bullet_lifetime = 750
        self.spawn_time = pygame.time.get_ticks() # gets the specific time that the bullet was created
    
    def bullet_movement(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()
    
    def update(self):
        hits = pygame.sprite.spritecollide(self, enemy_group, False)
        if hits and player.shoot == True:
            self.kill()
        self.bullet_movement()

#Enemy infomation
class Enemy1(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.position = pygame.math.Vector2(position)
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = 4
        self.health = 3

    def hunt_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2()
        
        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def get_vector_distance(self, vector_1, vector_2):
        return(vector_1 - vector_2).magnitude()

    def update(self):
        hits = pygame.sprite.spritecollide(self, bullet_group, False)
        if hits and player.shoot == True:
            self.health -= 1
            if self.health <= 0:
                self.kill()
                print("Enemy killed")
        elif hits and player.shoot == False:
            player.player_hit()

        self.hunt_player()

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.position = pygame.math.Vector2(position)
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = 4
        self.health = 3

    def hunt_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2()
        
        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def get_vector_distance(self, vector_1, vector_2):
        return(vector_1 - vector_2).magnitude()

    def update(self):
        hits = pygame.sprite.spritecollide(self, bullet_group, False)
        if hits and player.shoot == True:
            self.health -= 1
            if self.health <= 0:
                self.kill()
                print("Enemy killed")
        elif hits and player.shoot == False:
            player.player_hit()

        #Doesn't work fully, trying smth
        # collision_tolerance = 10
        # collide = pygame.sprite.spritecollide(self, enemy_group, False)
        # if collide:
        #     if abs(enemy2.rect.top - self.rect.bottom) < collision_tolerance > 0:
        #         self.speed *= -1
        #     if abs(enemy2.rect.bottom - self.rect.top) < collision_tolerance < 0:
        #         self.speed *= -1
        #     if abs(enemy2.rect.right - self.rect.left) < collision_tolerance < 0:
        #         self.speed *= -1
        #     if abs(enemy2.rect.left - self.rect.right) < collision_tolerance > 0:
        #         self.speed *= -1


        self.hunt_player()

#Sotring of sprites
all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = Player()
enemy1 = Enemy1((400,400))
enemy2 = Enemy2((600,600))

all_sprites_group.add(player)
all_sprites_group.add(enemy1)
enemy_group.add(enemy1)

all_sprites_group.add(enemy2)
enemy_group.add(enemy2)

#Loop that runs the game
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0,0))

    all_sprites_group.draw(screen)
    all_sprites_group.update()
    # pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    # pygame.draw.rect(screen, "yellow", player.rect, width=2)

    pygame.display.update()
    clock.tick(FPS)