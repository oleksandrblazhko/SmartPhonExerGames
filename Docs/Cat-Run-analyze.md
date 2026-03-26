# Cat-Run Scratch Program Analysis

## Overview
**Cat-Run** is a Scratch v3 program (sb3 file) - an endless runner game where a cat character runs and jumps over obstacles. The program was decompiled from `4-Cat-Run-SmartPhone.sb3`.

## Directory Structure
```
Docs/Cat-Run/
├── project.json          # Main program logic (Scratch blocks as JSON)
├── *.svg                 # 87 vector graphics (costumes, backgrounds)
├── *.png                 # 3 bitmap images
└── *.wav                 # 3 audio files (sound effects)
```

## Program Structure (Targets)

The program contains **13 targets** (1 Stage + 12 Sprites):

| # | Sprite Name | Type | Description |
|---|-------------|------|-------------|
| 0 | **Stage** | Stage | Main stage with global variables and broadcasts |
| 1 | Blank | Sprite | Empty placeholder sprite |
| 2 | Player | Sprite | Main player character with multiple costumes |
| 3 | Obstacles | Sprite | Obstacle/spike generator using clones |
| 4 | Background | Sprite | Scrolling background |
| 5 | Text | Sprite | UI text display (score, HP) |
| 6 | This will Never Stop | Sprite | Continuous sound loop |
| 7 | Title | Sprite | Title screen with animations |
| 8 | Thumbnail | Sprite | Thumbnail image (Scratch Cat) |
| 9 | Detector | Sprite | Collision/interaction detector |
| 10 | Love / Fave | Sprite | Love/Favorite feedback system |
| 11 | Text 2 | Sprite | Secondary text display |
| 12 | Messages | Sprite | Message display system |

---

## Stage Configuration

### Variables (15 total)
| Variable | Default | Cloud? | Purpose |
|----------|---------|--------|---------|
| `*Speed` | 1 | No | Game speed control |
| `*Score` | 6 | No | Current score |
| `*Hurt` | 0 | No | Hurt state flag |
| `*Health` | 3 | No | Player health (lives) |
| `*Mouse` | 0 | No | Mouse input state |
| `Favorite` | 0 | No | Favorite counter |
| `Love` | 0 | No | Love counter |
| `Clones` | 1 | No | Clone counter |
| `*Character` | 0 | No | Current character index |
| `Character Set` | 1 | No | Character skin set |
| `*Can Change` | 0 | No | Character change permission |
| `*Highscore` | 0 | No | High score |
| `*Total Obstacles` | 6 | No | Obstacle counter |
| `-Use Buttons` | 1 | No | Button UI toggle |
| `☁ Record` | 42 | **Yes** | Cloud variable for online score |

### Lists (1 total)
| List | Contents | Purpose |
|------|----------|---------|
| `Characters` | ["1"] | Available character skins |

### Broadcast Messages (4 total)
| Message | Purpose |
|---------|---------|
| `Play Game` | Start game signal |
| `Game Over` | End game signal |
| `Animate` | Animation trigger |
| `Title` | Show title screen |

---

## Sprite Details

### Player Sprite
**Variables:**
- `Move` (default: 1) - Vertical movement state
- `-First` (default: "1") - Initialization flag

**Costumes (41 total):**
- Main cat run cycle: `run-01` through `run-16`
- Pico character: `Pico Walk 1-6`, `Pico Dead`
- Gobo character: `Gobo Walk 1-7`, `Gobo Dead`
- Nano character: `Nano Walk 1-7`, `Nano Dead`
- Death state: `Dead`

**Key Behaviors:**
- Keyboard controls: Up arrow / W (jump), Down arrow / S (duck)
- Mouse click support for mobile
- Character selection from list
- Multiple character skins (Cat, Pico, Gobo, Nano)

### Obstacles Sprite
**Variables:**
- `Lane` (default: 2) - Current lane position
- `Set` (default: "12") - Obstacle set number
- `Chance` (default: "8") - Spawn probability

**Costumes:** `Spikes`

**Key Behaviors:**
- Creates clones for multiple obstacles
- Random lane assignment
- Moves left (scrolling towards player)
- Collision detection with Player

### Background Sprite
**Variables:**
- `Move` (default: -1490) - Scroll position

**Key Behaviors:**
- Parallax scrolling effect
- Continuous leftward movement
- Wraps around for seamless loop

### Text Sprite
**Variables:**
- `Clone` (default: 7) - Text clone counter
- `Text` (default: "2") - Current text index

**Costumes:** Number digits (0-9), HP displays (HP 1, HP 2, HP 3, HP 4), blank

**Key Behaviors:**
- Dynamic score display
- Health point visualization
- Clone-based text rendering

### Title Sprite
**Costumes (7 total):** Title screen variations

**Key Behaviors:**
- Animated title screen
- Broadcasts "Play Game" on start
- Character preview display

### Detector Sprite
**Costumes:** `1`, `love`, `fave`

**Key Behaviors:**
- Touch/collision detection
- Love/Favorite feedback triggers

### Other Sprites
| Sprite | Purpose |
|--------|---------|
| **This will Never Stop** | Background music loop |
| **Thumbnail** | Project thumbnail (Scratch Cat) |
| **Love / Fave** | Social feedback animations |
| **Text 2** | Secondary text/messages |
| **Messages** | Pop-up message system |
| **Blank** | Placeholder (comment: "Please make changes if you're remixing") |

---

## Game Mechanics Summary

### Core Loop
1. **Title Screen** → Broadcast "Play Game"
2. **Player** runs in place (animation loop)
3. **Obstacles** spawn and move left
4. **Player** jumps/ducks to avoid obstacles
5. **Score** increases over time
6. **Health** decreases on collision
7. **Game Over** when health reaches 0

### Controls
- **Keyboard:** Up Arrow / W (jump), Down Arrow / S (duck)
- **Mouse:** Click/touch for mobile support

### Features
- Multiple character skins (unlockable)
- Cloud variable for online high scores
- Love/Favorite social features
- Animated title screen
- Parallax scrolling background
- Dynamic health/score display

---

## Technical Notes

### Block Categories Used
- **Motion:** Position, movement
- **Looks:** Costumes, effects, visibility
- **Sound:** Audio playback
- **Events:** Flag, broadcast, key presses
- **Control:** Loops, conditionals, clones, procedures
- **Sensing:** Touching, mouse, timer
- **Operators:** Math, logic, text
- **Variables:** Global and local variables
- **Lists:** Character storage

### Clone Usage
Heavy use of clones for:
- Obstacle generation
- Text rendering
- Visual effects

### Custom Procedures (Definitions found in blocks)
- `Reset` - Initialize game state
- `Walk` - Player walking animation

---

## File Inventory

### SVG Files (87 vector graphics)
Character costumes, obstacles, backgrounds, UI elements

### PNG Files (3 bitmap images)
- `0a05043fc2175c1f529339bb831b7ce7.png`
- `39bdb05096e87f9be9397c299efb658b.png`
- `cd11f6a83c1430611f99dc8d0ce4c851.png`
- `e2255cfea3b09eebf6b2c9b114ba6afc.png`

### WAV Files (3 audio)
- `1f81d88fb419084f4d82ffb859b94ed6.wav`
- `295e6859e83f726c0cafac5c3af58a86.wav`
- `32514c51e03db680e9c63857b840ae78.wav`
- `56144b03bb989a1bf33a3c54c83ef4a3.wav`
- `83a9787d4cb6f3b7632b4ddfebf74367.wav` (pop sound)
- `cac3341417949acc66781308a254529c.wav`

---

*Analysis generated from project.json structure*
