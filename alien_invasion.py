import sys

import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
            (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion ———— by 王胜")
    
    # 创建Play按钮
    play_button = Button(ai_settings,screen,"Play")
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 在窗口右上角创建记分牌
    scoreboard = Scoreboard(ai_settings,screen,stats)
    # 创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组和一个外星人的编组
    bullets = Group()
    aliens = Group()
    
    gf.create_fleet(ai_settings,screen,aliens,ship)
    
    # 读取最高得分数据
    gf.read_high_score(stats,scoreboard)
    
    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,play_button,
                ship,aliens,bullets,scoreboard)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,aliens,bullets,ship,stats,scoreboard)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets,scoreboard)
               
        # 每次循环时都重绘屏幕,并切换到新屏幕
        gf.update_screen(ai_settings,stats,ship,screen,bullets,aliens,play_button,scoreboard)
        
run_game()
