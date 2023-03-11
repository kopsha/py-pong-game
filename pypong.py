#!/usr/bin/env python3
from picasso import PicassoEngine
from palettes import BLACK, WHITE
from collections import namedtuple

import pygame


Point = namedtuple("Point", ["x", "y"])

WINDOW_SIZE = 1024, 768
WIDTH, HEIGHT = WINDOW_SIZE
MIDDLE = WIDTH // 2
THICKNESS = 8

STICK_WIDTH = 20
STICK_HEIGHT = 150
STICK_VELOCITY = 13

LEFT_LANE = 80
RIGHT_LANE = WIDTH - LEFT_LANE - STICK_WIDTH


class PyPongGame(PicassoEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_counter = 0
    
        self.left_player = Point(LEFT_LANE, 100)
        self.right_player = Point(RIGHT_LANE, 100)

        self.left_up = False
        self.left_down = False
        self.right_up = False
        self.right_down = False

    def post_init(self):
        pass

    def on_paint(self):
        self.update_player_moves()
        
        self.draw_field()
        self.draw_stick(self.left_player)
        self.draw_stick(self.right_player)

        self.frame_counter += 1
        if self.frame_counter % 1000 == 0:
            print(f" >> rendered {self.frame_counter // 1000}k frames")

    def on_click(self, event):
        x, y = event.pos

    def on_mouse_motion(self, event):
        pass

    def on_key(self, event):
        if event.key == pygame.K_ESCAPE:
            bye = pygame.event.Event(pygame.QUIT)
            pygame.event.post(bye)
            return
        
        pressed = pygame.key.get_pressed()
        self.left_up = pressed[pygame.K_w]
        self.left_down = pressed[pygame.K_s]
        self.right_up = pressed[pygame.K_UP]
        self.right_down = pressed[pygame.K_DOWN]
    
    def update_player_moves(self):
        if self.left_up and self.left_player.y > 0:
            new_y = self.left_player.y - STICK_VELOCITY
            self.left_player = Point(self.left_player.x, new_y)
        elif self.left_down and self.left_player.y < HEIGHT - STICK_HEIGHT:
            new_y = self.left_player.y + STICK_VELOCITY
            self.left_player = Point(self.left_player.x, new_y)

        if self.right_up and self.right_player.y > 0:
            new_y = self.right_player.y - STICK_VELOCITY
            self.right_player = Point(self.right_player.x, new_y)
        elif self.right_down and self.right_player.y < HEIGHT - STICK_HEIGHT:
            new_y = self.right_player.y + STICK_VELOCITY
            self.right_player = Point(self.right_player.x, new_y)

    def draw_field(self):
        self.screen.fill(BLACK)
        N = 20
        for i in range(N):
            center = MIDDLE, (i * HEIGHT) // N
            pygame.draw.circle(self.screen, WHITE, center, THICKNESS)

    def draw_stick(self, position):
        r = pygame.Rect(position.x, position.y, STICK_WIDTH, STICK_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, r)


def main():
    with PyPongGame(window_size=WINDOW_SIZE) as engine:
        engine.post_init()
        engine.run()


if __name__ == "__main__":
    main()
