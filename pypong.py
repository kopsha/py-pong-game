#!/usr/bin/env python3
from picasso import PicassoEngine
from palettes import BLACK, WHITE

import pygame

WINDOW_SIZE = 1000, 1000
WIDTH, HEIGHT = WINDOW_SIZE
MIDDLE = WIDTH // 2
THICKNESS = 3


class PyPongGame(PicassoEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_counter = 0

    def post_init(self):
        pass

    def on_paint(self):
        self.draw_field()
        self.frame_counter += 1
        if self.frame_counter % 1000 == 0:
            print(f" >> rendered {self.frame_counter // 1000}k frames")

    def on_click(self, event):
        x, y = event.pos

        if event.button == 1:  # left click
            print("left click", x, y)
        elif event.button == 3:  # right click
            print("right click", x, y)

    def on_mouse_motion(self, event):
        x, y = event.pos

    def on_key(self, event):
        if event.key == pygame.K_ESCAPE:
            bye = pygame.event.Event(pygame.QUIT)
            pygame.event.post(bye)
        elif event.key == pygame.K_F1:
            print("help yourself")
        elif event.key == pygame.K_KP_PLUS:
            print("increase velocity")
        elif event.key == pygame.K_KP_MINUS:
            print("decrease velocity")


    def draw_field(self):
        self.screen.fill(BLACK)
        top = MIDDLE, 0
        bottom = MIDDLE, HEIGHT
        # nimic
        
        pygame.draw.circle(self.screen, WHITE, bottom, THICKNESS)

        N = 50
        for i in range(N):
            center = MIDDLE, (i * HEIGHT) // N
            pygame.draw.circle(self.screen, WHITE, center, THICKNESS)


def main():
    with PyPongGame(window_size=WINDOW_SIZE) as engine:
        engine.post_init()
        engine.run()


if __name__ == "__main__":
    main()
