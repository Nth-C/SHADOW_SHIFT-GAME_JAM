import pygame as pg


def dessiner_lumiere_degradee(
    surface: pg.Surface, x: int, y: int, rayon: int, obscurite_alpha: int = 160
):
    rayon = max(1, int(rayon))
    temp_surf = pg.Surface((rayon * 2, rayon * 2), pg.SRCALPHA)
    temp_surf.fill((0, 0, 0, 0))

    for distance in range(rayon, -1, -2):
        intensite = (1 - (distance / rayon)) ** 1.3
        alpha = int(obscurite_alpha * intensite)
        pg.draw.circle(temp_surf, (0, 0, 0, alpha), (rayon, rayon), distance)

    surface.blit(temp_surf, (x - rayon, y - rayon), special_flags=pg.BLEND_RGBA_SUB)


def get_map_objects(tmx_data):
    if not tmx_data:
        return []
    return getattr(tmx_data, "objects", [])


def iter_light_sources(tmx_data):
    for obj in get_map_objects(tmx_data):
        name = str(getattr(obj, "name", "") or "").lower()
        if name in {"lampe", "light", "source", "lamp"}:
            properties = getattr(obj, "properties", {}) or {}
            rayon = int(properties.get("rayon", properties.get("radius", 150)))
            w = getattr(obj, "width", 0) or 0
            h = getattr(obj, "height", 0) or 0
            cx = obj.x + (w / 2 if w > 0 else 0)
            cy = obj.y + (h / 2 if h > 0 else 0)
            yield cx, cy, rayon


def iter_dark_areas(tmx_data):
    for obj in get_map_objects(tmx_data):
        name = str(getattr(obj, "name", "") or "").lower()
        if name in {"ombre", "shadow", "dark", "obscurite"}:
            x = int(getattr(obj, "x", 0))
            y = int(getattr(obj, "y", 0))
            width = int(getattr(obj, "width", 0))
            height = int(getattr(obj, "height", 0))
            yield x, y, width, height


def render_lights(
    surface_lumiere: pg.Surface,
    tmx_data,
    camera_offset=(0, 0),
    obscurite_alpha: int = 110,
):
    if surface_lumiere is None:
        return

    surface_lumiere.fill((0, 0, 0, obscurite_alpha))

    if not tmx_data:
        return

    offset_x, offset_y = camera_offset

    for lampe_x, lampe_y, rayon in iter_light_sources(tmx_data):
        screen_x = int(lampe_x + offset_x)
        screen_y = int(lampe_y + offset_y)
        dessiner_lumiere_degradee(
            surface_lumiere, screen_x, screen_y, rayon, obscurite_alpha
        )

    for x, y, width, height in iter_dark_areas(tmx_data):
        rect_ombre = pg.Rect(
            int(x + offset_x), int(y + offset_y), int(width), int(height)
        )
        pg.draw.rect(
            surface_lumiere, (0, 0, 0, min(255, obscurite_alpha + 60)), rect_ombre
        )


def draw_light_objects(screen: pg.Surface, tmx_data, camera_offset=(0, 0)):
    if not tmx_data:
        return

    offset_x, offset_y = camera_offset

    for obj in get_map_objects(tmx_data):
        name = str(getattr(obj, "name", "") or "").lower()
        if name in {"lampe", "light", "source", "lamp"}:
            image = getattr(obj, "image", None)
            if image is not None:
                screen.blit(image, (int(obj.x + offset_x), int(obj.y + offset_y)))
