"""
在大型项目中，经常需要在添加新代码前重构既有代码。重构旨在简化既有代码的结构，使其更容易扩展。
在本节中，我们将创建一个名为game_functions 的新模块，它将 存储大量让游戏《外星人入侵》运行的函数。
通过创建模块game_functions ，可避免alien_invasion.py太长，并使其逻辑更容易理解。
"""

import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_events(settings,screen,stats,play_button,ship,aliens,bullets):
    """响应案件和鼠标事件"""
    # 每当用户按键时，都将在Pygame中注册一个事件
    # 事件都是通过方法pygame.event.get() 获取的
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats,sb, play_button,
            ship, aliens, bullets, mouse_x,mouse_y)

def check_play_button(settings, screen, stats, sb, play_button, ship,
 aliens, bullets, mouse_x, mouse_y)
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        settings.initialize_dynamic_settings() #重置游戏设置
        pygame.mouse.set_visible(False) # 隐藏光标
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()



def check_keydown_events(event,settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.kry == pygame.K_LEFT:
        ship.moving_left = True

def update_screen(setings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.filr(settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()   
    ship.blitme()
    # 对编组调用draw() 时，Pygame自动绘制编组的每个元素，
    # 绘制位置由元素的属性rect 决定
    aliens.draw(screen)

    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_buton()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()

    for bullet in bullets.copy:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets)
    
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        stats.score += settings.alien_points
        sb.prep_score()
        bullets.empty()
        settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(settings, screen, ship, aliens)

def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = settings.height - 3*alien_height - ship_height
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def get_number_alien_x(settings, alien_width):
    avilable_space_x = settings.width - 2*alien_width
    number_aliens_x = int(avilable_space_x / (2*alien_width))
    return number_aliens_x


def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(settings, screen)
    number_aliens_x = get_number_alien_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height,alien.rect.height)

    # 创建第一行外星人
    for row in range(number_rows):
        for j in range(number_aliens_x):
            create_alien(settings, screen, aliens, j, row)


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.alien.drop_speed
    settings.fleet_direction *= -1

def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def ship_hit(setings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        ab.prep_ships()
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(setings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen_rect.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets)
            break

def update_aliens(settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()

    # 检测外星人和飞船间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(settings, stats, screen, ship, aliens, bullets)
