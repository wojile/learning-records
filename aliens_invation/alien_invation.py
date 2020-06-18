
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien

def run_game():

    #初始化游戏并创建屏幕对象
    pygame.init()
    # screen = pygame.display.set_mode((1200,800))
    temp_set = Settings()
    screen = pygame.display.set_mode((temp_set.width,temp_set.height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(temp_set, screen, "Play")

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(temp_set)
    sb = Scoreboard(settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(temp_set, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一个外星人编组
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(temp_set, screen, ship, aliens)

    #开始游戏主循环
    while True:
        # for event in pygame.event.get(): #监听键盘和鼠标事件
        #     if event.type == pygame.QUIT:
        #         sys.exit()
        gf.check_events(temp_set,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(temp_set, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(temp_set, screen, stats, sb, ship, aliens, bullets)
        # screen.fill(temp_set.bg_color) #每次循环时都重绘屏幕
        # ship.blitme()
        # pygame.display.flip() #让最近绘制的屏幕可见
        gf.update_screen(temp_set, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
