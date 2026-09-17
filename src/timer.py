import pygame as pg

class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.is_running = False

    def start(self):
        """Lance ou relance le chronomètre."""
        self.start_time = pg.time.get_ticks()
        self.is_running = True

    def stop(self):
        """Arrête le chronomètre et enregistre le temps final."""
        if self.is_running:
            self.end_time = pg.time.get_ticks()
            self.is_running = False

    def get_time_ms(self) -> int:
        """Renvoie le temps écoulé en millisecondes."""
        if self.is_running:
            return pg.time.get_ticks() - self.start_time
        return self.end_time - self.start_time

    def get_formatted_time(self) -> str:
        """Renvoie le temps formaté (ex: '02:45')."""
        total_time_ms = self.get_time_ms()
        secondes_totales = total_time_ms // 1000
        minutes = secondes_totales // 60
        secondes = secondes_totales % 60
        
        return f"{minutes:02d}:{secondes:02d}"