import gymnasium as gym
from gymnasium import spaces
import numpy as np
from exercise.game import DroneEngine
import cv2


class DroneLandingEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.engine = DroneEngine()

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=np.array([-20, -5, -10, -10, 0]),
            high=np.array([20, 25, 10, 10, 100]),
            dtype=np.float32,
        )
        self.width, self.height = 600, 400

    def _get_obs(self):
        return np.array(
            [
                self.engine.x,
                self.engine.y,
                self.engine.vel_x,
                self.engine.vel_y,
                self.engine.fuel,
            ],
            dtype=np.float32,
        )

    def step(self, action):
        is_safe, is_crash = self.engine.update(action)
        
        # Basic survival reward (the longer you survive the better, but keep it small)
        reward = -0.05   # Small penalty each step to encourage faster landing

        # Height-related: closer to the ground gives positive tendency (but don’t give big rewards too early)
        if self.engine.y > 0:
            reward -= 0.005 * self.engine.y          # Height penalty (optional, helps descend faster)
        
        # Position: strongly encourage staying near the center
        reward -= 0.25 * abs(self.engine.x)          # Original 0.1 was too weak, increased

        # Velocity penalty (very important!)
        reward -= 0.15 * abs(self.engine.vel_x)      # Horizontal velocity should not be too large
        reward -= 0.4  * abs(self.engine.vel_y)      # Vertical velocity must be small (critical for landing)
        
        # Fuel usage penalty (avoid burning fuel just to hover)
        if action != 0:
            reward -= 0.08                           # Extra penalty for each fuel unit spent

        # Terminal condition rewards/penalties (override accumulated values)
        terminated = False
        
        if is_safe:
            reward += 150.0                          # Big reward for successful landing
            terminated = True
        elif is_crash:
            reward -= 100.0                          # Big penalty for crashing
            terminated = True
        elif self.engine.y <= 0:
            # Catch any other boundary cases
            reward -= 50.0
            terminated = True

        return self._get_obs(), reward, terminated, False, {}


    def reset(self, seed=None, options=None):
        self.engine.reset()
        return self._get_obs(), {}

    def render(self):
        # 1. Create a blank black image
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # 2. Convert Engine Coordinates to Pixel Coordinates
        # Center x=0 (scale by 20), Ground y=0 (from bottom)
        px = int(self.engine.x * 20 + self.width // 2)
        py = int(self.height - (self.engine.y * 15))

        # 3. Draw the Landing Pad (Green rectangle at the bottom center)
        cv2.rectangle(
            img,
            (self.width // 2 - 40, self.height - 10),
            (self.width // 2 + 40, self.height),
            (0, 255, 0),
            -1,
        )

        # 4. Draw the Drone (Yellow circle)
        if self.engine.last_status == "crashed":
            # Draw a red "explosion" star/circle
            cv2.circle(img, (px, 0), 25, (0, 0, 255), -1)
            cv2.putText(
                img,
                "CRASHED!",
                (self.width // 2 - 80, self.height // 2),
                cv2.FONT_HERSHEY_TRIPLEX,
                1.5,
                (0, 0, 255),
                3,
            )
        elif self.engine.last_status == "landed":
            # Draw a green "success" circle
            cv2.circle(img, (px, py), 15, (0, 255, 0), -1)
            cv2.putText(
                img,
                "SUCCESS",
                (self.width // 2 - 80, self.height // 2),
                cv2.FONT_HERSHEY_TRIPLEX,
                1.5,
                (0, 255, 0),
                3,
            )
        else:
            # Standard Yellow Drone
            cv2.circle(img, (px, py), 10, (0, 255, 255), -1)

        # 5. Overlay Text Info
        cv2.putText(
            img,
            f"Fuel: {int(self.engine.fuel)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            img,
            f"X: {int(self.engine.x)}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            img,
            f"Y: {int(self.engine.y)}",
            (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        # 6. Show the image
        cv2.imshow("RL Drone Simulation", img)

        # REQUIRED for OpenCV to actually render the window
        cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()
