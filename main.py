import pygame
import pygame_menu
from level import *
import character as character_module
import tile as tile_module
import Menu as menu_module

def create_theme_menu():
    myimage = pygame_menu.baseimage.BaseImage(
        image_path="data/image.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
        drawing_offset=(0, 0)
    )
    mytheme = pygame_menu.Theme(background_color=myimage,
                                      title_background_color=(255, 158, 158),
                                      title_font_shadow=True,
                                      widget_padding=27)
    return mytheme


def start_menu(screen, size_screen, theme_menu=None):
    menu = pygame_menu.Menu(
        height=size_screen[1],
        theme=theme_menu,
        title='Добро пожаловать',
        width=size_screen[0]
    )
    menu.add.button("Начать игру", lambda: game(screen, background_game_img))
    menu.add.button("Выход", pygame_menu.events.EXIT)
    menu.mainloop(screen)


def win(screen, background_game_img):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background_game_img, (0, 0))
        pygame.display.flip()

def game_over(screen, background_game_img):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                running = False
                game()
        screen.blit(background_game_img, (12, 0))
        pygame.display.flip()





def game(screen, background_game_img):
    # создадим группу, содержащую все спрайты
    FPS = 60
    tick = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player_group.update(event)
        screen.fill((0, 0, 0))
        screen.blit(background_game_img, (0, 0))
        if not player_group:
            running = False
            game_over(screen, background_game_img)
        # изменяем ракурс камеры
        camera.update(player, width, height)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update()
        player.check_collide(platform_group, enemy_group)
        if player.go_in_house(control_point_group):
            running = False
            win(screen, background_game_img)
        all_sprites.update()



        tiles_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        tick += 1
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    pygame.init()
    background_game_img = pygame.image.load("data/background.png")
    size = width, height = 700, 400
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Редиска')
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    control_point_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    lvl = Level('data/lvl.txt')
    player, level_x, level_y = lvl.generate_level(tile_module,  character_module, player_group, enemy_group, tiles_group, platform_group, control_point_group, all_sprites)
    camera = Camera()
    start_menu(screen, size, create_theme_menu())