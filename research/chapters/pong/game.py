import random


class Vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)
    
    def mult(self, scaler: float) -> "Vector":
        return Vector(self.x * scaler, self.y * scaler)

    def __str__(self):
        return f"{self.x}, {self.y}"


class Pong:

    def __init__(self, paddle_length: float):
        self.ball_pos = Vector(0, 0)
        self.ball_vel = Vector(0, 0)
        self.paddle_pos = Vector(0, 0)
        self.paddle_length = paddle_length
    
    def reset(self, ball_pos: Vector, paddle_pos: Vector):
        self.ball_pos = ball_pos
        self.ball_vel = Vector(0, 0)
        self.paddle_pos = paddle_pos

    def start(self, ball_vel: Vector):
        self.ball_vel = ball_vel
    
    def paddle_move(self, speed: float, dt: float):
        self.paddle_pos.x += speed * dt
        if self.paddle_pos.x + self.paddle_length / 2 > 1.0:
            self.paddle_pos.x = 1.0 - self.paddle_length / 2
        elif self.paddle_pos.x - self.paddle_length / 2 < 0.0:
            self.paddle_pos.x = self.paddle_length / 2

    # Returns (is_game_over, is_paddle_bounced)
    def update(self, dt: float) -> tuple[bool, bool]:
        dv = self.ball_vel.mult(dt)
        self.ball_pos = self.ball_pos.add(dv)

        is_paddle_bounced = False

        if self.ball_pos.y <= 0:
            if (self.ball_pos.x < self.paddle_pos.x - self.paddle_length / 2 or
                self.ball_pos.x > self.paddle_pos.x + self.paddle_length / 2):
                return (True, False)
            else:
                self.ball_pos = Vector(self.ball_pos.x, -self.ball_pos.y)
                self.ball_vel.y *= -1
                is_paddle_bounced = True

        if self.ball_pos.y > 1.0:
            self.ball_pos = Vector(self.ball_pos.x, 1.0 - (self.ball_pos.y - 1.0))
            self.ball_vel.y *= -1

        if self.ball_pos.x < 0.0:
            self.ball_pos = Vector(-self.ball_pos.x, self.ball_pos.y)
            self.ball_vel.x *= -1
        
        if self.ball_pos.x > 1.0:
            self.ball_pos = Vector(1.0 - (self.ball_pos.x - 1.0), self.ball_pos.y)
            self.ball_vel.x *= -1

        return (False, is_paddle_bounced)


class GameInterface:

    def __init__(self, seed: int, dt: float, initial_ball_direction: Vector):
        self.rng = random.Random(seed)
        self.dt = dt
        self.paddle_speed = 1
        self.ball_speed = 0.5

        self.game = Pong(0.25)
        self.game.reset(Vector(0.5, 0.25), Vector(0.5, 0))
        self.game.start(initial_ball_direction.mult(self.ball_speed))
    
    def update(self, paddle_direction: int) -> tuple[bool, bool]:
        self.game.paddle_move(paddle_direction * self.paddle_speed, self.dt)
        return self.game.update(self.dt)

    def get_inputs(self, channels: int, min_prob: float, max_prob: float) -> list[int]:
        arr = [0] * channels
        index = min(int(self.game.ball_pos.x * channels), channels - 1)
        prob = min_prob + (1.0 - self.game.ball_pos.y) * (max_prob - min_prob)
        arr[index] = int(self.rng.random() < prob)
        return arr



if __name__ == "__main__":
    gi = GameInterface(1211, 1.0 / 20.0)
    print(gi.game.ball_pos)
    for i in range(25):
        #print(gi.update(), gi.game.ball_pos)
        gi.update()
        print(gi.get_inputs(10, 0.05, 0.75))
