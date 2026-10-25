"""
Run this script to try out the cart pole environment yourself
use the arrow keys to push the cart left or right and try to keep the pole balanced for as long as possible
Note the game has been slowed down here. It's almost impossible at full speed. 
You can change the clock.tick() value to make it faster or slower.
"""

from gymnasium.envs.classic_control import CartPoleEnv
import pygame

# Initialize environment with human render mode
env = CartPoleEnv(render_mode="human")
observation, info = env.reset()

# Default action (0 = Push Left, 1 = Push Right)
action = 0

running = True
clock = pygame.time.Clock()

print("CartPole Human Control")
print("----------------------")
print("LEFT Arrow  : Push Left")
print("RIGHT Arrow : Push Right")
print("ESC / Close : Quit")

while running:
    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        action = 0
    elif keys[pygame.K_RIGHT]:
        action = 1
    elif keys[pygame.K_ESCAPE]:
        running = False

    # x, x_dot, theta, theta_dot = observation
    # z = (0.224*x + 0.294*x_dot + 1.066*theta + 0.547*theta_dot - 0.192)
    # action = 1 if z > 0 else 0

    # Step the environment with current key action
    observation, reward, terminated, truncated, info = env.step(action)

    # Reset environment if game over (pole falls or cart leaves bounds)
    if terminated or truncated:
        observation, info = env.reset()

    # Set to 10 hz - change to 50 hz for full speed
    clock.tick(10)

env.close()
pygame.quit()