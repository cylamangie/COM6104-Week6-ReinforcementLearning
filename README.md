# COM6104-Week6-ReinforcementLearning
COM6104 Week 6 lab — Reinforcement Learning with a custom drone landing environment, using Gymnasium, Stable Baselines3 (PPO), and OpenCV visualization.

# Reinforcement Learning Lab – Week 6

## 📌 Overview
This project implements a **custom reinforcement learning environment** for drone landing, built with **Gymnasium**.  
The agent is trained using **Stable Baselines3 (PPO)** to safely land a drone while managing fuel, velocity, and position.  
The environment includes **reward shaping** and **OpenCV visualization**.

> 📝 **Note**: This is the **sixth lab assignment** for **COM6104 – Topics in Data Science and Artificial Intelligence**.

---

## 🎯 Motivation
Reinforcement learning is a powerful paradigm for training agents to make sequential decisions.  
This lab highlights:
- How to design a custom environment with **observation and action spaces**.  
- How to implement **reward shaping** for safe landings.  
- How to train an agent with **Stable Baselines3 PPO**.  
- How to visualize the simulation with **OpenCV**.

---

## ⚙️ Files
- **`drone_engine.py`** → Drone physics engine (`DroneEngine`).  
- **`drone_env.py`** → Custom Gymnasium environment (`DroneLandingEnv`).  
- **`reinforcement_learning_drone.ipynb`** → PPO training and simulation loop.  

---

## 📊 Key Features
- **Observation space:** Drone position, velocity, and fuel.  
- **Action space:** Discrete actions (stay, left, up, right).  
- **Reward shaping:**  
  - Penalties for height, velocity, position, and fuel usage.  
  - Large positive reward for safe landing.  
  - Large negative reward for crashing.  
- **Visualization:** Real-time OpenCV rendering with landing pad, drone, and status messages.

---

## 🚀 How to Run
Install dependencies:
```bash
pip install -r requirements.txt
```

## 📚 Course Context
Completed as part of COM6104 – Topics in Data Science and Artificial Intelligence at The Hang Seng University of Hong Kong.

## 💡 Reflection
This lab helped me understand how to design a custom RL environment and apply reward shaping to guide agent behavior.
I learned how to integrate Stable Baselines3 PPO with Gymnasium and visualize training outcomes with OpenCV.
It reinforced the importance of balancing exploration, reward design, and simulation realism in reinforcement learning.

## 📚 Acknowledgements
Parts of this code were adapted from COM6104 lab materials provided by the instructor.
This repository is licensed under the MIT License, which permits reuse and modification with proper attribution.
