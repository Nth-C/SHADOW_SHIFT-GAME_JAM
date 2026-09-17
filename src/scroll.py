
class Scroll:
    def __init__(self):
        self.x = 0
        self.y = 0

    # créer une camera temporaire pour faire la modificaiton
    def apply(self, rect):
        return rect.move(self.x, self.y)

    # calcule le décallage qui doit être appliqué au monde
    def scroll_update(self, target, width, height):
        self.x = -target.rect.centerx + (width // 2)
        self.y = -target.rect.centery + (height // 2)

        self.x = min(0, self.x)
        self.y = min(0, self.y)

        self.x = max(-(1024 - width), self.x)
        self.y = max(-(768 - height), self.y)
    