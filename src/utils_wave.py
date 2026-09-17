import random

import pygame as pg

from enemies.enemy import Enemy


def get_enemies_of_waves(
    self, min_id_enemy, max_id_enemy, nb_enemies, hp=20
) -> pg.sprite.Group:
    id_enemies_selected: list[int] = []
    wave = pg.sprite.Group()

    for i in range(nb_enemies):
        rnd_int = random.randint(min_id_enemy, max_id_enemy)

        while rnd_int in id_enemies_selected:
            rnd_int = random.randint(min_id_enemy, max_id_enemy)
        id_enemies_selected.append(rnd_int)

        enemy = self.map.tmx_data.get_object_by_name("ennemi " + str(rnd_int))
        wave.add(Enemy(enemy.x, enemy.y, 50, hp=hp))

    return wave
