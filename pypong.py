#!/usr/bin/env python3
from picasso import PicassoEngine
from palettes import BLACK, WHITE, YELLOW, GRAY
from random import randint, choice
from dataclasses import dataclass

import pygame


WINDOW_SIZE = 1024, 768
WIDTH, HEIGHT = WINDOW_SIZE
MIDDLE = WIDTH // 2
WALLMARK_THICKNESS = 5

STICK_WIDTH = 20
STICK_HEIGHT = 150
STICK_VELOCITY = 13

BALL_THICKNESS = 13

LEFT_LANE = 80
RIGHT_LANE = WIDTH - LEFT_LANE - STICK_WIDTH


@dataclass
class Point:
    x: int
    y: int

    @property
    def pos(self):
        return self.x, self.y


class PyPongGame(PicassoEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_counter = 0

        self.left_up = False
        self.left_down = False
        self.right_up = False
        self.right_down = False

        self.left_player = Point(LEFT_LANE, 100)
        self.right_player = Point(RIGHT_LANE, 100)

        self.restart_game()

    def restart_game(self):
        # ball start from center in random direction
        self.ball = Point(MIDDLE, HEIGHT // 2)
        self.velocity = Point(
            choice((-1, 1)) * randint(5, 15),
            choice((-1, 1)) * randint(5, 15),
        )

    def post_init(self):
        pass

    def on_paint(self):
        self.update_player_moves()
        self.update_ball_move()

        self.draw_field()
        self.draw_stick(self.left_player)
        self.draw_stick(self.right_player)
        self.draw_ball()

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

    def update_ball_move(self):
        new_pos = Point(
            self.ball.x + self.velocity.x,
            self.ball.y + self.velocity.y,
        )

        if new_pos.x > (WIDTH - BALL_THICKNESS) or new_pos.x < (0 + BALL_THICKNESS):
            self.restart_game()
            return

        # wall reflections
        if new_pos.y > (HEIGHT - BALL_THICKNESS):
            over_y = new_pos.y - (HEIGHT - BALL_THICKNESS)
            new_pos.y -= over_y
            self.velocity.y = -self.velocity.y
        elif new_pos.y < (0 + BALL_THICKNESS):
            over_y = new_pos.y - (0 + BALL_THICKNESS)
            new_pos.y -= over_y
            self.velocity.y = -self.velocity.y
        elif (
            ((self.right_player.y - BALL_THICKNESS) <= new_pos.y <= (self.right_player.y + STICK_HEIGHT + BALL_THICKNESS))
            and
            ((self.right_player.x - BALL_THICKNESS) <= new_pos.x <= self.right_player.x)
        ):  # right player reflections
            over_x = new_pos.x - (self.right_player.x - BALL_THICKNESS)
            new_pos.x -= over_x
            self.velocity.x = -self.velocity.x
        elif (
            ((self.left_player.y - BALL_THICKNESS) <= new_pos.y <= (self.left_player.y + STICK_HEIGHT + BALL_THICKNESS))
            and
            ((self.left_player.x +  STICK_WIDTH) <= new_pos.x <= ((self.left_player.x +  STICK_WIDTH) + BALL_THICKNESS))
        ):  # left player reflections
            over_x = new_pos.x - ((self.left_player.x +  STICK_WIDTH) + BALL_THICKNESS)
            new_pos.x -= over_x
            self.velocity.x = -self.velocity.x

        self.ball = new_pos

    def draw_field(self):
        self.screen.fill(BLACK)
        N = 20
        for i in range(N):
            center = MIDDLE, (i * HEIGHT) // N
            pygame.draw.circle(self.screen, GRAY, center, WALLMARK_THICKNESS)

    def draw_stick(self, position):
        r = pygame.Rect(position.x, position.y, STICK_WIDTH, STICK_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, r)

    def draw_ball(self):
        pygame.draw.circle(self.screen, YELLOW, self.ball.pos, BALL_THICKNESS)


def main():
    with PyPongGame(window_size=WINDOW_SIZE) as engine:
        engine.post_init()
        engine.run()


if __name__ == "__main__":
    main()
