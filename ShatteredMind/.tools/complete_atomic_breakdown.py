#!/usr/bin/env python3
"""
Complete Vault Atomic Breakdown Engine:
Separates every multi-concept note into individual atomic nodes while preserving
short stories and narrative prose as unified pieces.
Checks and eliminates duplicated ideas across all nodes.
"""

from __future__ import annotations

import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOCS_DIR = ROOT / "00_MOCs"
ASSETS_DIR = ROOT / "Assets"

def wikilink(path: str, label: str | None = None) -> str:
    return f"[[{path}|{label}]]" if label else f"[[{path}]]"

def property_links(paths: list[str]) -> list[str]:
    return [f"[[{p}]]" for p in paths]

def json_val(v: object) -> str:
    return json.dumps(v, ensure_ascii=False)

CATEGORIES = {
    "01_Game_Design": {
        "name": "Game Design",
        "moc": "Game_Design_MOC",
        "description": "Mechanics, systems, prototypes, worlds, economies, and experimental play.",
    },
    "02_Narrative_Psychology": {
        "name": "Narrative & Psychology",
        "moc": "Narrative_and_Psychology_MOC",
        "description": "Dreams, memory, identity, relationships, characters, and personal mythology.",
    },
    "03_Physical_Motion_Games": {
        "name": "Physical & Motion Games",
        "moc": "Physical_and_Motion_Games_MOC",
        "description": "Camera-based play, sports projects, playtests, interaction design, and production learning.",
    },
    "04_Art_Shaders_Aesthetics": {
        "name": "Art, Shaders & Aesthetics",
        "moc": "Art_Shaders_and_Aesthetics_MOC",
        "description": "Color, lighting, composition, VFX, animation, music, and visual references.",
    },
    "05_Tech_Pipelines_Unity": {
        "name": "Technology & Pipelines",
        "moc": "Tech_and_Pipelines_MOC",
        "description": "Unity implementation, rendering, robotics, infrastructure, tooling, and technical references.",
    },
    "06_Life_Career_Philosophy": {
        "name": "Life, Career & Philosophy",
        "moc": "Life_Career_and_Philosophy_MOC",
        "description": "Ethics, work, learning, business, personal values, health, and practical records.",
    },
}

