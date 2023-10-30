import sys
import pygame

def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    player = pygame.Rect(300, 220, 100, 100)
    screen_width, screen_height = 640, 480
    moving_rect = pygame.Rect(350, 350, 100, 100)
    x_speed, y_speed = 5, 5  # Initialize x_speed and y_speed
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.x -= 10
        if keys[pygame.K_d]:
            player.x += 10
        if keys[pygame.K_w]:
            player.y -= 10
        if keys[pygame.K_s]:
            player.y += 10

        moving_rect.x += x_speed
        moving_rect.y += y_speed

        if moving_rect.right >= screen_width or moving_rect.left <= 0:
            x_speed *= -1
        if moving_rect.bottom >= screen_height or moving_rect.top <= 0:
            y_speed *= -1

        collision_tolerance = 10
        if moving_rect.colliderect(player):
            if abs(player.top - moving_rect.bottom) < collision_tolerance and y_speed > 0:
                y_speed *= -1
            if abs(player.bottom - moving_rect.top) < collision_tolerance and y_speed < 0:
                y_speed *= -1
            if abs(player.right - moving_rect.left) < collision_tolerance and x_speed < 0:
                x_speed *= -1
            if abs(player.left - moving_rect.right) < collision_tolerance and x_speed > 0:
                x_speed *= -1

        screen.fill((40, 40, 40))
        pygame.draw.rect(screen, (150, 200, 20), player)
        pygame.draw.rect(screen, (200, 100, 20), moving_rect)  # Draw the moving rectangle

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
