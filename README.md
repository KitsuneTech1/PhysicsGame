<p align="center"><a href="https://kitsunetechnologies.org/work"><img src="https://raw.githubusercontent.com/KitsuneTech1/.github/main/assets/kitsune-banner.svg" alt="Built by Kitsune Technologies" width="760"></a></p>

# Physics Demolition Puzzler

A pygame and pymunk physics puzzler where you place bombs to blow up buildings and knock every block below the collapse line.

## What it is

Physics Demolition Puzzler is a 2D demolition game built on pygame for rendering and pymunk for the physics simulation. Each level is a structure built out of steel, wood, and glass blocks with different masses (steel is heaviest, glass is lightest). You get a limited number of bombs per level. Place them, detonate, and let real physics (gravity, impulses, friction) take the structure down.

## Requirements

- Python 3.x
- `pygame`
- `pymunk`

(both listed in `requirements.txt`)

## Install and run

### Recommended (virtual environment)

```bash
git clone <this-repo-url>
cd PhysicsGame
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 game.py
```

On Windows, activate the venv with:

```
.venv\Scripts\activate
```

### Quick (no virtual environment)

```bash
pip install -r requirements.txt
python3 game.py
```

### Windows note

Same steps as above. If `python3` isn't recognized on your system, use `python` instead:

```
pip install -r requirements.txt
python game.py
```

## How to play

**Goal:** Place your bombs, detonate them, and bring every block in the structure down below the blue collapse line to clear the level.

**Controls (mouse only):**
- **Main menu:** click **Start** to begin, or **Quit** to exit.
- **Placing bombs:** click anywhere on the level to drop a bomb at that spot (costs one of your available bombs, shown in the top-left counter).
- **Detonate:** click the **Detonate** button (top right) to trigger every bomb you've placed. Each block within the blast radius gets an outward physics impulse, with a penalty of 50 points per bomb used.
- **After a loss:** if you run out of bombs with none placed and the structure hasn't collapsed below the line, you lose. The level automatically restarts after a couple of seconds, or you can click the **Menu** button on the "YOU LOSE!" screen to return to the main menu.
- **After a win:** once every block's bottom edge is below the collapse line, you see "YOU WIN!" and the game automatically advances to the next level.

There is no keyboard input; everything is driven by mouse clicks.

**Levels:** 2 levels are included.
- **Level 1** is a two-story wood and steel house on a steel foundation with 5 bombs available.
- **Level 2** is a 5-block glass, wood, and steel tower with 3 bombs available.

Clearing both levels ends the game.

## License

Licensed under the [PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0). Copyright (c) 2026 Kitsune Technologies LLC. Free for noncommercial use (personal, research, education, nonprofit, government); commercial use is not permitted under this license. See `LICENSE.md` for the full text.
