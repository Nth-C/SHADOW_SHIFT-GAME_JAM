import pygame as pg

class Waves:
    def __init__(self, list_of_waves: list[pg.sprite.Group]):
        # list avec un list d'enemies
        self.list_of_waves = list_of_waves
        self.current_index = 0
        # si la salle n'a pas commencer ou qu'elle est fini false
        self.is_active = False

    def start_wave(self):
        if not self.room_is_clear():
            self.is_active = True

    def wave_update(self, player, walls: list[pg.Rect] | None = None):
        if self.is_active and not self.room_is_clear():
            for enemy in self.list_of_waves[self.current_index]:
                enemy.update(player, walls)

    def draw_waves(self, screen, scroll):
        if self.is_active and not self.room_is_clear():
            for enemy in self.list_of_waves[self.current_index]:
                enemy_move = scroll.apply(enemy.rect)
                enemy.draw_aggro_range(screen, enemy_move)
                screen.blit(enemy.image, enemy_move)
                enemy.draw_hp_bar(screen, enemy_move)

    def update_wave_status(self):
        if self.room_is_clear() or not self.is_active:
            return

        if len(self.list_of_waves[self.current_index]) == 0:
            self.is_active = False
            self.current_index += 1

    def room_is_clear(self) -> bool:
        return self.current_index >= len(self.list_of_waves)
    
    def get_current_enemies(self) -> pg.sprite.Group:
        if self.room_is_clear() or not self.is_active:
            return pg.sprite.Group()
        
        return self.list_of_waves[self.current_index]
