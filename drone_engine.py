import numpy as np


class DroneEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = np.random.uniform(-10, 10)
        self.y = 20.0
        self.vel_y = 0.0
        self.vel_x = 0.0
        self.fuel = 100.0
        self.fuel_spent = 0.0
        self.last_status = "flying"

    def update(self, action: int):
        # Action: 0=Stay, 1=Left, 2=Up, 3=Right
        if action > 0 and self.fuel > 0:
            self.fuel -= 1
            if action == 1:
                self.vel_x -= 0.5
            elif action == 2:
                self.vel_x += 0.5
            else:
                self.vel_y += 0.25

        self.vel_y -= 0.1  # Gravity
        self.x += self.vel_x
        self.y += self.vel_y

        # Game over checks
        is_safe_landing = self.y <= 0 and abs(self.x) < 2 and abs(self.vel_y) < 1
        is_crash = self.y <= 0 and not is_safe_landing

        self.last_status = "flying"
        if is_safe_landing:
            self.last_status = "landed"
        if is_crash:
            self.last_status = "crashed"

        return is_safe_landing, is_crash
