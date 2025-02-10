# animation.py
import pygame
import settings

class Animation:
    def __init__(self, image, frame_width, frame_height, num_frames, frame_rate, loop=True):
        self.image = image
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.frame_rate = frame_rate  # in milliseconds per frame
        self.loop = loop
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False
        self.frames = []
        self.last_update = pygame.time.get_ticks()
        self._load_frames()

    def _load_frames(self):
        for i in range(self.num_frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.image.subsurface(rect).copy()
            # Scale the frame according to settings.SCALE.
            scaled_frame = pygame.transform.scale(
                frame_image, 
                (int(self.frame_width * settings.SCALE), int(self.frame_height * settings.SCALE))
            )
            self.frames.append(scaled_frame)

    def update(self):
        if self.finished:
            return
        now = pygame.time.get_ticks()
        delta = now - self.last_update
        self.elapsed_time += delta
        self.last_update = now
        if self.elapsed_time > self.frame_rate:
            self.elapsed_time = 0
            self.current_frame += 1
            if self.current_frame >= self.num_frames:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.num_frames - 1
                    self.finished = True

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.elapsed_time = 0
        self.finished = False
        self.last_update = pygame.time.get_ticks()