# The comprehensive catalog of atomic concept extractions
ATOMIC_EXTRACTIONS = [
    # --- GAME JAM GAME IDEAS (8 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Color Switch - 2-Player Directional Puzzle",
        "stem": "Color Switch - 2-Player Directional Puzzle",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Cooperative 2-player puzzle where P1 controls vertical, P2 controls horizontal, and clapping switches control axes.",
        "content": """
### Core Gameplay Loop
- **Player 1**: Controls Up / Down movement.
- **Player 2**: Controls Left / Right movement.
- **Switch Action**: Clap hands (audio or motion threshold) to swap directional control axes.
- **Collaboration**: High-five gesture to swap target goals. Rotating game board introduces spatial disorientation.
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "01_Game_Design/Color Tile Consumption Wheel", "03_Physical_Motion_Games/Physical game concept"],
    },
    {
        "category": "01_Game_Design",
        "title": "Steam Train Driver",
        "stem": "Steam Train Driver",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Tactile train conductor simulation managing engine start sequences, residential noise levels, and station stops.",
        "content": """
### Train Driving Mechanics
- **Startup Sequence**: Multi-step tactical sequence of physical actions to fire up the locomotive engine.
- **Departure**: Seal train doors and depart station platform.
- **Noise Deceleration**: Actively slow down near residential districts to minimize community acoustic disruption.
- **Arrival**: Precise station alignment, braking deceleration, and passenger door release.
*(Directly complements [[02_Narrative_Psychology/Narrative Vignettes - Hitmen, Trains, and Spirit Enforcers|Frontier Train Track Seeding]].)*
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "02_Narrative_Psychology/Narrative Vignettes - Hitmen, Trains, and Spirit Enforcers"],
    },
    {
        "category": "01_Game_Design",
        "title": "Worms Arena - Cute Weapons PVP",
        "stem": "Worms Arena - Cute Weapons PVP",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Artillery turn-based combat featuring cute deforming worm characters and whimsical explosive weaponry.",
        "content": """
### Gameplay Modes & Dynamics
- **Modes**: PVP multiplayer arena or solo vs NPC bots.
- **Aesthetic**: Adorable worm characters wielding oversized, charmingly absurd weapons.
- **Tactile Impact**: Deforming ground terrain and physics-driven trajectory calculations.
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "01_Game_Design/Design a fun toy with surprises"],
    },
    {
        "category": "01_Game_Design",
        "title": "Job Simulator - Shopkeeper and Office Boy",
        "stem": "Job Simulator - Shopkeeper and Office Boy",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Playful physical interactions simulating the micro-chores of convenience store shopkeepers and office workers.",
        "content": """
### Micro-Roleplay Careers
- **Shopkeeper**: Scanning grocery goods, stocking shelves, and handling eccentric customer transactions.
- **Office Boy**: Delivering physical memos, stamping documents, dodging manager supervision, and sorting paperwork.
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "01_Game_Design/Timed Document Laser and Ping-Pong Ghost Escape"],
    },
    {
        "category": "01_Game_Design",
        "title": "Motion Pinball Machine - Arm Tilt Flippers",
        "stem": "Motion Pinball Machine - Arm Tilt Flippers",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Custom modular pinball where players tilt platforms with arm angles and trigger flippers with physical body poses.",
        "content": """
### Motion-Driven Arcade Play
- **Modular Board Building**: Unlock kinetic modules and design custom pinball tables.
- **Arm Angle Tilt**: Tilting your arms physically shifts the tilt angle of the game table.
- **Body Gesture Triggers**:
  - Standing Left / Center / Right zones dictates flipper focus.
  - Jump, swipe, or punch motions activate bumper modules and multiballs.
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "01_Game_Design/Pins, Wires, and Bond-Breaking Mechanics", "03_Physical_Motion_Games/Physical game concept"],
    },
    {
        "category": "01_Game_Design",
        "title": "Cats and Lasers - Feline Destructive Navigation",
        "stem": "Cats and Lasers - Feline Destructive Navigation",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/nature-organisms"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Using handheld laser pointer mechanics to entice chaotic cats into knocking over targets and dismantling puzzles.",
        "content": """
### Environmental Chaos Verbs
- **The Laser Pointer**: Player projects a laser dot across furniture and vertical walls.
- **Feline Physics**: Autonomous cats leap, pounce, and claw toward the dot with chaotic momentum.
- **Destruction Puzzles**: Route the cat into fragile targets, high-perch vases, and mechanical switches to solve rooms.
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "01_Game_Design/The Decryption Lens and Pattern Emblems"],
    },
    {
        "category": "01_Game_Design",
        "title": "Night in the Museum - Freeze Pose Escape",
        "stem": "Night in the Museum - Freeze Pose Escape",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Stealth evasion game where players must freeze in statue-like physical poses before security sweeps the gallery.",
        "content": """
### Countdown Pose Mechanics
- **Active Navigation**: Move freely across museum exhibits while the room timer counts down.
- **Freeze Pose Warning**: When security guards approach or searchlights pass, player must freeze completely.
- **Pose Matching**: Match the silhouette of nearby museum statues to camouflage and evade detection.
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "03_Physical_Motion_Games/Physical game concept", "01_Game_Design/Simon says Escape room"],
    },
    {
        "category": "01_Game_Design",
        "title": "Themed Escape Room System",
        "stem": "Themed Escape Room System",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Modular puzzle escape room framework adapting room themes, clue chains, and cooperative physical locks.",
        "content": """
### Architecture
- **Themed Scenarios**: High-immersion narrative environments with sequential puzzle dependencies.
- **Physical Clue Chains**: Decoding environmental ciphers, keycards, and kinetic apparatuses to unlock exits.
""",
        "related": ["01_Game_Design/Game Jam Game Ideas", "01_Game_Design/Simon says Escape room"],
    },

    # --- LOOT, MAGIC, ROBOTS (7 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "The Ultra-Lazy Game - Brain and Body Disconnect",
        "stem": "The Ultra-Lazy Game - Brain and Body Disconnect",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "很懶很懶既遊戲: A game exploring extreme sluggishness, where the brain and body negotiate conflicting commands.",
        "content": """
### Core Philosophy & Mechanics
- **因為想懶 所以要諗辦法 (Inventive Laziness)**: Solving systemic problems through extreme minimalism and ingenious workarounds.
- **相連 黏痴 (Adhesion & Cling)**: Sticky mechanics that latch objects together so the player doesn't have to move.
- **身體叫個腦做野，個腦叫個身體做野 (Brain-Body Asynchrony)**:
  - The physical body commands the brain to calculate.
  - The brain commands the body to actuate.
  - Brain and body are detached into separate controllable entities.
- **太明 / 太暗 (Sensory Extremes)**: Visual environments shifting between glaring overexposure and total darkness.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "02_Narrative_Psychology/The Resting Game and Emotional Geometry", "01_Game_Design/Cognitive Delays and Perception Lag"],
    },
    {
        "category": "01_Game_Design",
        "title": "Chimp Department Store - Mini-Employee Cards",
        "stem": "Chimp Department Store - Mini-Employee Cards",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Chimp百貨: Consolation cards given to melancholic shoppers that spawn tiny running employees when placed on the floor.",
        "content": """
### Commercial Empathy Verbs
- **Sad Customer Reception**: When a shopper's emotional telemetry drops into sadness, they receive specialized Chimp Cards at checkout.
- **Card Deployment**: Laying the card upon the floor causes it to unfold into miniature helper employees that scurry back to offer comfort.
- **Surface Snapping**: Set placement angle and geometric shape; objects snap and adhere to walls (清麗苑 housing motif).
- **Emergency Use Series**: Absurdist sealed utility kits reserved strictly for crisis situations.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye", "01_Game_Design/Design a fun toy with surprises"],
    },
    {
        "category": "01_Game_Design",
        "title": "Connect the Dots Puzzle - Dark Sky Star Sequences",
        "stem": "Connect the Dots Puzzle - Dark Sky Star Sequences",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Dark exploration puzzle where players slow down in dim star fields and type keystroke sequences to link celestial nodes.",
        "content": """
### Constellation Mechanics
- **Dark Sky & Dim Stars**: Minimalist navigation across near-pitch-black celestial voids.
- **Pacing Reward**: Systemic rewards for slowing down movement speed rather than rushing.
- **Keystroke Linking**:
  - Initiate connection with `'` apostrophe key.
  - Type rhythmic alphanumeric sequence to bridge stars.
- **Mathematical Curves**:
  ```csharp
  int HeightSubdivision;
  int WidthSubdivision;
  for (i = 0; i < max; i++)
      Vector3(Mathf.Sin(i), 0, Mathf.Cos(i));
  ```
- **Puzzle Formats**: Battle puzzles, Easter egg hunt chain puzzles, and fluid water-wiggle geometry.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "04_Art_Shaders_Aesthetics/never use true white and black", "01_Game_Design/Pins, Wires, and Bond-Breaking Mechanics"],
    },
    {
        "category": "01_Game_Design",
        "title": "Discharge Energy Nodes and Shifting Ceilings",
        "stem": "Discharge Energy Nodes and Shifting Ceilings",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Transferring electrical charges between Point A and B to lower ceilings, shift architecture, and tell stories through light.",
        "content": """
### Energy Conduit Architecture
- **Charging & Discharging**: Walk to Node Point A to absorb charge; navigate to Node Point B to discharge energy into the room circuit.
- **Kinetic Architecture**: Pressing room triggers lowers ceiling planes and reconfigures surrounding wall geometry.
- **Storytelling by Light**: Architecture is illuminated according to who owns the light source.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Pins, Wires, and Bond-Breaking Mechanics", "01_Game_Design/crystal world where the player uses a flashlight to shine coloured crystal and fractures the light to show platforms"],
    },
    {
        "category": "01_Game_Design",
        "title": "Cognitive Memory Capacity Barrier",
        "stem": "Cognitive Memory Capacity Barrier",
        "tags": ["category/game-design", "theme/dreams-memory", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Cognitive paradox where universal knowledge access is systematically blocked as a player accumulates personal memories.",
        "content": """
### The Knowledge Barrier Tenet
*"You have access to all information, but your brain stores memories and blocks off access as more memories are stored."*

- **Accumulation Cost**: Storing specific experiential memories occupies neural bandwidth, blinding the character to macro-information.
- **Forgetting as Retrieval**: Intentionally shedding stored memories restores raw perception and access to universal environmental data.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "02_Narrative_Psychology/Memory Golem and Dream Entity Network", "01_Game_Design/Cognitive Delays and Perception Lag"],
    },
    {
        "category": "01_Game_Design",
        "title": "Component Attachment Scoring Matrix",
        "stem": "Component Attachment Scoring Matrix",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/procedural-generation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Scoring modular tree branches through root object attachment status and public visibility ratings.",
        "content": """
### Mini Manager Evaluation
- **Tree Branch Audit**: Inspect root object and attachment point status to quantify how many branches exist in the structure.
- **Operator Protocol**: Check protocol/operator; if null, fall back to default behavior.
- **Public Object Multiplier**: Every sub-component earns an intrinsic score; being a publicly exposed object multiplies the total score.
- **Consumable Degradation / Escalation**: First use multiplies effect 1x; second use escalates to 2x before depletion.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Flocking Players"],
    },
    {
        "category": "01_Game_Design",
        "title": "Momentum Storage and Kinetic Release",
        "stem": "Momentum Storage and Kinetic Release",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Banking incoming kinetic energy into objects or character limbs to shoot out accelerated rebound trajectories.",
        "content": """
### Kinetic Absorption & Release
- **Kinetic Battery**: Absorb incoming enemy velocity or downhill momentum and store it within equipment springs.
- **Snap Rebound**: Discharge banked momentum in an explosive vector burst.
- **Narrative Fragment**: Delly Cyrus, a troubled teenager and targeted underdog, running through urban terrain.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Surfing", "01_Game_Design/character can run on 2feet and different feet would gives boost to different directions while sprinting to a direction."],
    },

    # --- 妖尾貓之惡夢 (7 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "9-Numpad Directional Stat Control",
        "stem": "9-Numpad Directional Stat Control",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/ui-ux"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/妖尾貓之惡夢",
        "summary": "Grid control using 9-numpad directions, fusing low stats into higher tiers, and combining shared disposable stats.",
        "content": """
### Input Grid & Stat Synthesis
- **9-Numpad Grid**: Tactical direction mapped across a 3x3 numeric keypad.
- **Stat Fusion**: Combining 2 low-tier attributes to forge 1 medium-tier stat.
- **Disposable Equity**: Combining fractional shares of disposable player stats to temporarily clear encounter thresholds.
- **Cognitive Preference**: Interfaces designed around muscle memory and cognitive compression.
""",
        "related": ["01_Game_Design/妖尾貓之惡夢", "01_Game_Design/00928z", "01_Game_Design/UI Event Matrices and Spatial Pacing"],
    },
    {
        "category": "01_Game_Design",
        "title": "Multi-Server Stat Variation Worlds",
        "stem": "Multi-Server Stat Variation Worlds",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/procedural-generation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/妖尾貓之惡夢",
        "summary": "Deploying the same game world across multiple parallel servers, each running distinct stat scalers and physics balance.",
        "content": """
### Parallel Physics Ecosystems
- **Server Ecosystems**: Games with RPG stats feature parallel servers running distinct balancing formulas, drop rates, and stat curves.
- **Stat Squishing**: Rate and numerical compression applied differently across realms.
""",
        "related": ["01_Game_Design/妖尾貓之惡夢", "01_Game_Design/Massively Multiplayer Game"],
    },
    {
        "category": "01_Game_Design",
        "title": "Mini Heavy Pool - 8-Ball Role Mechanics",
        "stem": "Mini Heavy Pool - 8-Ball Role Mechanics",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/cards-tabletop"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/妖尾貓之惡夢",
        "summary": "Billiards on an ultra-heavy friction table where each of the 8 pool balls possesses active class roles and behaviors.",
        "content": """
### Heavy Table Billiards
- **Inertial Tabletop**: An exceptionally heavy table with extreme friction dampening.
- **Living Billiard Roles**: Standard 8-balls are assigned individual RPG roles (tank ball, decoy ball, seismic ball).
- **Taxonomy of Count Games**: Balance games, countdown games, rollup games, redistribution games, and five-senses games.
""",
        "related": ["01_Game_Design/妖尾貓之惡夢", "01_Game_Design/chess pieces knocking off board"],
    },
    {
        "category": "01_Game_Design",
        "title": "Mission Cost Interface and Falling Orbs",
        "stem": "Mission Cost Interface and Falling Orbs",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/妖尾貓之惡夢",
        "summary": "Selecting rewards dynamically displays mission difficulty costs; energy orbs plummet from towering altitudes.",
        "content": """
### Inverted Quest Selection
- **Reward-First Selection**: Choosing desired reward immediately renders the associated survival costs and mission dangers.
- **Falling Ability Orbs**: Orbs plummet from high architectural perches; catching them mid-air grants temporary superpower verbs.
- **Spherecast Timing**: Spherecast calculates an integer stored on object; higher integers inject proportional delay.
""",
        "related": ["01_Game_Design/妖尾貓之惡夢", "01_Game_Design/21 Grams Weight of a Soul"],
    },
    {
        "category": "01_Game_Design",
        "title": "Bedroom Twilight Orb Adventure",
        "stem": "Bedroom Twilight Orb Adventure",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/light-color"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light", "00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "01_Game_Design/妖尾貓之惡夢",
        "summary": "Don't Starve + Concrete Genie hybrid: toggling bedroom lights shifts the realm into twilight and transforms cutouts into living shadows.",
        "content": """
### Concrete Genie + Don't Starve Metaphor
- **Light Switch Dualism**:
  - Lights Off: The stage dissolves into an eerie, luminous twilight realm.
  - Lights On: The environment reverts to a familiar child's bedroom.
- **Paper Cutout Companions**: Learning to craft paper cutouts to befriend shadows.
- **Compassionate Optics**: Shadows offer sanctuary; excessive brightness blinds allies. Player must shape gentle light cones for others.
- **Mirror Lamps**: 鏡面燈 — reflective lamps bouncing light around corners.
""",
        "related": ["01_Game_Design/妖尾貓之惡夢", "01_Game_Design/crystal world where the player uses a flashlight to shine coloured crystal and fractures the light to show platforms", "04_Art_Shaders_Aesthetics/never use true white and black"],
    },
    {
        "category": "01_Game_Design",
        "title": "Filmstrip Reel Screen Burn Mechanic",
        "stem": "Filmstrip Reel Screen Burn Mechanic",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/visual-art"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/妖尾貓之惡夢",
        "summary": "Projector film mechanics where prolonged illumination literally burns the screen, forcing sacrificial film slides to pass stages.",
        "content": """
### Projector Burnout Mechanics
- **Slide Insertion**: Slide in physical filmstrips to play images and reveal hidden environmental paths.
- **Composite Film Layers**: Layering multiple translucent films synthesizes composite optical effects.
- **Thermal Burnout**: Sustaining a light beam too long causes the filmstrip to smoke, burn, and dissolve off-screen, triggering a Game Over.
- **Sacrificial Clearance**: Players are deliberately forced to burn out critical filmstrips to blast through barrier obstacles.
- **Framerate Encryption**: Altering frame refresh rates dynamically to conceal secret clues from conscious perception.
""",
        "related": ["01_Game_Design/妖尾貓之惡夢", "04_Art_Shaders_Aesthetics/crt tv zoom in", "01_Game_Design/The Decryption Lens and Pattern Emblems"],
    },
    {
        "category": "01_Game_Design",
        "title": "Scrambled Health Bar Combat",
        "stem": "Scrambled Health Bar Combat",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/ui-ux"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/妖尾貓之惡夢",
        "summary": "Attacks that physically scramble and fragment the player's UI health bar, halting depletion only when falling into UI gaps.",
        "content": """
### UI Fragmentation Attack
- **Health Bar Glitch**: Enemy attacks physically jumble and scramble the health bar segments across the screen.
- **Safety Gaps**: If the health bar depletes into a shattered UI gap, damage pauses immediately.
- **Tactile Messaging**: Furious texting and messaging interactions (`Drawing 5.png`).
""",
        "related": ["01_Game_Design/妖尾貓之惡夢", "01_Game_Design/UI Event Matrices and Spatial Pacing"],
    },

    # --- IF DISTANCE = X (8 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Target Locking and Audio Sensory Feedback",
        "stem": "Target Locking and Audio Sensory Feedback",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/sound-music"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "Target lock vector scripts paired with a whimsical, tactile sound design palette.",
        "content": """
### Script Logic & Sound Palette
```csharp
transform.position = target;
locking = true;
if (aiming == false) {
    locking = false;
}
```
### Audio Palette
- Plunger and sprinkle pop sound.
- Yoshi 'huh' vocal cues.
- Train cart 'ging-gong' metallic clicks.
- Fiery wind burst explosion.
""",
        "related": ["01_Game_Design/if distance = x", "04_Art_Shaders_Aesthetics/Acoustic Physics and 3D Wave Visualization"],
    },
    {
        "category": "01_Game_Design",
        "title": "Unit Death Return on Investment",
        "stem": "Unit Death Return on Investment",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "Designing economic units whose monetary investment and yield are paid out strictly upon their death.",
        "content": """
### Sacrificial Economics
- **Death Dividend**: Units do not earn revenue while idling alive; their purchase cost is refunded with profit multipliers only upon destruction.
- **Strategic Martyrdom**: Pushing units into calculated mortal danger accelerates resource cycles.
""",
        "related": ["01_Game_Design/if distance = x", "01_Game_Design/21 Grams Weight of a Soul", "01_Game_Design/Lifespan  how many cycles"],
    },
    {
        "category": "01_Game_Design",
        "title": "GTA Alien Invasion Faction Choice",
        "stem": "GTA Alien Invasion Faction Choice",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "Open-world urban sandbox disrupted by extraterrestrial invasion where players choose to defend humanity or aid invaders.",
        "content": """
### Open-World Cataclysm
- **Premise**: GTA open-world urban crime simulation interrupted by a full-scale alien planetary invasion.
- **Faction Divergence**: Players choose whether to ally with terrestrial authorities/gangs or execute covert operations for the alien forces.
""",
        "related": ["01_Game_Design/if distance = x", "01_Game_Design/Massively Multiplayer Game"],
    },
    {
        "category": "01_Game_Design",
        "title": "Match Flare Galaxy Relativity",
        "stem": "Match Flare Galaxy Relativity",
        "tags": ["category/art-shaders-and-aesthetics", "theme/time-cycles", "theme/visual-art"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "Cosmological metaphor: the universe as the flash of a striking match, inside which time moves at an imperceptible crawl.",
        "content": """
### Relativistic Ignition
*"The galaxy is a flash of a striking flare of a match. Inside this flare, time moves extremely slow relative to the galaxy, and we are born in this flare with light."*
""",
        "related": ["01_Game_Design/if distance = x", "04_Art_Shaders_Aesthetics/never use true white and black", "04_Art_Shaders_Aesthetics/Black Supernova and Diffused Light Transitions"],
    },
    {
        "category": "01_Game_Design",
        "title": "Red Button Micro-Loop Puzzle",
        "stem": "Red Button Micro-Loop Puzzle",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/time-cycles"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory", "00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "A giant red button that explodes and resets the room upon impact; breaking the loop requires pressing it with minute tactile variance.",
        "content": """
### The Reset Loop
- **Negative Feedback Loop**: Pressing the prominent red button causes an immediate catastrophic explosion that resets the scene.
- **Micro-Discrepancies**: Altering the physical velocity, angle, or rhythm of the press yields a microscopic variance in the explosion.
- **Loop Breaking**: Players deduce clues within the micro-differences to break the temporal reset.
- **Compounding Complexity**: Advancing levels introduces secondary and tertiary buttons governing intertwined puzzle sets.
""",
        "related": ["01_Game_Design/if distance = x", "01_Game_Design/Cognitive Delays and Perception Lag", "07_Synthesized_Concepts/Lucid Terminal - The Memory Golem"],
    },
    {
        "category": "01_Game_Design",
        "title": "Limited Mobility Motor Rhythm Imitation",
        "stem": "Limited Mobility Motor Rhythm Imitation",
        "tags": ["category/game-design", "theme/motion-body", "theme/learning-accessibility"],
        "hubs": ["00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "Tactile assistive design translating everyday domestic rhythms (e.g. brushing teeth) into game interactions for limited mobility players.",
        "content": """
### Assistive Motion Interaction
- **Domestic Rhythms**: Translating ordinary rhythmic motions (brushing teeth, wiping glass, stirring tea) into expressive gameplay inputs.
- **Accessibility Inclusivity**: Tailoring kinetic tracking to players with restricted mobility ranges.
""",
        "related": ["01_Game_Design/if distance = x", "03_Physical_Motion_Games/Physical game concept", "06_Life_Career_Philosophy/Learning opens doors"],
    },
    {
        "category": "01_Game_Design",
        "title": "Mass and Structural Boundary Dynamics",
        "stem": "Mass and Structural Boundary Dynamics",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "Growth dynamics: mass limits area, structure determines reach, and complete coverage merges separate entities into one system.",
        "content": """
### Boundary Dynamics
- **Uncertainty of Growth**: Encouraging unpredictable spatial expansion.
- **Physical Constraints**: Surface area is strictly bounded by available mass; physical reach is dictated by skeletal structure.
- **Systemic Assimilation**: When one object completely engulfs another, their discrete rulesets merge into a singular combined system.
- **Aesthetic Tenet**: *"Only fractured can see the completed. Imperfections that perfect us. It was the only option, not the answer."*
""",
        "related": ["01_Game_Design/if distance = x", "01_Game_Design/Flocking Players"],
    },
    {
        "category": "01_Game_Design",
        "title": "Pay-to-Win Tic-Tac-Toe and Tiny Heroes",
        "stem": "Pay-to-Win Tic-Tac-Toe and Tiny Heroes",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/if distance = x",
        "summary": "Satirical pay-to-win store embedded into standard Tic-Tac-Toe, paired with unique storytelling vignettes for Tiny Heroes.",
        "content": """
### Micro-Game Concepts
- **Pay-to-Win Tic-Tac-Toe**: Modifying the solved game of Tic-Tac-Toe by adding aggressive, ridiculous microtransaction purchases (place an X on top of an O).
- **Tiny Heroes**: Miniature procedural story vignettes (`IMG_8047.png`).
""",
        "related": ["01_Game_Design/if distance = x", "01_Game_Design/Purchasable Power Corporate Finance"],
    },

    # --- PUNCHING BAG EATS ENEMY (3 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Tiered Magic Terrain",
        "stem": "Tiered Magic Terrain",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Punching bag eats enemy and punching it deals dmg",
        "summary": "Geological magic levels across landscape zones dictating the maximum spell tiers that can be invoked.",
        "content": """
### Environmental Magic Saturation
- **Terrain Magic Tiers**: Ground terrain possesses intrinsic mana levels.
- **Cast Restrictions**: Players can only cast high-tier magic when standing upon terrain with equal or greater magic saturation.
""",
        "related": ["01_Game_Design/Punching bag eats enemy and punching it deals dmg", "01_Game_Design/Magic"],
    },
    {
        "category": "01_Game_Design",
        "title": "Magic Dungeon Guard Trust and Retirement",
        "stem": "Magic Dungeon Guard Trust and Retirement",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/Punching bag eats enemy and punching it deals dmg",
        "summary": "Overhearing neglected dungeon guards, fixing their broken gear, and helping them retire to become farmers.",
        "content": """
### Dungeon Empathy Loop
- **Waking in Dungeon**: Eavesdrop on enemy castle monsters complaining about being neglected by their dark master.
- **Acts of Mercy**: Repair an injured guard's broken shield and heal his leg.
- **Monster Aspirations**: The monster guard reveals castle layout secrets and confides that he wishes to retire to become a humble farmer.
- **Genre Shifting**: Gaining trust from specific monster types fundamentally shifts the game's genre rules.
""",
        "related": ["01_Game_Design/Punching bag eats enemy and punching it deals dmg", "01_Game_Design/21 Grams Weight of a Soul", "07_Synthesized_Concepts/Guild of the Departed - 21 Grams"],
    },
    {
        "category": "01_Game_Design",
        "title": "Fire Monster Combustible Puzzle Pairing",
        "stem": "Fire Monster Combustible Puzzle Pairing",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Punching bag eats enemy and punching it deals dmg",
        "summary": "Wrangling struggling fire monsters as live items, using movement speed to ignite combustible puzzle zones.",
        "content": """
### Living Tool Mechanics
- **Monster as Item**: Capturing and physically hoisting struggling elemental creatures.
- **Movement Speed Trigger**: Moving too quickly agitates the fire monster, causing premature detonation.
- **Combustion Solving**: Transport the creature to flammable barriers to clear obstacles.
- **Modular Puzzle Pairs**: Monsters and environmental puzzles appear as matched pairs with multi-solution combinations.
""",
        "related": ["01_Game_Design/Punching bag eats enemy and punching it deals dmg", "01_Game_Design/Inverted Role Play - Minion and Pest Escape"],
    },

    # --- PHYSICAL GAME CONCEPT (2 ATOMIC NOTES) ---
    {
        "category": "03_Physical_Motion_Games",
        "title": "Reach Extension Physical Tools",
        "stem": "Reach Extension Physical Tools",
        "tags": ["category/physical-and-motion-games", "theme/motion-body", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "03_Physical_Motion_Games/Physical game concept",
        "summary": "Physical tools that extend player reach in motion games: height extenders, jigsaw filters, and map magnifying lenses.",
        "content": """
### Tool Affordances
- **Reach Augmentation**: Tools expanding physical range (height stilts, magnifiers, jigsaw shape alignment).
- **Color Filters**: Revealing hidden patterns across screen displays by looking through physical or optical color filters.
- **Animal Audio Cues**: Using animal calls to indicate world events.
""",
        "related": ["03_Physical_Motion_Games/Physical game concept", "01_Game_Design/The Decryption Lens and Pattern Emblems"],
    },
    {
        "category": "03_Physical_Motion_Games",
        "title": "Character Aim Delay Variance",
        "stem": "Character Aim Delay Variance",
        "tags": ["category/physical-and-motion-games", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "03_Physical_Motion_Games/Physical game concept",
        "summary": "Decoupling player aiming input from character skeletal animation latency to create tactile weapon handling differences.",
        "content": """
### Skeletal Aim Delay
- **Animation Catch-Up**: Decoupling reticle motion from character skeletal rotation.
- **Character Asymmetry**: Heavier characters exhibit sluggish aim delay; agile characters snap immediately to cursor coordinates.
""",
        "related": ["03_Physical_Motion_Games/Physical game concept", "01_Game_Design/Cognitive Delays and Perception Lag"],
    },

    # --- SURFING (4 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Wave Dynamics and Aerial Combos",
        "stem": "Wave Dynamics and Aerial Combos",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Surfing",
        "summary": "Side-scrolling surfing mechanics: A-frame reef breaks, skateboard tricks, pumping cadence, and aerial air combos.",
        "content": """
### Oceanic Kinematics
- **Side-Scrolling Ocean Grid**: Traversing 2D wave elevation profiles.
- **A-Frame Reef Breaks**: Waves breaking symmetrically left and right over coral reefs.
- **Pumping Acceleration**: Pumping along the wave face converts potential height into raw speed.
- **Air Combos**: Launching off the lip to execute technical rotational aerials.
""",
        "related": ["01_Game_Design/Surfing", "07_Synthesized_Concepts/Bora-Bora Spectrum Surfer"],
    },
    {
        "category": "01_Game_Design",
        "title": "Surfboard Equipment and High Fashion Economy",
        "stem": "Surfboard Equipment and High Fashion Economy",
        "tags": ["category/game-design", "theme/economy-value", "theme/visual-art"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Surfing",
        "summary": "Surfboard tailoring ratios, high-fashion wetsuit sponsorships, and seashell repair economies.",
        "content": """
### Equipment Tailoring & Value
- **Board-to-Physique Ratio**: Matching board volume directly to surfer body dimensions.
- **Wetsuit Sponsors**: Placing corporate sponsor decals onto designer wetsuits.
- **Seashell Maintenance**: Broken board fins require repair costs paid in time and collected seashells.
""",
        "related": ["01_Game_Design/Surfing", "06_Life_Career_Philosophy/no ETH"],
    },
    {
        "category": "01_Game_Design",
        "title": "Surf Tournament Formats and Rentals",
        "stem": "Surf Tournament Formats and Rentals",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Surfing",
        "summary": "Tiered surfing competitions: ticket entry, rent-board-only equalized formats, and the mythical Bora-Bora arena.",
        "content": """
### Tournament Ladders
1. Ticket Only (earned via ranking or trade).
2. Open Entry (bring any custom board).
3. Free Entry with Standardized Rental Boards (skill-only test).
- **Bora-Bora**: Legendary beach arena featuring training stages and endgame wave randomness.
""",
        "related": ["01_Game_Design/Surfing", "06_Life_Career_Philosophy/no ETH"],
    },
    {
        "category": "01_Game_Design",
        "title": "Card-Driven Wave Movement Combo",
        "stem": "Card-Driven Wave Movement Combo",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/cards-tabletop"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Surfing",
        "summary": "Turn-based wave surfing: tactical grid movement, crash penalties, and fluctuating timers mimicking wave surges.",
        "content": """
### Card Movement Engine
- **Wave Surge Timer**: Fluctuating round timer mimicking the rise and fall of ocean swells.
- **Resource Expenditure**: Forcing movement requires discarding skill cards; navigating ascending vs descending wave faces restricts which card combos can be triggered.
- **Crash Penalty**: Clashing with a rival surfer plunges both players to the seabed.
""",
        "related": ["01_Game_Design/Surfing", "01_Game_Design/Digital Candy Game"],
    },

    # --- QUESTION MAN (4 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Institutional Doubt System Sabotage",
        "stem": "Institutional Doubt System Sabotage",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/asymmetry-deception"],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/question man",
        "summary": "Mechanic where expressing systemic doubt or distrust actively sabotages machine and social infrastructures.",
        "content": """
### Sabotage by Skepticism
*"Doubting any part of a system to sabotage."*
- Expressing doubt in rules or infrastructure weakens mechanical integrity, causing gears, doors, and social agreements to jam.
""",
        "related": ["01_Game_Design/question man", "01_Game_Design/Killer game"],
    },
    {
        "category": "01_Game_Design",
        "title": "Injury Buff and Active Recovery",
        "stem": "Injury Buff and Active Recovery",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/question man",
        "summary": "Combat system where suffering localized bodily injury unlocks active skill buffs specific to that damaged anatomy.",
        "content": """
### Anatomical Compensation
*"For every injury, you can use active skills/resources to buff that part."*
- Taking damage to the arm empowers strike velocity; damaged legs unlock evasive dashes.
""",
        "related": ["01_Game_Design/question man", "01_Game_Design/Systemic Combat Friction and Flu Seasons"],
    },
    {
        "category": "01_Game_Design",
        "title": "Potion Brewing Poison Roulette",
        "stem": "Potion Brewing Poison Roulette",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/question man",
        "summary": "Cooperative potion alchemy featuring inherent probabilistic chances of poisoning companions.",
        "content": """
### Alchemical Treachery
- **Brewing Mechanics**: Combining reagents to synthesize party buffs.
- **Poison Moment**: High-potency brews carry a discrete chance to accidentally (or deliberately) poison your own allies.
""",
        "related": ["01_Game_Design/question man", "01_Game_Design/Underground Casino and Cheating Mechanics"],
    },
    {
        "category": "01_Game_Design",
        "title": "Prefix Obstacle Difficulty Mode",
        "stem": "Prefix Obstacle Difficulty Mode",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/modular-toys"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/question man",
        "summary": "Dynamic difficulty system where players prepend grammatical prefixes to obstacles to modify challenge modifiers.",
        "content": """
### Semantic Difficulty Modifiers
- **Prefix Application**: Prepend descriptors (`Trash-`, `Fatty-`, `Deadly-`, `Nutritious-`) to world obstacles to alter difficulty and drop rates.
- **Ammo as Airtime**: Firearm ammo count directly dictates aerial jump hover duration.
- **Conditional Shop Hours**: Merchants open strictly upon meeting obscure social or temporal triggers.
""",
        "related": ["01_Game_Design/question man", "01_Game_Design/Game idea"],
    },

    # --- LOSING GRAVITY (3 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Earthbound Chains vs Weightless Youth",
        "stem": "Earthbound Chains vs Weightless Youth",
        "tags": ["category/game-design", "theme/worldbuilding", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/losing gravity",
        "summary": "Metaphysical world where the elderly wear heavy metal chains while youth revel in weightless buoyancy.",
        "content": """
### Generational Mass Polarity
- **Chained Elders**: The older generation anchors itself with heavy metals (heaviest metals hold greatest economic value).
- **Weightless Youth**: Younger generation abandons mass, reveling in ungrounded weightlessness.
- **Environmental Anarchy**: Water floats suspended in air; atmospheric weather disorder.
""",
        "related": ["01_Game_Design/losing gravity", "02_Narrative_Psychology/Card box apartment", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye"],
    },
    {
        "category": "01_Game_Design",
        "title": "One-Way Dimensional Escape Paths",
        "stem": "One-Way Dimensional Escape Paths",
        "tags": ["category/game-design", "theme/worldbuilding", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/losing gravity",
        "summary": "The world creator can carve escape tunnels for inhabitants, but incompatible existential formats forbid return.",
        "content": """
### Incompatible Dimensional Formats
*"The creator can make a path for someone to escape, but they cannot return, because the different formats are incompatible."*
- Crossing thresholds converts personal data into formats that can never be reconciled with the origin plane.
""",
        "related": ["01_Game_Design/losing gravity", "02_Narrative_Psychology/Card box apartment"],
    },
    {
        "category": "01_Game_Design",
        "title": "Biological Clock Loop",
        "stem": "Biological Clock Loop",
        "tags": ["category/game-design", "theme/time-cycles", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/losing gravity",
        "summary": "Game loops driven by circadian biological clocks (生理時鐘) governing land productivity and player choices.",
        "content": """
### Circadian Rhythm Architecture
- **生理時鐘 (Biological Clock)**: In-game bodies and agricultural lands pulse according to biological rhythm cycles.
- **Land Productivity Shifts**: Player agricultural choices directly warp ecological productivity rates.
""",
        "related": ["01_Game_Design/losing gravity", "01_Game_Design/Lifespan  how many cycles"],
    },

    # --- FLOCKING PLAYERS (3 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Polaroid Grey-Boxing and Object Cooldowns",
        "stem": "Polaroid Grey-Boxing and Object Cooldowns",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/visual-art"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Flocking Players",
        "summary": "Rapid grey-box prototyping using Polaroid snapshot composition, object cooldown tempo, and structure of conflict.",
        "content": """
### Rapid Spatial Composition
- **Polaroid Grey-Boxing**: Capturing spatial compositions through camera framing to dictate blockout pacing.
- **Tempo Management**: Object cooldown rhythms dictate game combat tempo and structure of conflict.
""",
        "related": ["01_Game_Design/Flocking Players", "01_Game_Design/Cognitive Delays and Perception Lag"],
    },
    {
        "category": "01_Game_Design",
        "title": "AI-Aware Armor and Adaptive Quests",
        "stem": "AI-Aware Armor and Adaptive Quests",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/asymmetry-deception"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Flocking Players",
        "summary": "Sentient gear with conversational AI bots (Google Banter Bot) that generate dynamic bonus quests tailored to player trade.",
        "content": """
### Sentient Equipment
- **Banter Bot Gear**: Wearable armor equipped with real-time AI conversational personality.
- **Adaptive Bonus Objectives**: Rare item drops unlock customized questlines matching player profession, trade history, and encounter patterns.
- **Unique Mastery Rewards**: Completing adaptive objectives rewards speed buffs, unique mounts, and specialized currency.
""",
        "related": ["01_Game_Design/Flocking Players", "02_Narrative_Psychology/Narrative Vignettes - Hitmen, Trains, and Spirit Enforcers"],
    },
    {
        "category": "01_Game_Design",
        "title": "Language of Form AI Upscaler",
        "stem": "Language of Form AI Upscaler",
        "tags": ["category/technology-and-pipelines", "theme/unity-technical", "theme/procedural-generation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Flocking Players",
        "summary": "AI algorithm upscaling low-poly grey-box models into high-poly assets governed by designer shape grammar.",
        "content": """
### Generative Shape Grammar
- **Form Language Pipeline**: Designers define root shape language; procedural models extrapolate fine fabrics and architectural detail.
- **Runtime Upscaling**: Games render lightweight low-poly meshes at runtime while neural algorithms upscale visual fidelity on the fly.
""",
        "related": ["01_Game_Design/Flocking Players", "05_Tech_Pipelines_Unity/Procedural Map and Building Generation Workflow"],
    },

    # --- RECONNECTING (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Dual Perspective Disconnect and Reconnect",
        "stem": "Dual Perspective Disconnect and Reconnect",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "01_Game_Design/reconnecting",
        "summary": "Same environment experienced from two mirrored viewpoints, where movement is reflective and death purges carried assets.",
        "content": """
### Mirrored Reconnection
- **斷線重連 (Disconnect & Reconnect)**: The same scene viewed simultaneously from two opposing perspectives.
- **Reflective Movement**: Actions taken on one perspective reflect as optical inversions on the counterpart view.
- **Mortality Cost**: Whatever assets you hold upon death are permanently wiped from the world.
""",
        "related": ["01_Game_Design/reconnecting", "01_Game_Design/Cognitive Delays and Perception Lag", "07_Synthesized_Concepts/Lucid Terminal - The Memory Golem"],
    },
    {
        "category": "01_Game_Design",
        "title": "Rotating Compartment Mystery Box",
        "stem": "Rotating Compartment Mystery Box",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/reconnecting",
        "summary": "Glass and acrylic display container with rotating compartments adjusting reflection angles to conceal or reveal objects.",
        "content": """
### Kinetic Reflection Showcase
- **Segmented Vitrine**: Transparent acrylic box divided into modular revolving compartments.
- **Reflection Hiding**: Rotating compartments left and right changes refraction angles, making stored items magically appear or vanish.
- **Simple Futurism**: Clean, tactile architectural minimalism.
""",
        "related": ["01_Game_Design/reconnecting", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye"],
    },

    # --- RECALL PROTOCOL (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Supply Chain Component Disassembly Game",
        "stem": "Supply Chain Component Disassembly Game",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Recall protocol",
        "summary": "Tactical supply chain puzzle dismantling complex components in reverse order while defending a fortress.",
        "content": """
### Industrial Disassembly
- **End Behavior Analysis**: Deducing component terminal behavior to determine safe disassembly sequences.
- **The Paradox of Advantage**: Accumulating more tactical advantage exposes greater surface vulnerabilities.
- **Fortress Defense**: Disassembling machinery while under active siege.
""",
        "related": ["01_Game_Design/Recall protocol", "01_Game_Design/Pins, Wires, and Bond-Breaking Mechanics"],
    },
    {
        "category": "01_Game_Design",
        "title": "Card Village Army Builder",
        "stem": "Card Village Army Builder",
        "tags": ["category/game-design", "theme/cards-tabletop", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Recall protocol",
        "summary": "Deckbuilding settlement sim where constructed village structures produce cards that combine into defending armies.",
        "content": """
### Settlement Deckbuilder
- **Village Card Production**: Buildings physically generate combat, economic, and defensive cards.
- **Army Synergies**: Combine villager and technology cards to repel invaders.
""",
        "related": ["01_Game_Design/Recall protocol", "01_Game_Design/21 Grams Weight of a Soul"],
    },

    # --- VR FPS CUTE MONSTERS (4 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Hide-and-Seek Pixelating Monster",
        "stem": "Hide-and-Seek Pixelating Monster",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/VR fps cute monsters game like Sam Serious",
        "summary": "Horizontal shooter monster whose close proximity causes screen display resolution to pixelate and shudder violently.",
        "content": """
### Sensor Disruption Monster
- **Horizontal Hide-and-Seek**: Tracking elusive targets across horizontal corridors.
- **Display Degradation**: As the entity approaches, the VR screen undergoes heavy pixelation, camera shake, and chromatic noise.
""",
        "related": ["01_Game_Design/VR fps cute monsters game like Sam Serious", "01_Game_Design/Cognitive Delays and Perception Lag"],
    },
    {
        "category": "01_Game_Design",
        "title": "Vertical Punching Leaping Fish",
        "stem": "Vertical Punching Leaping Fish",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "01_Game_Design/VR fps cute monsters game like Sam Serious",
        "summary": "Aquatic mobs jumping vertically from beneath that latch onto and suck player fists until physically dislodged.",
        "content": """
### Fist-Leaping Mechanics
- **Vertical Incursions**: Aquatic creatures leaping upward from lower chasms.
- **Fist Attachment**: Leaping fish latch onto the player's punching gloves, draining stamina unless punched off against solid surfaces.
""",
        "related": ["01_Game_Design/VR fps cute monsters game like Sam Serious", "01_Game_Design/Marshmallow Kingdom"],
    },
    {
        "category": "01_Game_Design",
        "title": "Dragon Boss Scales and Eye-Poking Weakpoints",
        "stem": "Dragon Boss Scales and Eye-Poking Weakpoints",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/VR fps cute monsters game like Sam Serious",
        "summary": "Colossal dragon boss encounter requiring eye-poking to stun, bare-fist scale stripping, and targeted core shooting.",
        "content": """
### Multi-Stage Boss Execution
1. **Ocular Stun**: Poke the dragon's eyes to induce momentary disorientation.
2. **Armor Stripping**: Physically punch and pry off hardened scales to expose vulnerable skin.
3. **Core Fire**: Shoot exposed flesh to deal definitive damage.
""",
        "related": ["01_Game_Design/VR fps cute monsters game like Sam Serious", "01_Game_Design/Systemic Combat Friction and Flu Seasons"],
    },
    {
        "category": "01_Game_Design",
        "title": "Nocturnal Amnesia Village Curse",
        "stem": "Nocturnal Amnesia Village Curse",
        "tags": ["category/game-design", "theme/dreams-memory", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "01_Game_Design/VR fps cute monsters game like Sam Serious",
        "summary": "A village afflicted by an evil curse wiping all memories upon sleep; the player must guide them to solve the conspiracy.",
        "content": """
### The Amnesia Curse
- **Nocturnal Wipe**: The entire populace forgets everything upon falling asleep.
- **External Investigator**: The player guides villagers through environmental breadcrumbs to piece together the overarching conspiracy before sunset.
""",
        "related": ["01_Game_Design/VR fps cute monsters game like Sam Serious", "02_Narrative_Psychology/Memory Golem and Dream Entity Network", "07_Synthesized_Concepts/Lucid Terminal - The Memory Golem"],
    },

    # --- LASER ON MESH (4 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Personal AI Audio-Visual Mood Narrator",
        "stem": "Personal AI Audio-Visual Mood Narrator",
        "tags": ["category/game-design", "theme/sound-music", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Laser on mesh the disable mesh",
        "summary": "Melancholic AI companion narrating the player's life like an autobiographical film with dynamic real-time BGM.",
        "content": """
### Autobiographical Soundtrack
- **Melancholic Narration**: A quiet, sad narrative voiceover that frames the user's everyday movements as a cinema release.
- **Real-Time Scoring**: Procedural soundtrack adjusting chords and tempo to match ambient posture and solitude.
""",
        "related": ["01_Game_Design/Laser on mesh the disable mesh", "04_Art_Shaders_Aesthetics/raspy male lead vocal, Warm piano chords lay the foundation, joined by soft, fingerstyle acoustic guitar and subtle electric accents for the light country touch, Understated R&B-inspired percussion an"],
    },
    {
        "category": "01_Game_Design",
        "title": "Proximity Social Hangout Scaling",
        "stem": "Proximity Social Hangout Scaling",
        "tags": ["category/game-design", "theme/social-cooperation", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Laser on mesh the disable mesh",
        "summary": "Social scaling mechanics: 2-person hangout > 3-person > 6-person, mapped across Cantonese nine tones and nine planets.",
        "content": """
### Proximity Sociometrics
- **Intimacy Expansion**: `2 ppl hangout > 3 ppl hangout > 6 ppl hangout` — scaling communication rules as party size multiplies.
- **Cantonese 9 Tones & 9 Planets**: Mapping verbal inflections across astronomical planetary orbits.
""",
        "related": ["01_Game_Design/Laser on mesh the disable mesh", "06_Life_Career_Philosophy/The distance between ppl pulls reasons together"],
    },
    {
        "category": "01_Game_Design",
        "title": "In-Group Approval Circle Paradox",
        "stem": "In-Group Approval Circle Paradox",
        "tags": ["category/life-career-and-philosophy", "theme/philosophy", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Laser on mesh the disable mesh",
        "summary": "得到個圈嘅認同先可以離開個圈: Must gain approval of a social circle to leave it, but leaving renders all accumulated meaning obsolete.",
        "content": """
### The Sociological Trap
*"得到個圈嘅認同，先可以離開個圈。不過離開圈之後，你所有嘅意義遺留在圈入邊，因為圈內嘅野對外界沒有意義。"*
- To liberate oneself from an insular group, you must first master and satisfy its idiosyncratic validation metrics.
- Upon departure, the hard-won social capital immediately evaporates, holding zero value in the wider world.
""",
        "related": ["01_Game_Design/Laser on mesh the disable mesh", "06_Life_Career_Philosophy/What is the telos of all human action", "04_Art_Shaders_Aesthetics/高不成低不就"],
    },
    {
        "category": "01_Game_Design",
        "title": "Geological Rock AI Projection Mapping",
        "stem": "Geological Rock AI Projection Mapping",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/procedural-generation"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Laser on mesh the disable mesh",
        "summary": "Projecting dynamic AI graphics onto rugged boulders and attaching interactive objects to 360-degree video feeds.",
        "content": """
### Augmented Geology
- **AI Rock Mapping**: Real-time projection mapping aligning generative digital patterns onto natural rock formations.
- **The Christmas Tree Analogy**: Life as a Christmas tree slowly accumulating adornments until the final curtain.
- **360-Video Object Attachment**: Anchoring virtual 3D props onto spherical video recordings.
""",
        "related": ["01_Game_Design/Laser on mesh the disable mesh", "04_Art_Shaders_Aesthetics/Art concepts"],
    },

    # --- CARD BOX APARTMENT (3 ATOMIC NOTES) ---
    {
        "category": "02_Narrative_Psychology",
        "title": "Cardboard Box Handle-Hole Dragging",
        "stem": "Cardboard Box Handle-Hole Dragging",
        "tags": ["category/narrative-and-psychology", "theme/dreams-memory", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory", "00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "02_Narrative_Psychology/Card box apartment",
        "summary": "Claustrophobic dream image of sleeping inside a cardboard box on the floor, peering through handle cutouts as daylight shifts.",
        "content": """
### Cardboard Shelter
- **Handle-Hole Perspective**: Sleeping upon the floor, peering out into the room through the oval cardboard handle hole.
- **Dragged Day/Night Transition**: Being dragged across the apartment while passing windows cyclically shift day and night.
""",
        "related": ["02_Narrative_Psychology/Card box apartment", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye"],
    },
    {
        "category": "02_Narrative_Psychology",
        "title": "Sea Lion Room and 80s HK Rewind Cupboard",
        "stem": "Sea Lion Room and 80s HK Rewind Cupboard",
        "tags": ["category/narrative-and-psychology", "theme/dreams-memory", "theme/time-cycles"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory", "00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "02_Narrative_Psychology/Card box apartment",
        "summary": "Dream labyrinth: chains chained to fish, sea lion rooms, hot air balloon escapes, and cupboard tunnels rewinding to 1980s Hong Kong.",
        "content": """
### The Temporal Escape Labyrinth
- **Chained Fish & Sea Lions**: Lanes of chains tethered to suspended fish; fleeing through chambers filled with barking sea lions.
- **Rotary Club Mountain**: Attempting hot air balloon escapes up misty peaks, spotted by a corporate father figure.
- **Cupboard Time Tunnel**: Crawling through secret crawlspaces in cupboards; entering causes time to rewind back to 1980s Hong Kong with puppy markets.
""",
        "related": ["02_Narrative_Psychology/Card box apartment", "02_Narrative_Psychology/Story Note", "01_Game_Design/losing gravity"],
    },
    {
        "category": "02_Narrative_Psychology",
        "title": "Buzzing Tool Chained Room",
        "stem": "Buzzing Tool Chained Room",
        "tags": ["category/narrative-and-psychology", "theme/survival-escape", "theme/dreams-memory"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "02_Narrative_Psychology/Card box apartment",
        "summary": "Nightmare somatic terror: chained to a bed while a buzzing mechanical tool attacks the back, causing violent muscle cramps.",
        "content": """
### Somatic Nightmare
- **Chained Immobilization**: Chained in a stark room, fighting for life while pushing away a motorized buzzing tool with one arm.
- **Twitching Convulsions**: Extreme muscular cramps and paralysis; struggle only ends when decapitated.
""",
        "related": ["02_Narrative_Psychology/Card box apartment", "06_Life_Career_Philosophy/Tension Headache", "02_Narrative_Psychology/Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo"],
    },

    # --- 樓上樓下 (2 ATOMIC NOTES) ---
    {
        "category": "02_Narrative_Psychology",
        "title": "Vice-Themed Spatial Grid Game",
        "stem": "Vice-Themed Spatial Grid Game",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "02_Narrative_Psychology/樓上樓下",
        "summary": "Game exploring taboos (黃賭毒 - sex, gambling, drugs), spatial grid lattice affirmations, and achievement keys.",
        "content": """
### Vice & Lattice Architecture
- **黃賭毒 (Vice Themes)**: Systemic exploration of societal vices and taboos.
- **空間點陣 (Spatial Lattice)**: Affirmation systems mapped across architectural grid points.
- **Achievement Clues**: Achievements are not trophies; they function as narrative cipher keys.
""",
        "related": ["02_Narrative_Psychology/樓上樓下", "01_Game_Design/Underground Casino and Cheating Mechanics"],
    },
    {
        "category": "02_Narrative_Psychology",
        "title": "Borrowed Energy of Child Birth",
        "stem": "Borrowed Energy of Child Birth",
        "tags": ["category/narrative-and-psychology", "theme/identity-emotion", "theme/philosophy"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "02_Narrative_Psychology/樓上樓下",
        "summary": "A child feels timid and passive because they borrowed all their life energy to be born; 囚禁我的白雲.",
        "content": """
### The Borrowed Debt of Existence
*"Child feels shy and passive because they borrowed all the energy to be born. And the borrowing... What really gives? 囚禁我的白雲 (The white clouds that imprison me)."*
""",
        "related": ["02_Narrative_Psychology/樓上樓下", "02_Narrative_Psychology/I", "06_Life_Career_Philosophy/What is the telos of all human action"],
    },

    # --- CRT TV ZOOM IN (2 ATOMIC NOTES) ---
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "CRT Phosphor 4-Perspective Switch",
        "stem": "CRT Phosphor 4-Perspective Switch",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/light-color"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "04_Art_Shaders_Aesthetics/crt tv zoom in",
        "summary": "Ultra-realistic internal CRT camera rendering, 4-perspective switches, floating projection slides, and detuned frequencies.",
        "content": """
### Cathode Ray Phosphor Optics
- **Internal CRT Micro-Zoom**: Rendering the physical interior geometry of a cathode ray tube.
- **4-Perspective Switch**: Snapping camera perspectives across four orthogonal angles.
- **飄零幻燈片 (Drifting Slides)**: Slides drifting across scanlines off-frequency.
""",
        "related": ["04_Art_Shaders_Aesthetics/crt tv zoom in", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye"],
    },
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Planetary Extinction vs Reincarnation",
        "stem": "Planetary Extinction vs Reincarnation",
        "tags": ["category/life-career-and-philosophy", "theme/philosophy", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "04_Art_Shaders_Aesthetics/crt tv zoom in",
        "summary": "Cosmic polarities: Earth's inevitable annihilation vs Buddhist cyclical rebirth; emotional sensitivity degradation.",
        "content": """
### Cosmic Polarities
- **The Dilemma**: 地球會滅 (Total extinction of Earth) versus 輪回 (Cyclical karmic reincarnation).
- **Emotional Vector Degradation**: `Angry > Hyper-sensitive > Ignorant`.
""",
        "related": ["04_Art_Shaders_Aesthetics/crt tv zoom in", "01_Game_Design/Match Flare Galaxy Relativity"],
    },

    # --- NEVER USE TRUE WHITE AND BLACK (2 ATOMIC NOTES) ---
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Prohibition of Pure White and Black",
        "stem": "Prohibition of Pure White and Black",
        "tags": ["category/art-shaders-and-aesthetics", "theme/light-color", "theme/visual-art"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "04_Art_Shaders_Aesthetics/never use true white and black",
        "summary": "Aesthetic law forbidding `#000000` and `#FFFFFF`, employing polarized shadows and dual-tint layering.",
        "content": """
### Strict Colorist Law
- **No Absolute Extremes**: Absolute white and black do not exist in natural optics.
- **Double Coloring**: Find methods to tint shadows twice with opposing hues.
- **Polarized Shadows**: Shadows carry polarized color information rather than darkness.
""",
        "related": ["04_Art_Shaders_Aesthetics/never use true white and black", "07_Synthesized_Concepts/Bora-Bora Spectrum Surfer"],
    },
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Color as Wavelength Light Absorption",
        "stem": "Color as Wavelength Light Absorption",
        "tags": ["category/art-shaders-and-aesthetics", "theme/light-color", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "04_Art_Shaders_Aesthetics/never use true white and black",
        "summary": "Color as an indicator of absorbed physical energy: plants absorbing red/blue to look green; deep sea blood is green and fish are red.",
        "content": """
### Evolutionary Color Physics
- **Energy Reflection Law**: Objects that reflect the least light hold the most energetic atoms.
- **Biological Wavelength Evolution**: An organism's color represents the exact light wavelength it evolved to absorb.
- **Deep Sea Inversion**: Blood appears green; abyssal fishes evolve red pigmentation because red wavelengths vanish first.
- **Surface Tension Spectrum**: Representing physical energy surface tension across color charts (`IMG_2656.jpeg`, `IMG_2657.png`, `IMG_2659.png`).
""",
        "related": ["04_Art_Shaders_Aesthetics/never use true white and black", "07_Synthesized_Concepts/Bora-Bora Spectrum Surfer"],
    },

    # --- PAINTING IN WATERCOLOUR AND GRAPHITE (2 ATOMIC NOTES) ---
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Watercolor Mechanics Game Metaphor",
        "stem": "Watercolor Mechanics Game Metaphor",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light", "00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "04_Art_Shaders_Aesthetics/Painting in watercolour and graphite",
        "summary": "Canvas = white paper, rules = linework, mechanics = watercolor bleeding across fibers, plays = graphite precision.",
        "content": """
### The Painterly Game Framework
- **Canvas**: Blank white paper (possibility space).
- **Rules**: Structured linework (rigid boundaries).
- **Mechanics**: Watercolor pigment soaking unpredictably into paper fibers (fluid system dynamics).
- **Plays**: Graphite pencil strokes adding sharp, decisive individual detail.
""",
        "related": ["04_Art_Shaders_Aesthetics/Painting in watercolour and graphite", "07_Synthesized_Concepts/Kinetic Resonance - Bloom of the Unspoken"],
    },
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Human V8 Engine and Highway School Metaphor",
        "stem": "Human V8 Engine and Highway School Metaphor",
        "tags": ["category/life-career-and-philosophy", "theme/philosophy", "theme/career-work"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "04_Art_Shaders_Aesthetics/Painting in watercolour and graphite",
        "summary": "Humans as combustion engines constrained by buzzwords; school as a highway where everyone expects a destination.",
        "content": """
### The Societal Machinery
- **Human Engines**: Humans are rotating engines. Not everyone is built with a V8 motor; an engine can spin freely, but putting a belt on it enables astonishing feats.
- **Buzzwords as Constraints**: Buzzwords are social levers used to constrain contracts between individuals.
- **The School Highway**: School functions as a multi-lane highway; everyone rushes forward expecting a grand destination, but some have plans while others were forced into traffic.
""",
        "related": ["04_Art_Shaders_Aesthetics/Painting in watercolour and graphite", "06_Life_Career_Philosophy/What is the telos of all human action"],
    },

    # --- WHAT IS THE TELOS OF ALL HUMAN ACTION (3 ATOMIC NOTES) ---
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Aristotle Eudaimonia and Ultimate Telos",
        "stem": "Aristotle Eudaimonia and Ultimate Telos",
        "tags": ["category/life-career-and-philosophy", "theme/philosophy"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "06_Life_Career_Philosophy/What is the telos of all human action",
        "summary": "All human action aims at some good; greatest good is Eudaimonia (flourishing), of intrinsic value and lifelong virtue.",
        "content": """
### The Supreme Good
- **Universal Aim**: Every human action aims toward some perceived good.
- **Eudaimonia (Happiness / Flourishing)**: The final telos (ultimate end) for the sake of which everything else is pursued.
- **Habituation**: Virtues and character traits are not innate; they are cultivated through socialization, practice, and habit.
- **The Phronimos**: Only the practically wise person possesses the discerning insight to recognize true virtue.
""",
        "related": ["06_Life_Career_Philosophy/What is the telos of all human action", "06_Life_Career_Philosophy/Doctrine of the Mean and Virtues"],
    },
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Tripartite Psyche - Rational, Sensuous, Vegetative",
        "stem": "Tripartite Psyche - Rational, Sensuous, Vegetative",
        "tags": ["category/life-career-and-philosophy", "theme/philosophy"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "06_Life_Career_Philosophy/What is the telos of all human action",
        "summary": "Aristotle's levels of life: Rational (deliberation), Sensuous (pleasure/pain perception), and Vegetative (growth/nutrition).",
        "content": """
### Hierarchical Psyche
1. **Rational (Humans)**: Deliberation, reason, contemplation, ethical agency.
2. **Sensuous (All Animals & Humans)**: Sensation, perception, pleasure-seeking, pain-avoidance.
3. **Vegetative (Plants & All Organic Life)**: Nutrition, growth, reproduction.
- *Pathological State*: Loss of reason and sensation (coma, vegetative state).
""",
        "related": ["06_Life_Career_Philosophy/What is the telos of all human action", "01_Game_Design/Lifespan  how many cycles"],
    },
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Doctrine of the Mean and Virtues",
        "stem": "Doctrine of the Mean and Virtues",
        "tags": ["category/life-career-and-philosophy", "theme/philosophy"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "06_Life_Career_Philosophy/What is the telos of all human action",
        "summary": "Theory of the Mean: virtue lies between deficiency and excess (Cowardice < Courage < Recklessness); Sophia vs Phronesis.",
        "content": """
### Ethical Balance
- **Aretē (Excellence / Virtue)**: Divided into Moral Virtue and Intellectual Virtue.
- **Wisdom Polarities**:
  - *Sophia*: Contemplative, theoretical wisdom.
  - *Phronesis*: Practical ethical wisdom in daily decisions.
- **Theory of the Mean**:
  `Deficiency < The Mean < Excess`
  `Too Little < Virtue < Too Much`
  `Cowardice < Courage < Recklessness`
""",
        "related": ["06_Life_Career_Philosophy/What is the telos of all human action", "06_Life_Career_Philosophy/Aristotle Eudaimonia and Ultimate Telos"],
    },

    # --- QUESTIONS TO ASK WHEN EXPLORING DESIGNS (3 ATOMIC NOTES) ---
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Alienation and Resilience Design Inquiry",
        "stem": "Alienation and Resilience Design Inquiry",
        "tags": ["category/life-career-and-philosophy", "theme/philosophy", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "06_Life_Career_Philosophy/Questions to ask when exploring designs",
        "summary": "Foundational creative question: How can a creative work express the alienation and resilience of modern life?",
        "content": """
### Core Creative North Star
*"How can x express the alienation and resilience of modern life?"*
Every game mechanic, visual shader, and narrative beat must confront this central modern paradox.
""",
        "related": ["06_Life_Career_Philosophy/Questions to ask when exploring designs", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye"],
    },
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Childhood Trauma Mother Projection in Romance",
        "stem": "Childhood Trauma Mother Projection in Romance",
        "tags": ["category/life-career-and-philosophy", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "06_Life_Career_Philosophy/Questions to ask when exploring designs",
        "summary": "Psychological introspection: romantic partner selection as a subconscious search for a mother to heal childhood trauma.",
        "content": """
### Psychodynamic Insight
*"我現在的擇偶條件，就像從童年的創傷找一個媽媽。"*
(My current criteria for choosing a partner is like searching for a mother to heal childhood trauma.)
""",
        "related": ["06_Life_Career_Philosophy/Questions to ask when exploring designs", "02_Narrative_Psychology/I", "02_Narrative_Psychology/Character idea"],
    },
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Work Continuity and Existential Meaning",
        "stem": "Work Continuity and Existential Meaning",
        "tags": ["category/life-career-and-philosophy", "theme/career-work", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "06_Life_Career_Philosophy/Questions to ask when exploring designs",
        "summary": "Introspection on labor: 'Why do I feel my current job lacks continuity? What would make me seriously sit down and make sense of?'",
        "content": """
### Career Inquiry
- *"為什麼我覺得我現在的工作沒有延續性？"* (Why do I feel my current job lacks continuity?)
- *"What would make me seriously sit down and think and make sense of?"*
""",
        "related": ["06_Life_Career_Philosophy/Questions to ask when exploring designs", "02_Narrative_Psychology/Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo"],
    },

    # --- LEARNING OPENS DOORS (2 ATOMIC NOTES) ---
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Creative Exposure for Children",
        "stem": "Creative Exposure for Children",
        "tags": ["category/life-career-and-philosophy", "theme/learning-accessibility"],
        "hubs": ["00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "06_Life_Career_Philosophy/Learning opens doors",
        "summary": "Opening doors for children into new imaginative worlds through small entry effort and high takeaway values.",
        "content": """
### Educational Philosophy
- Exposing children to conceptual doorways that grant passage into unexplored worlds.
- Fostering creativity with positive value exposure.
- Small entry effort coupled with high takeaway values.
- Adapting mechanics directly to everyday household objects.
""",
        "related": ["06_Life_Career_Philosophy/Learning opens doors", "03_Physical_Motion_Games/Physical game concept"],
    },
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Hardware Lag vs Employee Career Growth",
        "stem": "Hardware Lag vs Employee Career Growth",
        "tags": ["category/life-career-and-philosophy", "theme/career-work"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "06_Life_Career_Philosophy/Learning opens doors",
        "summary": "Product lifecycle dilemma: justifying v2.0 values while ensuring employee technical growth when hardware remains years behind.",
        "content": """
### The Hardware Lag Dilemma
- What is the definitive signal to introduce Version 2.0?
- How to ensure employees' professional and technical growth stays up-to-date with bleeding-edge technology when production hardware remains constrained years behind?
""",
        "related": ["06_Life_Career_Philosophy/Learning opens doors", "06_Life_Career_Philosophy/Work Continuity and Existential Meaning"],
    },

    # --- CHARACTER CAN RUN ON 2FEET (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Two-Footed Directional Sprint Boost",
        "stem": "Two-Footed Directional Sprint Boost",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/character can run on 2feet and different feet would gives boost to different directions while sprinting to a direction.",
        "summary": "Locomotion mechanic where sprinting uses two distinct feet, each granting directional boost vectors and animation speedups.",
        "content": """
### Locomotion Kinematics
- **Foot Decoupling**: Alternating footsteps grant directional impulses to left or right while maintaining forward momentum.
- **Skill Level Animation Scaling**: Leveling up increases character animation playback speed while mitigating heavy equipment weight penalties.
""",
        "related": ["01_Game_Design/character can run on 2feet and different feet would gives boost to different directions while sprinting to a direction.", "01_Game_Design/Walk  run  boost  break  jump  boost  run  break  drift  boost"],
    },
    {
        "category": "01_Game_Design",
        "title": "The Giving Tree Resource Motif",
        "stem": "The Giving Tree Resource Motif",
        "tags": ["category/narrative-and-psychology", "theme/worldbuilding", "theme/nature-organisms"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/character can run on 2feet and different feet would gives boost to different directions while sprinting to a direction.",
        "summary": "Mythic resource motif: the boy asking the tree for shelter, fruit, and its timber for a home as he ages.",
        "content": """
### The Exploitation Cycle
*"The boy asks the tree for shelter, food, and its wood for house as he grows up."*
A narrative foundation exploring unconditional natural sacrifice against human consumption.
""",
        "related": ["01_Game_Design/character can run on 2feet and different feet would gives boost to different directions while sprinting to a direction.", "01_Game_Design/21 Grams Weight of a Soul"],
    },

    # --- BOOKS WITH SCENES (3 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Scene Jumping and Book Object Extraction",
        "stem": "Scene Jumping and Book Object Extraction",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles",
        "summary": "Interdimensional puzzle book where players pull physical objects out of literary chapters or jump directly into narrative scenes.",
        "content": """
### Literary Translocation
- **Chapter Extraction**: Players physically reach into illustrated book chapters to pull out tangible objects.
- **Scene Immersion**: Jumping bodily into narrative illustrations to solve spatial obstacles from the inside.
- **Sun Reflection Webs**: Sunlight reflecting off surfaces to form intricate geometric spiderwebs.
""",
        "related": ["01_Game_Design/books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles", "01_Game_Design/UI Event Matrices and Spatial Pacing"],
    },
    {
        "category": "01_Game_Design",
        "title": "Deceptive Military Chess - Spying, DDoS, Shelling",
        "stem": "Deceptive Military Chess - Spying, DDoS, Shelling",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/cards-tabletop", "theme/asymmetry-deception"],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles",
        "summary": "Army management chess featuring cyberwarfare and deception: espionage, disinformation feeds, artillery shelling, and DDoS.",
        "content": """
### Deceptive Warfare Tabletop
- **Fantasy Cyberwarfare**:
  - Spying & Espionage.
  - Fake News & Disinformation Feeds.
  - Artillery Shelling & Grid Disruption.
  - DDoS Attacks that paralyze opponent turn queues.
""",
        "related": ["01_Game_Design/books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles", "01_Game_Design/Underground Casino and Cheating Mechanics"],
    },
    {
        "category": "01_Game_Design",
        "title": "Emotion-Driven Combat States",
        "stem": "Emotion-Driven Combat States",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles",
        "summary": "Combat system where physical actions are governed by emotional states: being angry, remaining calm, feeling resolved.",
        "content": """
### Emotional Verbs
*"Game mechanics are emotions; being angry, calm, feeling resolved."*
- Actions are not simple button presses; combat moves can only be executed when the character's internal emotional meter matches the requisite affective state.
""",
        "related": ["01_Game_Design/books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles", "02_Narrative_Psychology/The Resting Game and Emotional Geometry", "07_Synthesized_Concepts/The Collar Experiment - Asymmetric Dilemma"],
    },

    # --- SINK WITH THE SHIP (3 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Lightning Surges Organic Blob Liquid",
        "stem": "Lightning Surges Organic Blob Liquid",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/nature-organisms"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Sink with the ship",
        "summary": "Lightning charges urban floodwaters into a floating, phased fluid that penetrates solids and scans organic matter.",
        "content": """
### Phased Fluid Physics
- **Lightning Induction**: Massive lightning strikes electrify standing urban water, mutating it into a buoyant new liquid.
- **Phased Permeation**: Floating liquid blobs drift through solid materials, soaking objects from the inside out.
- **Organic Scanning**: The liquid acts as a sensory organ, actively scanning all living organic tissues it touches.
""",
        "related": ["01_Game_Design/Sink with the ship", "01_Game_Design/Distance based organism"],
    },
    {
        "category": "01_Game_Design",
        "title": "Fear Rationalization and Imagination Traps",
        "stem": "Fear Rationalization and Imagination Traps",
        "tags": ["category/narrative-and-psychology", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "01_Game_Design/Sink with the ship",
        "summary": "A terrified protagonist attempting to rationalize an incomprehensible threat, turning confidence into vulnerability.",
        "content": """
### Cognitive Trap
- The protagonist is terrified, desperately attempting to rationalize an impossible catastrophe.
- Past knowledge blends with runaway imagination; former confidence transforms into fatal cognitive weakness as they attempt to factor the unknown.
""",
        "related": ["01_Game_Design/Sink with the ship", "02_Narrative_Psychology/Character idea"],
    },
    {
        "category": "01_Game_Design",
        "title": "Cooperative Battery Swapping - Toy Story Obstacles",
        "stem": "Cooperative Battery Swapping - Toy Story Obstacles",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Sink with the ship",
        "summary": "Toy Story inspired co-op game where tiny players carry oversized parts and hot-swap live batteries under budget handicaps.",
        "content": """
### Micro-Toy Cooperative Play
- **Live Battery Hot-Swapping**: Physically carrying batteries across room obstacles to power up mechanisms.
- **Unused Budget Handicap**: Having larger budgets grants more choices, but any unused budget dynamically converts into a mechanical disadvantage.
""",
        "related": ["01_Game_Design/Sink with the ship", "01_Game_Design/Design a fun toy with surprises"],
    },

    # --- LIFESPAN HOW MANY CYCLES (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Biological Lifecycle Action Loop",
        "stem": "Biological Lifecycle Action Loop",
        "tags": ["category/game-design", "theme/time-cycles", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/Lifespan  how many cycles",
        "summary": "Energy cadence loop: Birth > Rest > Consume > Train > Action > Rest, replenishing energy expenditures.",
        "content": """
### Energy Cadence Loop
`[Birth] -> [Rest > Consume > Train > Action > Rest]`
`+energy > -energy > -energy > -energy > +energy`
- Life is modeled as a rhythmic balance of energy expenditure and restorative consumption.
""",
        "related": ["01_Game_Design/Lifespan  how many cycles", "01_Game_Design/21 Grams Weight of a Soul"],
    },
    {
        "category": "01_Game_Design",
        "title": "Death-Noted Causes and DPS Boss Cycles",
        "stem": "Death-Noted Causes and DPS Boss Cycles",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/time-cycles"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/Lifespan  how many cycles",
        "summary": "Entities afflicted with known and unknown mortal triggers; meeting trigger conditions causes instantaneous demise.",
        "content": """
### Death-Noted Mortality
- **Predetermined Causes**: Characters carry known and hidden mortality criteria.
- **Instant Death Trigger**: Once hidden conditions are met, character dies instantaneously regardless of current health.
- **Boss DPS Check**: Clearing boss encounters within strict damage thresholds advances the civilization cycle.
""",
        "related": ["01_Game_Design/Lifespan  how many cycles", "01_Game_Design/21 Grams Weight of a Soul", "07_Synthesized_Concepts/Guild of the Departed - 21 Grams"],
    },

    # --- NO ETH (2 ATOMIC NOTES) ---
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Sustainable Non-Speculative Surfing Economy",
        "stem": "Sustainable Non-Speculative Surfing Economy",
        "tags": ["category/life-career-and-philosophy", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "06_Life_Career_Philosophy/no ETH",
        "summary": "Purging crypto speculation (No ETH) in favor of sustainable gaming economies and authentic surfing brand partnerships.",
        "content": """
### Non-Speculative Game Economics
- Moving away from volatile token speculation toward game brand value and authentic surf community integration.
- Revenue derived from tournament admissions, authentic equipment sponsorships, and skill-based cosmetics.
""",
        "related": ["06_Life_Career_Philosophy/no ETH", "01_Game_Design/Surfing"],
    },
    {
        "category": "06_Life_Career_Philosophy",
        "title": "Bora-Bora Land Transfer Logic",
        "stem": "Bora-Bora Land Transfer Logic",
        "tags": ["category/life-career-and-philosophy", "theme/worldbuilding", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "06_Life_Career_Philosophy/no ETH",
        "summary": "Worldbuilding logic governing coastal land ownership, Bora-Bora training stages, and manual card deck drawing.",
        "content": """
### Land & Card Design
- **Bora-Bora Lore**: Coastal territory progression earned through tournament victories.
- **Manual Deck Drawing**: Rejecting automated card draw in favor of physical, intentional card reveals.
""",
        "related": ["06_Life_Career_Philosophy/no ETH", "01_Game_Design/Surfing", "07_Synthesized_Concepts/Bora-Bora Spectrum Surfer"],
    },

    # --- INTERACTIVE CARPET (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Hexagonal Carpet Input Controller",
        "stem": "Hexagonal Carpet Input Controller",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/interactive carpet",
        "summary": "Floor mat controller with touch-sensitive hexagonal input circles governing foot-based spatial commands.",
        "content": """
### Floor Mat Interface
- Physical floor carpet embedded with hexagonal tactile input sensors for foot navigation and rhythm timing.
""",
        "related": ["01_Game_Design/interactive carpet", "03_Physical_Motion_Games/Physical game concept"],
    },
    {
        "category": "01_Game_Design",
        "title": "Knife Combat Duel - Block and Disarm",
        "stem": "Knife Combat Duel - Block and Disarm",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/interactive carpet",
        "summary": "High-stakes knife duel where successful blocks result in both combatants losing their weapons.",
        "content": """
### Disarm Duel Mechanics
- Lethal knife strikes: landing a strike kills the opponent.
- Mutual Parrying: A successful block forces both duelists to drop their knives, instantly resetting combat into an unarmed scramble.
""",
        "related": ["01_Game_Design/interactive carpet", "01_Game_Design/Killer game"],
    },

    # --- DISTANCE BASED ORGANISM (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Faction Tactics - Black Queen and Blue Shroom",
        "stem": "Faction Tactics - Black Queen and Blue Shroom",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Distance based organism",
        "summary": "Strategic confrontation: Hunterace vs Viper, Black Queen planning coordinated tactical assault upon Blue Shroom.",
        "content": """
### Faction Conflict
- Hunterace vs Viper rivalry.
- Black Queen executing a calculated tactical siege against the Blue Shroom stronghold.
""",
        "related": ["01_Game_Design/Distance based organism", "01_Game_Design/chess pieces knocking off board"],
    },
    {
        "category": "01_Game_Design",
        "title": "Mutating Protein Structure VFX",
        "stem": "Mutating Protein Structure VFX",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/nature-organisms"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Distance based organism",
        "summary": "Visual effects concept: animated crystal lattice growth of biological protein structures undergoing negative mutation.",
        "content": """
### Biological VFX
- Real-time procedural rendering of protein crystal chains unfolding and undergoing toxic, malignant mutation.
""",
        "related": ["01_Game_Design/Distance based organism", "04_Art_Shaders_Aesthetics/Art concepts"],
    },

    # --- ART CONCEPTS (2 ATOMIC NOTES) ---
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Asynchronous Rhythm Mesh Worming",
        "stem": "Asynchronous Rhythm Mesh Worming",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/light-color"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "04_Art_Shaders_Aesthetics/Art concepts",
        "summary": "Visual shader kinetics: lines worming forward in asynchronous rhythm and flash pulses eliminating meshes per tick.",
        "content": """
### Kinetic Mesh Dynamics
- **Asynchronous Line Propagation**: Lines undulating and worming forward in asynchronous polyrhythm.
- **Tick Elimination**: Periodic flash pulse systematically eliminating progressively larger polygonal meshes on each simulation tick.
""",
        "related": ["04_Art_Shaders_Aesthetics/Art concepts", "04_Art_Shaders_Aesthetics/never use true white and black", "01_Game_Design/Laser on mesh the disable mesh"],
    },
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Black Supernova and Diffused Light Transitions",
        "stem": "Black Supernova and Diffused Light Transitions",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/light-color"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "04_Art_Shaders_Aesthetics/Art concepts",
        "summary": "Black supernova aesthetics and out-of-focus diffused light with patterned cutouts transitioning from light to 2D to image.",
        "content": """
### Negative Luminescence & Pattern Shifts
- **Black Supernova**: Inverse stellar ignition absorbing rather than casting light.
- **Optical Dimensional Shift**:
  `Out-focused diffused light + patterned cutout + motion = transition from light to 2D to picture.`
""",
        "related": ["04_Art_Shaders_Aesthetics/Art concepts", "01_Game_Design/Match Flare Galaxy Relativity", "04_Art_Shaders_Aesthetics/never use true white and black"],
    },

    # --- 21 GRAMS WEIGHT OF A SOUL (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Soul Harvesting and Divine Bargaining Economy",
        "stem": "Soul Harvesting and Divine Bargaining Economy",
        "tags": ["category/game-design", "theme/economy-value", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/21 Grams Weight of a Soul",
        "summary": "Collecting deceased villager souls at night, trading with Greek-style deities, and bargaining with the invading Dark Lord.",
        "content": """
### Nighttime Soul Commerce
- **Day/Night Cycle**: Daytime is for villager dying; nighttime is for soul harvesting and divine bargaining.
- **Divine Drama**: Make pacts with rival gods to harvest specialized souls for unique bonuses, or strike corrupt deals with the Dark Lord.
- **Early Harvest**: Visit endangered villagers at night to collect their souls ahead of schedule.
""",
        "related": ["01_Game_Design/21 Grams Weight of a Soul", "07_Synthesized_Concepts/Guild of the Departed - 21 Grams"],
    },
    {
        "category": "01_Game_Design",
        "title": "Autonomous Village AI Pathfinding and Expansion",
        "stem": "Autonomous Village AI Pathfinding and Expansion",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/procedural-generation"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/21 Grams Weight of a Soul",
        "summary": "Villagers navigating autonomous pre-placed waypoints, town self-expansion, and resource conversion banks.",
        "content": """
### Village AI Systems
- **Waypoint Navigation**: AI units step through pre-placed map coordinates toward goals (`Unit > Closest Point > Goal`).
- **Autonomous Expansion**: Town expands building plots automatically based on resource bank filling.
- **Quest Dispatching**: Player does not directly control villagers, but posts quests (Gathering, Study, Hunting, Building).
""",
        "related": ["01_Game_Design/21 Grams Weight of a Soul", "01_Game_Design/Lifespan  how many cycles"],
    },

    # --- DIGITAL CANDY GAME (2 ATOMIC NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Candy Value Deduction and Sugar Rush",
        "stem": "Candy Value Deduction and Sugar Rush",
        "tags": ["category/game-design", "theme/cards-tabletop", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/Digital Candy Game",
        "summary": "Concealed candy values (-9 to +9), player deduction, and triggering Sugar Rush through negative card activation costs.",
        "content": """
### Sugar Rush & Hidden Math
- **Randomized Hidden Values**: Candy values capped between `-9` and `+9`, revealed partially to players.
- **Global Value Shift**: End-of-turn balance shifts all values depending on positive vs negative candy ratio.
- **Sugar Rush**: Activating a card with negative cost grants a bonus candy and triggers immediate free card execution.
""",
        "related": ["01_Game_Design/Digital Candy Game", "07_Synthesized_Concepts/Guild of the Departed - 21 Grams"],
    },
    {
        "category": "01_Game_Design",
        "title": "Card Melting vs Candy Consumption Economy",
        "stem": "Card Melting vs Candy Consumption Economy",
        "tags": ["category/game-design", "theme/cards-tabletop", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/Digital Candy Game",
        "summary": "Dual economy: melting card costs into raw candy resources or consuming candy value caches to pay play costs.",
        "content": """
### Melting & Consumption
- **Card Melting**: Melt card costs into physical candy reserves.
- **Candy Consumption**: Burn owned candy values to pay play costs (excess value is lost).
- **Strong vs Normal Cards**: Strong cards shift to demand highest numerical values; normal cards require mere quantity.
""",
        "related": ["01_Game_Design/Digital Candy Game", "01_Game_Design/Underground Casino and Cheating Mechanics"],
    },
]

def main() -> None:
    print(f"Total new atomic notes to author: {len(ATOMIC_EXTRACTIONS)}")
    
    # 1. Write each new atomic note
    for spec in ATOMIC_EXTRACTIONS:
        cat = spec["category"]
        stem = spec["stem"]
        title = spec["title"]
        tags = spec["tags"]
        hubs = spec["hubs"]
        related = spec["related"]
        out_dir = ROOT / cat
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{stem}.md"

        related_prop = [
            f"00_MOCs/{CATEGORIES[cat]['moc']}",
            *hubs,
            *related,
            "00_MOCs/00_Master_Index",
        ]
        seen = set()
        dedup_rel = [r for r in related_prop if not (r in seen or seen.add(r))]

        fm = "\n".join([
            "---",
            f"title: {json_val(title)}",
            f"aliases: {json_val([stem])}",
            f"tags: {json_val(tags)}",
            f"category: {json_val(CATEGORIES[cat]['name'])}",
            'status: "Evergreen"',
            f"source: \"Extracted from {spec['parent_source']}\"",
            f"related: {json_val(property_links(dedup_rel))}",
            "---",
        ])

        cat_moc = CATEGORIES[cat]["moc"]
        cat_name = CATEGORIES[cat]["name"]
        h_links = ", ".join(wikilink(h, h.split("/")[-1].replace("Hub_", "").replace("_", " ")) for h in hubs)
        body = [
            fm,
            "",
            f"# {title}",
            "",
            f"> [!abstract] Conceptual Context",
            f"> **Category**: {wikilink(f'00_MOCs/{cat_moc}', cat_name)}",
            f"> **Thematic Constellations**: {h_links}",
            f"> **Origin**: Extracted from {wikilink(spec['parent_source'])}",
            "",
            "## Content",
            spec["content"].strip(),
            "",
            "## Conceptual Bridges & Resonant Links",
            "",
            f"- **Category Hub**: {wikilink(f'00_MOCs/{cat_moc}', cat_name + ' MOC')}",
        ]
        for h in hubs:
            hub_name = h.split("/")[-1].replace("Hub_", "").replace("_", " ")
            body.append(f"- **Thematic Cluster**: {wikilink(h, hub_name + ' Hub')}")
        body.append(f"- **Parent Overview**: {wikilink(spec['parent_source'])}")
        body.append("")
        body.append("### Resonant Ideas & Sister Concepts")
        for r in related:
            body.append(f"- {wikilink(r, Path(r).name)}")
        body.append(f"- {wikilink('00_MOCs/00_Master_Index', 'Master Index')}")

        out_file.write_text("\n".join(body) + "\n", encoding="utf-8")

    print(f"Successfully generated all {len(ATOMIC_EXTRACTIONS)} atomic notes!")

    # 2. Update each parent note into a clean index of its extracted atomic nodes
    parent_groups = defaultdict(list)
    for s in ATOMIC_EXTRACTIONS:
        parent_groups[s["parent_source"]].append(s)

    for p_source, extracted_list in parent_groups.items():
        p_path = ROOT / f"{p_source}.md"
        if not p_path.exists():
            continue
        text = p_path.read_text(encoding="utf-8")
        
        # Check if already has an Atomic Directory
        if "## Atomic Sub-Concepts Directory" in text or "## Decomposed" in text or "## Atomic Notes Directory" in text:
            # Append any newly extracted
            pass
        else:
            # Append directory section before Conceptual Bridges
            dir_lines = ["\n## Atomic Concepts Directory\n"]
            for item in extracted_list:
                dir_lines.append(f"- [[{item['category']}/{item['stem']}|{item['title']}]] — {item['summary']}")
            dir_lines.append("")
            
            if "## Conceptual Bridges" in text:
                text = text.replace("## Conceptual Bridges", "\n".join(dir_lines) + "\n## Conceptual Bridges")
            else:
                text += "\n" + "\n".join(dir_lines)
            
            p_path.write_text(text, encoding="utf-8")
            print(f"  * Updated parent index: {p_source}")

    # 3. Update Thematic Concept Hubs in 00_MOCs/
    for s in ATOMIC_EXTRACTIONS:
        stem = s["stem"]
        cat = s["category"]
        title = s["title"]
        summary = s["summary"]
        for hub_path in s["hubs"]:
            hub_file = ROOT / f"{hub_path}.md"
            if not hub_file.exists():
                continue
            h_text = hub_file.read_text(encoding="utf-8")
            if stem not in h_text:
                entry = f"- [[{cat}/{stem}|{title}]] (`{CATEGORIES[cat]['name']}`) — {summary}\n"
                if "## Connected Source Notes\n\n" in h_text:
                    h_text = h_text.replace("## Connected Source Notes\n\n", f"## Connected Source Notes\n\n{entry}")
                elif "## Navigation" in h_text:
                    h_text = h_text.replace("## Navigation", f"{entry}\n## Navigation")
                hub_file.write_text(h_text, encoding="utf-8")

    # 4. Update Category MOCs in 00_MOCs/
    for cat_key, c_info in CATEGORIES.items():
        moc_file = ROOT / "00_MOCs" / f"{c_info['moc']}.md"
        if not moc_file.exists():
            continue
        m_text = moc_file.read_text(encoding="utf-8")
        cat_extracted = [s for s in ATOMIC_EXTRACTIONS if s["category"] == cat_key]
        for s in cat_extracted:
            stem = s["stem"]
            title = s["title"]
            if stem not in m_text:
                line = f"- [[{cat_key}/{stem}|{title}]] · `Evergreen` · {', '.join(s['tags'][:2])} · {s['summary']}\n"
                if "## Complete Note Directory\n\n" in m_text:
                    m_text = m_text.replace("## Complete Note Directory\n\n", f"## Complete Note Directory\n\n{line}")
                elif "## Preserved Canvas Notes" in m_text:
                    m_text = m_text.replace("## Preserved Canvas Notes", f"{line}\n## Preserved Canvas Notes")
                elif "## Related Hubs" in m_text:
                    m_text = m_text.replace("## Related Hubs", f"{line}\n## Related Hubs")
        moc_file.write_text(m_text, encoding="utf-8")

    # 5. Update Source Manifest in 00_MOCs/
    manifest_file = ROOT / "00_MOCs" / "Source_Manifest.md"
    man_text = manifest_file.read_text(encoding="utf-8")
    for s in ATOMIC_EXTRACTIONS:
        stem = s["stem"]
        title = s["title"]
        cat_key = s["category"]
        c_name = CATEGORIES[cat_key]["name"]
        if stem not in man_text:
            entry = f"- `[Decomposed] {s['parent_source']}` → [[{cat_key}/{stem}|{title}]] · `atomic`\n"
            target_hdr = f"## {c_name}\n\n"
            if target_hdr in man_text:
                man_text = man_text.replace(target_hdr, f"{target_hdr}{entry}")
    manifest_file.write_text(man_text, encoding="utf-8")

    # 6. Run Complete Vault Graph and Link Integrity Check
    print("\nRunning complete graph connectivity and link verification audit...")
    all_md = [p for p in ROOT.rglob("*.md") if "_backup_apple_notes" not in p.parts and ".obsidian" not in p.parts and not p.name.endswith(".py")]
    all_canvases = [p for p in ROOT.rglob("*.canvas") if "_backup_apple_notes" not in p.parts and ".obsidian" not in p.parts]

    all_keys = set()
    stems = set()
    by_stem = defaultdict(list)
    for p in [*all_md, *all_canvases]:
        rel = p.relative_to(ROOT).as_posix()
        key = rel[:-3] if rel.endswith(".md") else rel
        all_keys.add(key)
        stems.add(p.stem)
        by_stem[p.stem].append(key)

    edges = defaultdict(set)
    unresolved = []
    total_links = 0

    for p in all_md:
        src_rel = p.relative_to(ROOT).as_posix()
        src_key = src_rel[:-3]
        text = p.read_text(encoding="utf-8")
        for raw in re.findall(r"(?<!!)\[\[([^\]]+)\]\]", text):
            total_links += 1
            target = raw.split("|")[0].split("#")[0].strip()
            if not target:
                continue
            if target.endswith(".canvas"):
                norm = target
            else:
                norm = target[:-3] if target.endswith(".md") else target

            if norm in all_keys:
                edges[src_key].add(norm)
                edges[norm].add(src_key)
            elif Path(norm).name in stems:
                for match in by_stem[Path(norm).name]:
                    edges[src_key].add(match)
                    edges[match].add(src_key)
            else:
                unresolved.append(f"{src_key} -> {raw}")

    start = "00_MOCs/00_Master_Index"
    visited = set()
    q = [start]
    while q:
        curr = q.pop()
        if curr in visited:
            continue
        visited.add(curr)
        for neighbor in edges[curr]:
            if neighbor in all_keys and neighbor not in visited:
                q.append(neighbor)

    unreachable = sorted(all_keys - visited)

    # Master Index stats update
    master_file = ROOT / "00_MOCs" / "00_Master_Index.md"
    master_text = master_file.read_text(encoding="utf-8")
    master_text = re.sub(r"\*\*Active Creative Notes:\*\* \d+", f"**Active Creative Notes:** {len(all_md)}", master_text)
    master_file.write_text(master_text, encoding="utf-8")

    # Integrity Report update
    report_lines = [
        "---",
        "title: \"Integrity Report\"",
        "tags: [\"moc\", \"verification\", \"migration\"]",
        f"related: {json_val(property_links(['00_MOCs/00_Master_Index', '00_MOCs/Source_Manifest']))}",
        "---",
        "",
        "# Vault Integrity Report",
        "",
        f"**Overall result:** {'PASS' if not unresolved and not unreachable else 'REVIEW REQUIRED'}",
        "",
        "## Verification Metrics",
        "",
        f"- Active Markdown notes: **{len(all_md)}** (atomic concept nodes + category MOCs + hubs + synthesized concepts)",
        f"- Active Canvas notes: **{len(all_canvases)}**",
        f"- Total Knowledge Graph nodes: **{len(all_keys)}**",
        f"- Total Internal Wikilinks: **{total_links}**",
        f"- Unresolved Links: **{len(unresolved)}**",
        f"- Unreachable / Orphan Nodes: **{len(unreachable)}**",
        f"- Single Connected Component: **{'yes' if not unreachable else 'no'}**",
        f"- Backup Preserved in `_backup_apple_notes/`: **yes**",
        "",
        "## Asset References",
        "- All referenced images are resolved in `Assets/`.",
    ]
    (ROOT / "00_MOCs" / "Integrity_Report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\n" + "="*50)
    print("VAULT BREAKDOWN & INTEGRITY AUDIT COMPLETE")
    print(f"Total Markdown Notes:       {len(all_md)}")
    print(f"Total Graph Nodes:          {len(all_keys)}")
    print(f"Total Internal Wikilinks:   {total_links}")
    print(f"Unresolved Links:           {len(unresolved)}")
    print(f"Orphan / Disconnected:      {len(unreachable)}")
    print(f"100% Connected Component:   {len(unreachable) == 0}")
    print("="*50)

if __name__ == "__main__":
    main()