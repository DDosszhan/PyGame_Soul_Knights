# Soul Knight Inspired Game

## Overview
This is a 2D action game inspired by *Soul Knight*, built using **Pygame**. The game features procedurally generated rooms, enemy AI, and both melee and ranged combat mechanics. The player fights through multiple rooms, defeating enemies while upgrading their health and attack power.

## Features
- **Procedural room generation** with randomized enemy placement.
- **AI-driven enemies** that chase and attack the player.
- **Melee and ranged combat** with animations.
- **Health and damage system** for the player and enemies.
- **Main menu, pause menu, and game over screen**.
- **Dynamic sprite animations** for player and enemies.
- **Background music and sound effects**.

## Installation
### Prerequisites
Ensure you have Python installed (version 3.7 or higher) along with Pygame.
```sh
pip install pygame
```

### Clone the Repository
```sh
git clone https://github.com/your-repo/soul-knight-game.git
cd soul-knight-game
```

### Run the Game
```sh
python main.py
```

## Controls
- **WASD** → Move the player.
- **Left Mouse Click** → Melee attack (charge for a stronger attack).
- **Right Mouse Click** → Shoot projectiles.
- **P** → Pause the game.
- **ESC** → Quit the game.
- **R (on game over screen)** → Restart the game.

## Project Structure
```
├── main.py         # Game entry point
├── game.py         # Main game loop and logic
├── player.py       # Player character mechanics
├── enemy.py        # AI-controlled enemies
├── room.py         # Procedural room generation
├── projectile.py   # Bullet/projectile system
├── animation.py    # Sprite animation handler
├── ui.py           # Health bars, text, menus
├── settings.py     # Game constants (screen size, FPS, scaling)
├── assets/         # Sprites, sounds, and background images
```

## Enemy AI Behavior
- **Chases the player** using vector-based movement.
- **Attacks when close** (with cooldowns to prevent spam).
- **Transitions between states** (walking, attacking, hurt, death).

## Future Improvements
🔹 Smarter AI (e.g., pathfinding, dodging)  
🔹 More enemy types & boss battles  
🔹 Power-ups and weapons  
🔹 Multiplayer mode  


