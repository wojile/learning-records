import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,temp_set,screen):
        """
        初始化飞船并设置其初始位置
        """
        super(Ship,self).__init__()
        self.screen = screen
        self.settings = self.temp_set # 让飞船能获得其速度设置

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect() #存储屏幕矩形

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0 :
            self.center -= self.settings.ship_speed_factor

        # 根据self.center更新rect
        self.rect.centerx = self.center


    def center_ship(self):
        self.center = self.screen_rect.centerx

    def blitme(self):
        """
        在指定位置绘制飞船
        """
        self.screen.blit(self.image, self.rect)