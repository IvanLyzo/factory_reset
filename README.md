# Factory Reset

Factory Reset is a top-down stealth-action game developed in Python using Pygame as part of a final project for a computer science course. All code and assets were created from scratch, with a focus on modularity, clean architecture, and extensibility. The game takes inspiration from classic arcade aesthetics, featuring pixel art, stark UI, and gameplay that emphasizes precision, awareness, and systems-based thinking. The entire project was created during a single week.

As always, this entire project (along with my entire life) is dedicated to  the love of my life **Hannah** (love you!!!)

## Game Premise

You play as a small worker bot navigating a decaying factory in a dystopian, productivity-obsessed world. The factory is structured into floors, and each floor consists of interconnected rooms. Your task is to ascend the levels while avoiding detection, disabling traps, and restoring or sabotaging systems.

Thematically, the game explores burnout, monotony, and systemic dysfunction, using the factory as a metaphor for productivity-at-all-costs culture.

## Core Features

### Modular Room and Level System

Rooms are defined as individual sections of a level ("floor").

The player can transition between rooms using a trigger system, which functions similarly to Unity's OnTriggerEnter. These transitions are modular and defined via callbacks.

Doors and room connections are built from JSON-like map data and dynamically loaded during gameplay.

### Trigger System

Triggers are rectangles in the game world that call a function (callback) when the player enters them.

Used for doorways, level transitions, or later, puzzle activators.

Internally tracked as their own class, allowing for arbitrary trigger zones that run modular behavior.

### Stealth Mechanic

The game starts in stealth mode, where turrets are offline and only simple patrol enemies are active.

If the player is spotted, the GameplayScene flips a stealth flag, activating more dangerous enemies and systems.

This system is centralized, with enemies checking against the global stealth flag rather than tracking player state.

### Health and Death System

The player has a current health and a health cap.

Getting hit reduces health; losing all health reduces the cap and resets current health.

When the cap hits zero, the game ends.

Integrates with UI to display current health.

### Game States

The game supports multiple global states: gameplay, paused, death, and minigame.

These states are handled in the main loop and determine what updates and what draws.

### UI Framework

A custom window-based UI system is used for menus, pause screens, and other interactions.

UIElement is a lightweight class for on-screen text with optional callbacks.

Visual selector (arrows) highlights the current option.

Entire UI interaction works via keyboard, matching the old-school arcade aesthetic.

### Snake-Inspired Minigame

Disabling advanced turret systems requires playing a minigame.

Based on Snake, but with a twist: the player must reach a target tile within a fixed-length snake.

Plays on a 15x15 tile grid.

Fully freezes the main game and switches to minigame state.

### Enemies

Turret: Stationary, rotates and shoots projectiles when stealth is broken.

Laser: Fires a constant beam across the room once stealth is broken; can only be disabled via minigame.

Drone: Non-solid flying unit that serves as surveillance. Doesn’t block movement.

Each enemy is its own class, but shares from a common Enemy base class for animation, disabling, and general interface.

### GameObject Hierarchy

All interactive objects inherit from a GameObject base class.

Provides pos, rect for collision, animation fields, and a draw method.

Used by players, enemies, turrets, and environmental objects (like laser catchers).

## Art and Visuals

Entirely pixel art, created manually.

Uses a limited industrial-themed color palette.

Floor and wall tiles have variants for visual diversity.

UI is white-on-black, pixelated, and minimal.

Sprites are animated using frame dictionaries with variable frame speeds.

## Code Quality and Type Safety

All core code is written using Python's type hints for better documentation and readability.

Uses enums (Direction) for orientation logic (both vector and angle).

Avoids deep inheritance trees where not useful (e.g., avoids unnecessary UI base classes).

Collisions, drawing, updating, and solid-state are all centralized in GameObject to reduce redundancy.

## Running the Game

Requirements

```
Python 3.10+

pygame 2.0+
```

Installation

```
pip install pygame
```

Run

```
python main.py
```

## Planned Features

Many additional features were planned but cut due to time constraints during the week-long development. Here are just some of the extensions considered:

- Final boss or narrative ending sequence

- Additional enemy variants

- Camera enemy that alerts other bots

- Dynamic tile variation (broken vs. repaired)

- Sound effects and ambient factory background track

## Developer Notes

This project was built not only as a game but as an exercise in managing complexity through modular systems. It showcases how Python and Pygame can be stretched far beyond simple arcade clones, supporting modern design practices like:

- Callback-driven systems

- State management

- Scene/window-based separation

- Minimal UI logic reuse

Feedback and suggestions are welcome. All code and assets are original. Feel free to use the code however you wish, but credit is always appreciated!
