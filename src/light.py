import pygame as pg


def dessiner_lumiere_degradee(surface: pg.Surface, x: int, y: int, rayon: int, couleur_base=(255, 255, 255)):
    # Dessine un halo lumineux circulaire avec dégradé additif
    rayon = max(1, int(rayon))
    temp_surf = pg.Surface((rayon * 2, rayon * 2))
    temp_surf.fill((0, 0, 0))  # Le noir n'ajoute aucune lumière

    for distance in range(rayon, 0, -2):
        intensite = (1 - (distance / rayon)) ** 1.5
        couleur = tuple(int(c * intensite) for c in couleur_base)
        pg.draw.circle(temp_surf, couleur, (rayon, rayon), distance)

    # Ajoute la lumière sur la surface sombre globale
    surface.blit(temp_surf, (x - rayon, y - rayon), special_flags=pg.BLEND_RGB_ADD)


def _get_map_objects(tmx_data):
    if not tmx_data:
        return []
    return getattr(tmx_data, "objects", [])


def _iter_light_sources(tmx_data):
    for obj in _get_map_objects(tmx_data):
        name = str(getattr(obj, "name", "")).lower()
        if name in {"lampe", "light", "source", "lamp"}:
            properties = getattr(obj, "properties", {}) or {}
            rayon = int(properties.get("rayon", properties.get("radius", 150)))
            x = int(getattr(obj, "x", 0))
            y = int(getattr(obj, "y", 0))
            yield x, y, rayon


def _iter_dark_areas(tmx_data):
    for obj in _get_map_objects(tmx_data):
        name = str(getattr(obj, "name", "")).lower()
        if name in {"ombre", "shadow", "dark", "obscurite"}:
            x = int(getattr(obj, "x", 0))
            y = int(getattr(obj, "y", 0))
            width = int(getattr(obj, "width", 0))
            height = int(getattr(obj, "height", 0))
            yield x, y, width, height


def render_lights(surface_lumiere: pg.Surface, tmx_data, camera_offset=(0, 0), couleur_lumiere=(255, 255, 255)):
    # Crée un masque d'obscurité qui sera multiplié à l'écran
    if surface_lumiere is None:
        return

    # Fond sombre (ex: bleu nuit très sombre). La multiplication assombrira l'écran.
    surface_lumiere.fill((40, 40, 60))

    if not tmx_data:
        return

    offset_x, offset_y = camera_offset

    for lampe_x, lampe_y, rayon in _iter_light_sources(tmx_data):
        screen_x = int(lampe_x + offset_x)
        screen_y = int(lampe_y + offset_y)
        dessiner_lumiere_degradee(surface_lumiere, screen_x, screen_y, rayon, couleur_lumiere)

    for x, y, width, height in _iter_dark_areas(tmx_data):
        rect_ombre = pg.Rect(int(x + offset_x), int(y + offset_y), int(width), int(height))
        pg.draw.rect(surface_lumiere, (10, 10, 15), rect_ombre)


def draw_light_objects(screen: pg.Surface, tmx_data, camera_offset=(0, 0)):
    # Redessine les lampes au premier plan pour les préserver au-dessus du halo
    if not tmx_data:
        return

    offset_x, offset_y = camera_offset

    for obj in _get_map_objects(tmx_data):
        name = str(getattr(obj, "name", "")).lower()
        if name in {"lampe", "light", "source", "lamp"}:
            image = getattr(obj, "image", None)
            if image is not None:
                screen.blit(image, (int(obj.x + offset_x), int(obj.y + offset_y)))
