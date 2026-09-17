import pygame as pg


def dessiner_lumiere_degradee(surface: pg.Surface, x: int, y: int, raidus: int, dark_alpha: int = 160):
    temp_surf = pg.Surface((raidus * 2, raidus * 2), pg.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0))

    for dist in range(raidus, -1, -2):
        intensity = (1 - (dist / raidus)) ** 1.3
        alpha = int(dark_alpha * intensity)
        pg.draw.circle(temp_surf, (0, 0, 0, alpha), (raidus, raidus), dist)

    surface.blit(temp_surf, (x - raidus, y - raidus), special_flags=pg.BLEND_RGBA_SUB)


def get_map_objects(tmx_data):
    light_list = []
    if tmx_data:
        light_list = tmx_data.objects
    return light_list


def iter_light_sources(tmx_data):
    lights = []
    for obj in get_map_objects(tmx_data):
        if obj.name and obj.name.lower() in ["lampe", "light", "source", "lamp"]:
            raidus = int(obj.properties.get("rayon", 150))

            center_x = obj.x + (obj.width / 2)
            center_y = obj.y + (obj.height / 2)

            lights.append((center_x, center_y, raidus))
    
    return lights


def iter_dark_areas(tmx_data):
    shadows = []
    for obj in get_map_objects(tmx_data):
        if obj.name and obj.name.lower() in ["lampe", "light", "source", "lamp"]:
            shadows.append((obj.x, obj.y, obj.width, obj.height))

    return shadows


def render_lights(surface_light: pg.Surface, tmx_data, camera_offset=(0, 0), dark_alpha: int = 110,):
    if surface_light and tmx_data:
        surface_light.fill((0, 0, 0, dark_alpha))
        offset_x, offset_y = camera_offset

        for led_x, led_y, radius in iter_light_sources(tmx_data):
            screen_x = led_x + offset_x
            screen_y = led_y + offset_y
            dessiner_lumiere_degradee(surface_light, screen_x, screen_y, radius, dark_alpha)

        for x, y, width, height in iter_dark_areas(tmx_data):
            rect_shadow = pg.Rect(x + offset_x, y + offset_y, width, height)
            pg.draw.rect(surface_light, (0, 0, 0, min(255, dark_alpha + 60)), rect_shadow)


def draw_light_objects(screen: pg.Surface, tmx_data, camera_offset=(0, 0)):
    if tmx_data:
        offset_x, offset_y = camera_offset

    for obj in get_map_objects(tmx_data):
        if obj.name and obj.name.lower() in ["lampe", "light", "source", "lamp"]:
            if hasattr(obj, "image") and obj.image:
                screen.blit(obj.image, (obj.x + offset_x, obj.y + offset_y))
