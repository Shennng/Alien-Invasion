import sys
from time import sleep

import pygame
import json

from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_play_button(ai_settings,screen,stats,play_button,
        ship,aliens,bullets,mouse_x,mouse_y,scoreboard):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        
        # 隐藏光标
        pygame.mouse.set_visible(False)
        
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        
        # 重置游戏等级,得分和最高得分
        scoreboard.prep_num_level()
        scoreboard.prep_num_score()
        scoreboard.prep_num_high_score()
        scoreboard.prep_ships()
        
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
    
        # 创建一群新的外星人,并将飞船放到屏幕中央
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()
        
def check_events(ai_settings,screen,stats,play_button,
                ship,aliens,bullets,scoreboard):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,
                ship,aliens,bullets,mouse_x,mouse_y,scoreboard)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,scoreboard):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1
        
        # 更新飞船数量记分牌数据
        scoreboard.prep_ships()
    
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
    
        # 创建一群新的外星人,并将飞船放到屏幕中央
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship()
    
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,scoreboard):
    """检查外星人是否碰到屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets,scoreboard)
    
    
def fire_bullet(ai_settings,screen,ship,bullets):
    """如果没有达到bullet_allowed,就发射一颗子弹"""
    # 创建一颗子弹，并将其加入编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width,alien_interval):
    """返回每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2*alien_interval
    number_aliens_x = int(available_space_x / (alien_interval + alien_width))
    return number_aliens_x
    
def get_number_aliens_rows(ai_settings,screen,alien_height,ship_height):
    """返回能容纳的外星人的行数"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_aliens_rows = int(available_space_y / (2 * alien_height))
    return number_aliens_rows
    
def create_alien(ai_settings,screen,aliens,alien_number,number_alien_row,alien_interval):
    """创建一个外星人,并将其放在当前行"""
    alien = Alien(ai_settings,screen)
    alien.x = (alien_interval + alien.rect.width)*alien_number + alien_interval
    alien.y = (2 * alien.rect.height)*number_alien_row + alien.rect.height
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)
    
def create_fleet(ai_settings,screen,aliens,ship):
    """创建外星人群"""
    # 创建一个外星人,并计算一行可容纳多少个外星人
    # 外星人间距为50px
    alien = Alien(ai_settings,screen)
    alien_interval = 50
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width,alien_interval)
    number_aliens_rows = get_number_aliens_rows(ai_settings,screen,alien.rect.height,ship.rect.height)
    
    # 创建多行外星人
    for number_alien_row in range(number_aliens_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,number_alien_row,alien_interval)
            
def update_bullets(ai_settings,screen,aliens,bullets,ship,stats,scoreboard):
    """更新子弹的rect的位置,并删除消失的子弹"""
    bullets.update()  # 为bullets编组中的每颗子弹调用bullet.update()    
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings,screen,bullets,aliens,ship,stats,scoreboard)        

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def save_high_score(stats):
    """保存最高得分到文件high_score.json"""
    filename = 'high_score.json'
    with open(filename,'w') as file_object:
        json.dump(stats.high_score,file_object)
        
def read_high_score(stats,scoreboard):
    """如果有最高得分数据,则读取它"""
    filename = 'high_score.json'
    try:
        with open(filename) as file_object:
            stats.high_score = json.load(file_object)
    except FileNotFoundError:
        pass
    else:
        scoreboard.prep_num_high_score()

def check_high_score(stats,scoreboard):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_num_high_score()
        save_high_score(stats)

def check_bullet_alien_collisions(ai_settings,screen,bullets,aliens,ship,stats,scoreboard):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中外星人
    # 如果是这样，就删除响应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    # 有子弹和外星人发生碰撞时,Pygame返回一个字典collisions
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_num_score()
        check_high_score(stats,scoreboard)
    
    if len(aliens) == 0:
        # 删除现有的子弹新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        
        # 一群外星人被消灭,等级提升1
        stats.level += 1
        scoreboard.prep_num_level()
        
        create_fleet(ai_settings,screen,aliens,ship)
           
def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移,并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,scoreboard):
    """检查是否有外星人位于屏幕边缘,并更新外星人的rect的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,scoreboard)
        
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,scoreboard)
    
def update_screen(ai_settings,stats,ship,screen,bullets,aliens,play_button,scoreboard):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    for alien in aliens.sprites():
        alien.blitme()
    
    # 绘制记分牌
    scoreboard.blitme()    
    # 如果游戏处于非活动状态,就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    
    pygame.display.flip()
    
