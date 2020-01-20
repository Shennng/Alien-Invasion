import pygame.font

from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """显示得分信息的类"""
    
    def __init__(self,ai_settings,screen,stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        # 显示得分信息时使用的字体设置
        self.text_color = (50,50,50)
        self.font = pygame.font.SysFont("Agency FB",40)
        
        # 准备初始图像
        self.prep_str_score()
        self.prep_num_score()
        self.prep_str_high_score()
        self.prep_num_high_score()
        self.prep_str_level()
        self.prep_num_level()
        self.prep_ships()
        
    def prep_str_score(self):
        """初始化字符串‘score’图像"""
        self.score_image = self.font.render("Scores: ",
            True,self.text_color,self.ai_settings.bg_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.centerx = self.screen_rect.right - 150
        self.score_image_rect.y = 0
        
    def prep_num_score(self):
        """初始化得分数据图像"""
        rounded_num_score = round(self.stats.score,-1)
        self.num_score = "{:,}".format(rounded_num_score)
        self.num_score_image = self.font.render(self.num_score,
            True,self.text_color,self.ai_settings.bg_color)
        self.num_score_image_rect = self.num_score_image.get_rect()
        self.num_score_image_rect.x = self.screen_rect.right - 100
        self.num_score_image_rect.y = 0
        
    def prep_str_high_score(self):
        """初始化字符串‘High Scores’图像"""
        self.high_score_image = self.font.render("High Scores: ",
            True,self.text_color,self.ai_settings.bg_color)
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.x = 10
        self.high_score_image_rect.y = 0
        
    def prep_num_high_score(self):
        """初始化最高得分数据"""
        self.num_high_score = "{:,}".format(self.stats.high_score)
        self.num_high_score_image = self.font.render(self.num_high_score,
            True,self.text_color,self.ai_settings.bg_color)
        self.num_high_score_image_rect = self.num_high_score_image.get_rect()
        self.num_high_score_image_rect.x = 180
        self.num_high_score_image_rect.y = 0
        
    def prep_str_level(self):
        """初始‘Level’图像"""
        self.level_image = self.font.render("Lv.",
            True,self.text_color,self.ai_settings.bg_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.x = self.screen_rect.right - 80
        self.level_image_rect.y = 45
        
    def prep_num_level(self):
        """初始等级数据"""
        self.num_level = str(self.stats.level)
        self.num_level_image = self.font.render(self.num_level,
            True,self.text_color,self.ai_settings.bg_color)
        self.num_level_image_rect = self.num_level_image.get_rect()
        self.num_level_image_rect.x = self.screen_rect.right - 35
        self.num_level_image_rect.y = 45
        
    def prep_ships(self):
        """显示还有多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.image = pygame.image.load('images\ship_icon.bmp')
            ship.rect.x = 570 + 35 * ship_number
            ship.rect.y = 10
            self.ships.add(ship)      
        
    def blitme(self):
        """绘制图像‘Scores:’和得分数据"""
        self.screen.blit(self.score_image,self.score_image_rect)
        self.screen.blit(self.num_score_image,self.num_score_image_rect)
        
        self.screen.blit(self.level_image,self.level_image_rect)
        self.screen.blit(self.num_level_image,self.num_level_image_rect)
        
        # 绘制飞船
        self.ships.draw(self.screen)
        
        self.screen.blit(self.high_score_image,self.high_score_image_rect)
        self.screen.blit(self.num_high_score_image,self.num_high_score_image_rect)
