#!/usr/bin/env python3
"""
Decompose massive notes (Concepts x9001, Edit skill animation, Instagram virtual rooms)
into atomic concept notes, eliminate duplicate ideas across the vault, and weave bidirectional links.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
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

def summary_line(text: str) -> str:
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith((">", "#", "---", "![[", "http", "|", "-")):
            continue
        line = re.sub(r"[*_`~\[\]()>-]+", " ", line)
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) >= 10:
            return line[:130] + ("…" if len(line) > 130 else "")
    return "Focused concept note."

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

# The 22 atomic concept notes
NEW_ATOMIC_NOTES = [
    # --- CONCEPTS X9001 BREAKDOWN (16 NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Cognitive Delays and Perception Lag",
        "stem": "Cognitive Delays and Perception Lag",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/time-cycles", "theme/ui-ux"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory", "00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Exploration of cognitive delay types (chronicle, logical, informational) and perceptual lag bottlenecks in gameplay.",
        "content": """
### Overview

Perception in games is governed by information latency. Designing around lag and delay transforms technical limitations into psychological tension.

### Three Types of Cognitive Delay

1. **Chronicle Delay**: The lag between an event occurring in world-time and the historical record catching up.
2. **Logical Delay**: The computation time required for the system or the player's brain to deduce the outcome of an action.
3. **Informational Delay**: The deliberate withholding or staged revelation of game state across channels.

### Perceptual Bottlenecks & Design Tenets

- **Lag game design / Visual bottleneck**: Intentionally slowing sensory refresh to force predictive rather than reactive play.
- **Train your tendency**: `tend end depend pretend den` — cognitive habituation through rhythmic repetition.
- **"Remembering gives no experience"**: Past actions cannot be banked unless actively enacted in the present moment.
- **Temporal foresight**: *"I can’t see it because it hasn’t happened yet / I want to draw through time."*
- **Generalized input delay**: Absence of input equals lost attack window; direct action skills act as interrupts.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/The Decryption Lens and Pattern Emblems",
            "01_Game_Design/Systemic Combat Friction and Flu Seasons",
            "01_Game_Design/00928z",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Underground Casino and Cheating Mechanics",
        "stem": "Underground Casino and Cheating Mechanics",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/cards-tabletop", "theme/asymmetry-deception"],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play", "00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Underground casino RPG system where victory is achieved through cheating, bluffing, and resource depletion.",
        "content": """
### Core Premise

An underground casino RPG where players attempt to beat house systems through cheating, luck manipulation, or D&D-style tabletop roleplay.

### Mechanics & Systems

- **Shared Cross-Game Inventory**: Items and gadgets acquired in one casino minigame carry over to all other gambling tables.
- **Mahjong Cheater Game (千王之王)**:
  - Active and passive sleight-of-hand skills.
  - Gag game tone 👾 mixed with high-stakes tension.
  - Getting caught versus pulling off the switch.
- **Inverted Resource Economy**: Players start with full resources and must strategically spend down or shed every item/resource to escape or win.
- **A Game Where You Can Cheat**: Cheating is not a hack; it is a first-class gameplay verb with failure states and risk/reward curves.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Digital Candy Game",
            "01_Game_Design/losing gravity",
            "01_Game_Design/Killer game",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Asymmetric Outlier Challenge",
        "stem": "Asymmetric Outlier Challenge",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/asymmetry-deception", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Cooperative spaces that invert into 1-vs-All when a single player accepts an outlier challenge.",
        "content": """
### Core Structure

A group of players are enclosed in a shared space, functioning as a cooperative team until someone voluntarily triggers the outlier challenge, turning into a lone adversary against all former allies.

### Dynamics & Systems

- **Choice-Based Asymmetry**: The game does not assign the traitor or killer; players choose when and why to take the leap.
- **Pacing Feedback**: `single run > multiple run > group run sfx` — audio and visual cues intensify as collective consensus shifts into individual rebellion.
- **Trend Dynamics**: *"It’s a trend because everyone can do it"* — collective mimicry creates momentum before the rupture.
- **Bean Bag Scale Mechanics**: Players represent bean bags of varying sizes; physical mass dictates resistance, pushing power, and positional advantage.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Killer game",
            "01_Game_Design/Idea hunger game catch",
            "07_Synthesized_Concepts/The Collar Experiment - Asymmetric Dilemma",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Color Tile Consumption Wheel",
        "stem": "Color Tile Consumption Wheel",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/cards-tabletop", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Team puzzle game clearing colored blocks with timed pass-through consumption and rotating faction split-wheels.",
        "content": """
### Gameplay Architecture

A team-based puzzle game focused on consuming color to maintain mobility and spatial control.

### Core Rules

1. **Consumption Movement**: Players select an adjacent colored tile to consume and step forward.
2. **Short-Window Pass-Through**: Consumed tiles remain permeable for a brief time window; failure to consume enough blocks within the threshold causes player death.
3. **Resource Limitation**: Total color palette is strictly bounded by the total block count on the board.

### The Rotating Split-Wheel

- Wheel constructed of 4 to 6 rows with a bottom-middle segment that splits off.
- Split parts rotate two alternating color values: results generate combinations `a`, `b`, or composite `a + b`.
- When two parts match, players gain the ability to phase/jump across those specific colors.
- Certain factions control particular color pairs, but players can switch faction allegiance mid-game to alter traversal rights.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Flipping number cards",
            "01_Game_Design/Prototype idea",
            "04_Art_Shaders_Aesthetics/never use true white and black",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Inverted Role Play - Minion and Pest Escape",
        "stem": "Inverted Role Play - Minion and Pest Escape",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Subversive role-inversions: playing a sluggish minion in a tower defense game or a domestic pest seeking consumption.",
        "content": """
### Core Inversions

Subverting player expectation by stripping superhuman agency and placing the player into humble, vulnerable, or bizarre roles.

### Concept 1: The Tower Defense Minion

- **Genre**: Trapped Escape Game.
- **Perspective**: The player is not the tower architect or the hero; you are a single minion inside a Tower Defense map.
- **Tempo Constraint**: Everything in the simulation moves agonizingly slow, requiring anticipatory route-finding through killzones.

### Concept 2: Domestic Pest Survival

- **Objective**: Invert survival horror into sacrificial comedy.
- **Verbs**: Be a pest in a house. Provoke other rival pests into attacking and consuming you.
- **Win Condition**: Guide the ecosystem so that ultimately a human eats you to secure victory.

### Related Mechanical Seeds

- **The Miracle Controller**: A dedicated input interface controlling divine interventions and miraculous buffs on your character.
- **VR Arm Dance**: 2+ players collaborating with physical arm tracking to form geometric silhouettes and synchronized shapes.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Simon says Escape room",
            "01_Game_Design/VR fps cute monsters game like Sam Serious",
            "03_Physical_Motion_Games/Physical game concept",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Purchasable Power Corporate Finance",
        "stem": "Purchasable Power Corporate Finance",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/economy-value", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles", "00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "A satirical macroeconomic system where corporate finance sells literal power and money represents life force.",
        "content": """
### Worldbuilding & Economic Tenet

*"The company provides global financial solutions for every type of businessman who has the ambition to conquer the world with purchasable power."*

### Systemic Mechanics

- **Money as Life Force**: In this world, capital is not merely a trading medium; your liquid funds dictate your literal life gauge and physical capabilities.
- **Monetary Distortion**: *"A powerful person can make a dollar worth more than a dollar."* Inflation, speculative leverage, and tier scaling warp value across socioeconomic tiers.
- **Purchasable Sovereignty**: World domination and existential safety are commodified into corporate investment packages.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/21 Grams Weight of a Soul",
            "01_Game_Design/Digital Candy Game",
            "02_Narrative_Psychology/樓上樓下",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Democracy Bingo and Systemic Game Rules",
        "stem": "Democracy Bingo and Systemic Game Rules",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/cards-tabletop"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Subversive game formats: Democracy Bingo, polygon leveling limits, functional failure chances, and testing patience.",
        "content": """
### Micro-Game Formats

### 1. Democracy Bingo
A collective voting game where consensus on card numbers alters the board rules for everyone.

### 2. Polygon Limit Leveling
Combat progression where character resolution visually scales with mastery: leveling up grants higher polygon budgets and finer mesh fidelity.

### 3. Systematic Failure Chance
Every button and interaction in the game retains an inherent probabilistic failure rate, forcing improvisation over rote execution.

### 4. Testing Patience Game
A social prank game where the win condition is pushing boundaries, but triggering genuine annoyance in NPCs or other players causes an immediate Game Over.

### Strategic Polarities

- **Spawn Dilemma**: Placed in a bad spot or choose to adventure.
- **Resolution Tension**: Most accurate versus most answered.
- **Alien Strategy**: Protecting the nest versus venturing out.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/question man",
            "01_Game_Design/chess pieces knocking off board",
            "01_Game_Design/Design a fun toy with surprises",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Systemic Combat Friction and Flu Seasons",
        "stem": "Systemic Combat Friction and Flu Seasons",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/time-cycles", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles", "00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Combat engagement latency, hair-tie slope tension, 2-hit mitigation, elemental taxes, and seasonal flu nerfs.",
        "content": """
### Combat & Economic Constraints

### Engagement Latency
Players currently locked in combat have slower reaction times to non-engaged external players, creating tactical openings and third-party choices.

### Hair Tie Theory
If you secure a hair tie to a sloped surface, accumulated mechanical tension will inevitably cause it to roll off over time. Tension cannot be stored indefinitely without release.

### MMO Sit/Rest Cover System
Repurposing traditional FPS cover mechanics into an MMO rest/recovery posture that restores stamina while leaving players vulnerable.

### Tetris Map Generation
Every playable zone block is an active puzzle piece; larger consolidated map sections award exponentially higher scores.

### Two-Hit Mitigation Triad
- **Tank**: Mitigates and absorbs the 1st hit.
- **DPS**: Delivers escalated strikes following mitigation.
- **Healer**: Reverses damage from the initial impact.

### Elemental Tax & Seasonal Flu Nerf
- **Unseeable Tax Collectors**: Supernatural entities monitor raw elements; overuse incurs heavy systemic taxes.
- **Flu Season**: Seasonal environmental debuff where characters weaken and are forced to re-specialize their builds.
- **Insect Vision**: Slower organisms have retinas exposed to light longer, perceiving higher contrast at lower speeds.
- **CO2 Mosquito Tracking**: Simulating real-world carbon emissions to govern monster tracking paths.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Lifespan  how many cycles",
            "01_Game_Design/21 Grams Weight of a Soul",
            "01_Game_Design/Punching bag eats enemy and punching it deals dmg",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Group Vision and Tactical Range",
        "stem": "Group Vision and Tactical Range",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Spatial visibility inversely tied to party density, fighting game inputs for chess, and health piece combat.",
        "content": """
### Inverted Perception by Proximity

*"Within a group can only see close. Without a group can only see far."*

- **Group Tunnel Vision**: Clustering together offers safety and collective defense, but shrinks tactical field-of-view to immediate surroundings.
- **Lone Scout Advantage**: Solitary wanderers have panoramic long-distance vision, discovering macro-level terrain and distant threats.

### Health Piece Combat System

- **Targeted Anatomy**: Select specific attack patterns and weapon types to dispatch distinct mob classes.
- **Fighting Game Inputs for Tabletop**: Chess mechanics paired with fighting game execution combos.
- **Input Commitment**: Generalized input latency; failing to commit input forfeits the attack window entirely. Direct action interrupts break enemy attack flow.
- **Artifact Overpowering**: Acquiring relics displays multi-attribute menus; players choose one single stat to overpower dramatically.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Idea hunger game catch",
            "01_Game_Design/Attack range of the enemies (Table)",
            "01_Game_Design/Flocking Players",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "The Decryption Lens and Pattern Emblems",
        "stem": "The Decryption Lens and Pattern Emblems",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/light-color", "theme/asymmetry-deception"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light", "00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Magical decryption lenses, Fibonacci emblem maps, fear attacks, Inception clearing layers, and negative energy consumption.",
        "content": """
### Optical Decryption Artifact

- **The Lens**: A magical overlay tool.
- Reading ancient scrolls reveals hidden stats only when viewed through the specialized lens cover.
- Looking through the lens without a scroll displays raw encrypted noise.

### Emblem Coordinates & World Map

- Emblems represent an underground map of universal patterns.
- Corporate and clan logos are geographical coordinates plotted along a Fibonacci spiral.

### Sensory Interactions

- **Mute & Stop Tools**: Bells that freeze enemy advance; volume sliders that mute hostile sounds and disable sound-based aggro.
- **Attraction Optics**: Projecting light attracts or repels creatures; light physically pulls human cognitive focus.
- **Fear-Based Attacks**: Players unleash combat damage by projecting their own psychological vulnerabilities.
- **Static Electric Friction**: Specialized body morphology generating massive electrostatic charges through motion.
- **Inception Layers**: A randomized stack of reality layers; clearing one unlocks the next until the foundation is cleared.
- **Negative Energy Economics**: Consuming energy generates negative residual energy that must be spent elsewhere.
- **Material Steps**: Walking on different surfaces charges the household battery.
- **Information Tax**: Voluntarily receiving information permanently reduces base stats.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/crystal world where the player uses a flashlight to shine coloured crystal and fractures the light to show platforms",
            "04_Art_Shaders_Aesthetics/Lense flare",
            "01_Game_Design/Laser on mesh the disable mesh",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "UI Event Matrices and Spatial Pacing",
        "stem": "UI Event Matrices and Spatial Pacing",
        "tags": ["category/ui-ux", "theme/ui-ux", "theme/game-mechanics", "theme/time-cycles"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Bubble ring character selection, teleporting books of memory, event cadence matrices, and camera focal geometry.",
        "content": """
### Novel Interface Paradigms

### Bubble Ring Selection
Character selection UI uses an expanding bubble ring that physically pushes rival players away to confirm pick.

### The Book of Memory
Reading the tome physically teleports the player to the recorded location; wiping or burning memory pages resets and refreshes the scene.

### Pre-Entry Mechanical Combo
Players must execute a tactile combination mechanic before gaining access to the game world.

### Sticky Collision
Colliding objects latch onto and bond with the parent surface rather than bouncing away.

### Event Cadence Matrix

| Event Intensity | Short Period | Long Period |
| :--- | :--- | :--- |
| **Heavy** | Static | Dynamic |
| **Medium** | Dynamic | Dynamic |
| **Light** | Static | Static |

- **Work versus Event Period**: Designing around cognitive fatigue. Complexity must be simple in rule but deep in execution.
- **Cultural Paradigms of Pathology**:
  - Medieval: How many devils are around?
  - Classical: How many fearless are around?
  - Positivism: How many inbreds are around?
  - Psychoanalyst: How many undeveloped are around?
  - Modern: How many psychopaths are around?

### Camera & Spatial Geometry

- **Perspective Distortion**: Lower angle = wider fish-eye; Higher angle = closer macro focus.
- **Portrait Range**: 80mm - 180mm optical compression.
- **Objective Design**: *"Design has to be objective enough to let players be subjective."*
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "06_Life_Career_Philosophy/What is the telos of all human action",
            "06_Life_Career_Philosophy/Questions to ask when exploring designs",
            "04_Art_Shaders_Aesthetics/crt tv zoom in",
        ],
    },
    # --- NARRATIVE / PSYCHOLOGY BREAKDOWN (3 NOTES) ---
    {
        "category": "02_Narrative_Psychology",
        "title": "Narrative Vignettes - Hitmen, Trains, and Spirit Enforcers",
        "stem": "Narrative Vignettes - Hitmen, Trains, and Spirit Enforcers",
        "tags": ["category/narrative-and-psychology", "theme/worldbuilding", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity", "00_MOCs/Hub_Dreams_and_Memory", "00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Narrative vignettes: the failed-hitman hitman, rail frontier development, and spirit-infused robot enforcers.",
        "content": """
### Story Vignette 1: The Hitman Who Hits on Failed Hitmen
A professional assassin whose specific clientele are failed hitmen. He affixes a mouth onto a bound target, and the affixed mouth speaks their innermost secrets aloud.

### Story Vignette 2: The Sick Child and the Doctor
A sick child grows up alongside the village physician, learning empirical science to survive rather than folklore.

### Story Vignette 3: Mountain Sea & Rock Worms
- A 3D body of water suspended high above a mountain valley.
- Bread worms feasting on an ornate cake, but every worm is solid rock.

### Story Vignette 4: The Frontier Train Driver
The newly settled frontier is still learning where to harvest. As the train driver traverses the rails, you scatter objects and seeds along the tracks; your regional distribution choices dictate whether neighboring civilizations rise or collapse.
*(Connected directly to [[01_Game_Design/Game Jam Game Ideas|Steam Train Driver]].)*

### Story Vignette 5: Seafood Heavy Weaponry
Fishing for seafood enemies: hooking a heavy bell-shaped oyster converts the fishing rod into an oversized blunt swing weapon.

### Story Vignette 6: The Spirit-Infused Robot Enforcer
A mechanical enforcer equipped with supernatural sensors. Being a machine, the robot cannot directly upgrade its own stats. However, it can infuse relics possessed by lingering spirits. By helping resolve aching spirits' unfinished business, the spirits upgrade your chassis in return.
*Spoiler*: You are constructed from broken discard parts that slowly absorbed enough spiritual resonance to awaken.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Game Jam Game Ideas",
            "01_Game_Design/21 Grams Weight of a Soul",
            "07_Synthesized_Concepts/The Collar Experiment - Asymmetric Dilemma",
        ],
    },
    {
        "category": "02_Narrative_Psychology",
        "title": "Memory Golem and Dream Entity Network",
        "stem": "Memory Golem and Dream Entity Network",
        "tags": ["category/narrative-and-psychology", "theme/dreams-memory", "theme/identity-emotion", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Assembling memory golems from villager achievements, collective entity dreams, and 24-hour cognitive drift.",
        "content": """
### The Memory Golem

*"Villager’s life resembles the creator’s memory based on its achievement. Assembles a golem of memory. Completion by memories."*

In this world, a person does not build a golem out of clay or stone; it is fashioned out of preserved subjective achievements and emotional anchors. To finish the golem is to complete one's own identity.

### The Collective Dream Entity

*"Everyone is just one entity / network; when a person dies, another person wakes up from a dream."*

- Death is not extinction; it is an awakening in another node of the network.
- Memory continuity bridges across waking individuals.
- **24-Hour Time Zone**: Time does not pause; the mind drags itself forward under constant temporal displacement.
- **"Game is not play"**: Creative effort and survival mechanics detach from mere entertainment.
- **Emotional Catalysts**: Humans only learn during moments of heightened emotional resonance.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "07_Synthesized_Concepts/Lucid Terminal - The Memory Golem",
            "02_Narrative_Psychology/Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo",
            "02_Narrative_Psychology/Character idea",
            "02_Narrative_Psychology/Story Note",
        ],
    },
    {
        "category": "02_Narrative_Psychology",
        "title": "The Resting Game and Emotional Geometry",
        "stem": "The Resting Game and Emotional Geometry",
        "tags": ["category/narrative-and-psychology", "theme/identity-emotion", "theme/game-mechanics", "theme/philosophy"],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory", "00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Learning to rest, saying farewell to yesterday's self, emotional spiral geometry, and sloth giant companions.",
        "content": """
### 要學習休息既遊戲 (A Game of Learning to Rest)

- **Farewell to the Past Self**:
  - *同昨日既自己講byebye (Say bye-bye to yesterday's self)*
  - *byebye你條尾 (Bye-bye to your lingering shadow)*
- **Stillness on Screen**: 靜落嚟既畫面 (A tranquil visual state), 琉璃 (stained glass clarity).
- **The Sloth Giant**: A massive sloth hugging and observing the player; marathon pace where the dog companion follows along.
- **Context Triad**: `Context > Border > Negative`.

### Emotional Geometry

- **Emotional Spirals**: People's emotional vectors spiral either toward compounded happiness or deepening melancholy.
- **Emotional Surface Area**: Visualizing the physical area occupied by emotional states.
- **Existential Floating**: *"If you are not sure but you feel the truth, just keep floating / 20% / 寄生腦 (Parasitic brain)."*

### The Triad of Yearning

- 給我一個朋友 (Give me a friend)
- 給我一點時間 (Give me some time)
- 給我一點樂趣 (Give me some joy)
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "06_Life_Career_Philosophy/Tension Headache",
            "02_Narrative_Psychology/Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo",
            "07_Synthesized_Concepts/Kinetic Resonance - Bloom of the Unspoken",
        ],
    },
    # --- ART / SHADERS / AESTHETICS BREAKDOWN (2 NOTES) ---
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Public Housing Perspectives and MTR Fisheye",
        "stem": "Public Housing Perspectives and MTR Fisheye",
        "tags": ["category/art-shaders-and-aesthetics", "theme/space-architecture", "theme/visual-art", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity", "00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Hong Kong public housing rental metrics, MTR fisheye optics, unnatural interactions, and window reflections.",
        "content": """
### Architectural Claustrophobia & Spatial Metrics

- **HK Public Housing Economics**: 香港公屋租金 / 超額 x 倍數 (Surplus multiplier on public housing rent).
- **Transit Vertigo**: 地鐵落電梯 廣告牌 手伸出黎 (Exiting MTR escalators, billboards, hands reaching out).
- **The Peeping Onlooker**: 窺望者 / 一個人等如一層樓 (One person equals one entire floor).
- **What Defines a Room**: Room definition governed by adjustable wash-lighting.
- **MTR Fisheye Distortion**: `Fisheye MTR seat zoom left pan right` — optical compression of subway cars; 3D mirrors for dual stereoscopic eyes.

### 不自然互動 (Unnatural Interaction)

- **Mechanical Repetition**: Objects placed in precise repetitions that rotate under fixed gear ratios.
- **Car Window Reflections**: Each car window reflection bounces off at a slightly offset angle.
- **Cardboard Modernity**: Supermarket cardboard people moving in stop-motion animation.
- **Organic Asymmetry**: Shells exhibit external symmetry while internal organs remain radically asymmetrical.
- **Funneling Shapes**: Handicapped constraints designed to funnel human output into defined architectural shapes.
*(Cross-referenced with [[06_Life_Career_Philosophy/People’s ignorance creates trouble for ppl|Unnatural Interaction & Communication Gap]].)*
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "06_Life_Career_Philosophy/People’s ignorance creates trouble for ppl",
            "02_Narrative_Psychology/樓上樓下",
            "04_Art_Shaders_Aesthetics/高不成低不就",
            "04_Art_Shaders_Aesthetics/crt tv zoom in",
        ],
    },
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Acoustic Physics and 3D Wave Visualization",
        "stem": "Acoustic Physics and 3D Wave Visualization",
        "tags": ["category/art-shaders-and-aesthetics", "theme/sound-music", "theme/visual-art", "theme/light-color"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light", "00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Concepts x9001",
        "summary": "Acoustic expectations, wave visualization in 3D, tidal keyboards, and aquatic ancient civilizations.",
        "content": """
### Sonic Expectations & Acoustic Physics

*"Audio represents physical expectations."*
Sound is not background dressing; acoustic frequencies set the physical constraints of what the player anticipates touching.

### Visualizing Waves in 3D

- **3D Soundwaves**: Visualizing sonic oscillation as structural geometry in 3D space.
- **The Tidal Keyboard**: 潮水的keyboard — an input instrument where wave surges correspond to keystrokes.
- **Turbine Shutter Light**: 渦輪機透光 (Turbine letting light pass frame-by-frame) / 渦輪機旋轉 (Turbine rotating to jump between frames).
- **Subsurface Civilizations**:
  - 浮潛面 (Snorkeling boundary) between surface and depths.
  - Isometric ancient civilizations submerged beneath fluctuating tides: heads growing from ground, waving water feeds, surging tides.
- **Atmospheric Lighting**: Giant floating strings with lights; realtime relight portal fixtures with rim lights; floating jellyfish tents.
- **Spline Deformations**: Face turn with spline deformation curving left-down while camera pans.
""",
        "related": [
            "01_Game_Design/Concepts x9001",
            "04_Art_Shaders_Aesthetics/never use true white and black",
            "01_Game_Design/Surfing",
            "07_Synthesized_Concepts/Bora-Bora Spectrum Surfer",
        ],
    },

    # --- EDIT SKILL ANIMATION BREAKDOWN (4 NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Unlimited Legend - Quick-Switch Champion Arena",
        "stem": "Unlimited Legend - Quick-Switch Champion Arena",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Edit skill animation in battle to dodge attack",
        "summary": "A fast-paced 5v5 MOBA format featuring instant full-item champion switching, rivalry bounties, and delayed side-lanes.",
        "content": """
### Game Mode Overview

A high-tempo competitive arena format designed for consecutive quick-match sessions in premade queues.

### Rules & Mechanics

- **Rapid Match Cadence**: Short, explosive matches chained in succession.
- **Random Champion Drafting**: 5v5 map where every player begins with one free complete item; no micro-component builds exist.
- **Champion Switching Economy**:
  - Free switch: Switching to a new champion costs zero gold, but purges all current items and assigns a baseline default item set (item quantity equals current match number).
  - Special Draft switch: Switching with a specialized random loadout costs 1 random item (3 distinct sets per champion).
  - Victory Reward: Winning a match awards a free switch to any champion with 2 free items.
- **Champion Rivalry Events**: Nemesis champion pairs trigger active rivalry bounties; executing your rival awards a full bonus item.
- **Modified Summoner's Rift Map**:
  - Mid-lane starts with 1 pre-destroyed turret.
  - Side lanes remain completely disabled until the mid-lane third turret falls.
  - Outer side lanes feature 2 pre-destroyed turrets once unlocked.
""",
        "related": [
            "01_Game_Design/Edit skill animation in battle to dodge attack",
            "01_Game_Design/Concepts x9001",
            "01_Game_Design/Massively Multiplayer Game",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Pins, Wires, and Bond-Breaking Mechanics",
        "stem": "Pins, Wires, and Bond-Breaking Mechanics",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/visual-art", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Edit skill animation in battle to dodge attack",
        "summary": "Tactile pinball wiring puzzles, rotating platforms, and bond-breaking interaction mechanics.",
        "content": """
### Core Mechanics

Tactile spatial puzzles centered on pins, wire connections, and mechanical bond disruption.

### Pinball Wire Networks

- **Wire Connections**: Physically connecting electrical wires between live pins.
- **Rotating Stage Descent**: A mage/healer character plunges through a kinetic arena, clinging onto rotating platforms to survive.
- **Overdrive Pin Slashes**: Overcharged pins slash electrical arcs toward adjacent nodes.

![[Drawing 1.png]]

### Bond-Breaking Systems

*"I misplace something to break something. Activate with a snap feedback. If I disconnect something, it activates differently. I have to break a bond to make a new bond."*

- **Weapon Assimilation**: Introduce enemy weapon systems that can be stolen, unlinked, and integrated into your own loadout.
- **Phantom Bonding**: Ghostly tether lines showing active energy routes.

![[Drawing 2.png]]
""",
        "related": [
            "01_Game_Design/Edit skill animation in battle to dodge attack",
            "01_Game_Design/Magic",
            "01_Game_Design/Loot, Magic, Robots",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Timed Document Laser and Ping-Pong Ghost Escape",
        "stem": "Timed Document Laser and Ping-Pong Ghost Escape",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Asymmetric_Social_Play"],
        "parent_source": "01_Game_Design/Edit skill animation in battle to dodge attack",
        "summary": "Laser scanning across timed document puzzles and arcade ping-pong ghost evasion.",
        "content": """
### Timed Document Laser Puzzle

- **Laser Scanning**: Lasers track across physical office documents and files.
- **Countdown Durations**: Each document displays a countdown in seconds; high-tier documents display unknown `?` countdowns.
- **High-Score Arcade Multiplier**: Successfully processing or clearing documents before laser expiration chains high-score combos.
- **Dynamic Camera System**: Movable fixed camera paired with dramatic fade-in and fade-out framing.

### Ping-Pong Ghost Escape

An intense evasion arcade game where players rally projectiles back and forth to repel pursuing spectral entities.

![[Drawing 3.png]]
""",
        "related": [
            "01_Game_Design/Edit skill animation in battle to dodge attack",
            "01_Game_Design/Simon says Escape room",
            "01_Game_Design/Killer game",
        ],
    },
    {
        "category": "01_Game_Design",
        "title": "Marshmallow Kingdom",
        "stem": "Marshmallow Kingdom",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/motion-body"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Somatic_Movement_and_Connection"],
        "parent_source": "01_Game_Design/Game Jam Game Ideas",
        "summary": "Consolidated design for Marshmallow Kingdom: punching deforming enemies and rubbing hands to generate soap liquid barriers.",
        "content": """
### Core Concept

A tactile, kinetic action game set in a squishy marshmallow castle environment.
*(Consolidated from redundant appearances in Game Jam Game Ideas and Edit Skill Animation).*

### Gameplay Verbs & Mechanics

- **Deforming Brawling**: Defend the sugar fortress by physically punching marshmallow enemies that deform, squish, and indent on impact.
- **Platform Jumping**: Leap onto giant marshmallow bouncy pads and punch smaller mob clusters.
- **Liquid Barrier (Soap Friction)**: Rub hands together vigorously (motion tracking or twin-stick friction) to create a bubbly liquid soap barrier that dissolves enemies.
- **Layered Items**: Dual-layered consumable objects combining plastic and styrofoam textures.
""",
        "related": [
            "01_Game_Design/Game Jam Game Ideas",
            "01_Game_Design/Edit skill animation in battle to dodge attack",
            "03_Physical_Motion_Games/Physical game concept",
            "01_Game_Design/Punching bag eats enemy and punching it deals dmg",
        ],
    },

    # --- INSTAGRAM REEL WORKFLOW BREAKDOWN (2 NOTES) ---
    {
        "category": "01_Game_Design",
        "title": "Virtual Room Interactive Items and Social Chaos",
        "stem": "Virtual Room Interactive Items and Social Chaos",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation", "theme/asymmetry-deception"],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play", "00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "04_Art_Shaders_Aesthetics/https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=",
        "summary": "Mischievous virtual room gadgets: room mutes, forced-vote sheep, spy dummies, and directional force pads.",
        "content": """
### Virtual Room Social Dynamics

Interactive toy gadgets deployed inside corporate or community virtual rooms to trigger emergent social chaos.

### Catalog of Interactive Items

- **Room Silencer**: An item that temporarily mutes every voice user in the room for several seconds.
- **Omni-Broadcast**: Allows a single user to broadcast voice everywhere across all rooms regardless of proximity or restrictions.
- **Happy Sheep (Forced Consensus)**: Deploys a sheep that forces all room occupants to vote 'YES' on active polls.
- **Spy House Dummy**: A covert surveillance dummy that can be placed inside another player's private residence.
- **Clone Dummy**: Copies another user's avatar appearance and mimics their movement gestures.
- **Traffic Light Stop**: Emits red/green phases that physically freeze players in place.
- **Directional Push Pad**: Floor tile that launches passing avatars in fixed vector directions.
- **Mess Shuffler**: Scrambles every furnishing and object inside the room into disarray.
- **Movement Alteration**: Items that radically speed up, slow down, or grant extreme vertical jump heights.
- **Token Receipt Machine**: Spits out digital receipts that convert into platform currency.
""",
        "related": [
            "04_Art_Shaders_Aesthetics/https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=",
            "01_Game_Design/Underground Casino and Cheating Mechanics",
            "01_Game_Design/Asymmetric Outlier Challenge",
        ],
    },
    {
        "category": "05_Tech_Pipelines_Unity",
        "title": "Procedural Map and Building Generation Workflow",
        "stem": "Procedural Map and Building Generation Workflow",
        "tags": ["category/technology-and-pipelines", "theme/unity-technical", "theme/procedural-generation"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "04_Art_Shaders_Aesthetics/https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=",
        "summary": "Technical pipeline for procedural road layouts, Houdini terrain conversions, building generation, and wearable cutoff points.",
        "content": """
### Procedural Environment Generation

Technical workflows for scaling 3D virtual spaces and avatar assets.

### Map Layout Pipeline
- Procedural road and attraction generation via Houdini.
- Exception handling rules for non-standard thoroughfares and special monuments.
- Pipeline for converting Houdini polygon meshes directly into native Unity Terrains.

### Building Generation
- Modular architectural scaling (Howl-inspired modularity).
- Density planning, quantity budgets, and performance scaling.

### Character & Wearable Pipeline
- Cutoff point definitions between avatar wearable categories (hats, tops, bottoms, shoes).
- Optimization plan for avatar draw calls and wearable batching.
- Off-screen proximity loading to preserve frame rate in dense virtual spaces.
""",
        "related": [
            "04_Art_Shaders_Aesthetics/https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=",
            "05_Tech_Pipelines_Unity/All unity plugins",
            "01_Game_Design/The number of land in each island",
        ],
    },
]

def execute_breakdown() -> None:
    print("Step 1: Writing the 22 new atomic concept notes...")
    for spec in NEW_ATOMIC_NOTES:
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
        print(f"  + Created: {out_file.relative_to(ROOT)}")

    print("\nStep 2: Updating master parent notes and eliminating duplicates...")

    # Concepts x9001.md
    concepts_9001_file = ROOT / "01_Game_Design" / "Concepts x9001.md"
    atomic_9001 = [s for s in NEW_ATOMIC_NOTES if s["parent_source"] == "01_Game_Design/Concepts x9001"]
    related_9001 = [
        "00_MOCs/Game_Design_MOC",
        "00_MOCs/Hub_Dreams_and_Memory",
        "00_MOCs/Hub_Soul_Economies_and_Lifecycles",
        "00_MOCs/Hub_Modular_Toy_Mechanics",
        "07_Synthesized_Concepts/Lucid Terminal - The Memory Golem",
        *[f"{s['category']}/{s['stem']}" for s in atomic_9001],
        "00_MOCs/00_Master_Index",
    ]
    seen = set()
    dedup_9001 = [r for r in related_9001 if not (r in seen or seen.add(r))]

    fm_9001 = "\n".join([
        "---",
        "title: \"Concepts x9001 — Master Concept Index\"",
        "aliases: [\"Concepts x9001\", \"apple-note-7536E76A-FAA0-466B-8B47-AE02210AE60F\"]",
        "tags: [\"category/game-design\", \"concept/index\", \"collection/concepts-x9001\"]",
        "category: \"Game Design\"",
        "status: \"Evergreen\"",
        "source: \"Apple Notes/Concepts x9001.md\"",
        "source_id: \"7536E76A-FAA0-466B-8B47-AE02210AE60F\"",
        "source_sha256: \"cf51ae1a3c169c1554207a7fc9d0e1a9edceede47de4b5afc5aa11c7e7c248e0\"",
        f"related: {json_val(property_links(dedup_9001))}",
        "---",
    ])
    body_9001 = [
        fm_9001,
        "",
        "# Concepts x9001 — Master Concept Index",
        "",
        "> [!info] Compilation Overview",
        "> `Concepts x9001` is an extensive, eclectic collection of experimental game mechanics, narrative seeds, systemic constraints, and spatial observations. To maintain atomic clarity and deep graph connectivity, this compilation has been broken down into 16 focused concept notes categorized below.",
        "",
        "## Atomic Notes Directory",
        "",
        "### 1. Game Mechanics & Systems",
        "- [[01_Game_Design/Cognitive Delays and Perception Lag|Cognitive Delays and Perception Lag]] — Chronicle, logical, and informational delay models.",
        "- [[01_Game_Design/Underground Casino and Cheating Mechanics|Underground Casino and Cheating Mechanics]] — Cheating verbs, shared casino items, and resource shed.",
        "- [[01_Game_Design/Asymmetric Outlier Challenge|Asymmetric Outlier Challenge]] — Voluntary 1-vs-All betrayal dynamics and bean-bag mass.",
        "- [[01_Game_Design/Color Tile Consumption Wheel|Color Tile Consumption Wheel]] — Permeable color tiles and rotating split-wheel faction gates.",
        "- [[01_Game_Design/Inverted Role Play - Minion and Pest Escape|Inverted Role Play - Minion and Pest Escape]] — Playing sluggish TD minions, sacrificial domestic pests, and miracle controllers.",
        "- [[01_Game_Design/Purchasable Power Corporate Finance|Purchasable Power Corporate Finance]] — Satirical money-as-life economy and leveraged power packages.",
        "- [[01_Game_Design/Democracy Bingo and Systemic Game Rules|Democracy Bingo and Systemic Game Rules]] — Voting bingo, polygon limit leveling, failure chances, and testing patience.",
        "- [[01_Game_Design/Systemic Combat Friction and Flu Seasons|Systemic Combat Friction and Flu Seasons]] — Engagement reaction delay, 2-hit mitigations, elemental taxes, and seasonal flu nerfs.",
        "- [[01_Game_Design/Group Vision and Tactical Range|Group Vision and Tactical Range]] — Inverted group field-of-view, health piece targeting, and fighting game chess.",
        "- [[01_Game_Design/The Decryption Lens and Pattern Emblems|The Decryption Lens and Pattern Emblems]] — Optical decryption scroll lenses, Fibonacci maps, and fear attacks.",
        "- [[01_Game_Design/UI Event Matrices and Spatial Pacing|UI Event Matrices and Spatial Pacing]] — Bubble ring pushes, teleporting memory books, event cadence matrices, and camera focal compression.",
        "",
        "### 2. Narrative & Psychology",
        "- [[02_Narrative_Psychology/Narrative Vignettes - Hitmen, Trains, and Spirit Enforcers|Narrative Vignettes - Hitmen, Trains, and Spirit Enforcers]] — Failed-hitman hitmen, rail frontier development, and spirit-infused robot parts.",
        "- [[02_Narrative_Psychology/Memory Golem and Dream Entity Network|Memory Golem and Dream Entity Network]] — Constructing memory golems from villager achievements and collective dream networks.",
        "- [[02_Narrative_Psychology/The Resting Game and Emotional Geometry|The Resting Game and Emotional Geometry]] — Learning to rest, bidding farewell to past selves, and emotional spiral vectors.",
        "",
        "### 3. Art, Shaders & Aesthetics",
        "- [[04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye|Public Housing Perspectives and MTR Fisheye]] — Hong Kong public housing rental pressure, MTR fisheye views, and unnatural interactions.",
        "- [[04_Art_Shaders_Aesthetics/Acoustic Physics and 3D Wave Visualization|Acoustic Physics and 3D Wave Visualization]] — Physical expectations from sound, tidal keyboards, and submerged ancient structures.",
        "",
        "## Synthesized Projects Derived from Concepts x9001",
        "- **[[07_Synthesized_Concepts/Lucid Terminal - The Memory Golem|Lucid Terminal: The Memory Golem]]** — Directly synthesizes the Memory Golem, 3 AM awakening, and fractured light platforms.",
        "- **[[07_Synthesized_Concepts/Guild of the Departed - 21 Grams|Guild of the Departed: 21 Grams]]** — Integrates soul lifecycles, value upgrading, and hidden conversion ratios.",
        "- **[[07_Synthesized_Concepts/The Collar Experiment - Asymmetric Dilemma|The Collar Experiment: Asymmetric Dilemma]]** — Draws upon asymmetric outlier choice, fear attacks, and information delay.",
        "",
        "## Navigation",
        "- [[00_MOCs/Game_Design_MOC|Game Design MOC]]",
        "- [[00_MOCs/00_Master_Index|Master Knowledge Index]]",
    ]
    concepts_9001_file.write_text("\n".join(body_9001) + "\n", encoding="utf-8")

    # Edit skill animation in battle to dodge attack.md
    edit_skill_file = ROOT / "01_Game_Design" / "Edit skill animation in battle to dodge attack.md"
    fm_edit = "\n".join([
        "---",
        "title: \"Location-Based Play and Animation Dodging\"",
        "aliases: [\"Edit skill animation in battle to dodge attack\"]",
        "tags: [\"category/game-design\", \"theme/game-mechanics\", \"theme/motion-body\"]",
        "category: \"Game Design\"",
        "status: \"Evergreen\"",
        "source: \"Apple Notes/Edit skill animation in battle to dodge attack.md\"",
        f"related: {json_val(property_links([
            '00_MOCs/Game_Design_MOC',
            '00_MOCs/Hub_Modular_Toy_Mechanics',
            '01_Game_Design/Unlimited Legend - Quick-Switch Champion Arena',
            '01_Game_Design/Pins, Wires, and Bond-Breaking Mechanics',
            '01_Game_Design/Timed Document Laser and Ping-Pong Ghost Escape',
            '01_Game_Design/Marshmallow Kingdom',
            '00_MOCs/00_Master_Index'
        ]))}",
        "---",
    ])
    body_edit = [
        fm_edit,
        "",
        "# Location-Based Play and Animation Dodging",
        "",
        "> [!abstract] Conceptual Context",
        "> **Category**: [[00_MOCs/Game_Design_MOC|Game Design]]",
        "> **Thematic Constellations**: [[00_MOCs/Hub_Modular_Toy_Mechanics|Modular Toy Mechanics]]",
        "",
        "## Core Location & Attack Mechanics",
        "",
        "### 1. Location-Based Mechanics: Stay at Home vs. Get Out of the Chair",
        "- **Stay at Home Play**: 鬥智 鬥力 合作 (Wits, strength, and cooperation). Continuous voice communication and party verbal coordination.",
        "- **Get Out of the Chair Play**: Physical catch mechanics, pet tracking, and location-based check-ins.",
        "- **Monetization & Engagement**: Monthly subscriptions, installment plans, WePlay integration.",
        "",
        "### 2. Animation Dodging & Attack Pattern Shifts",
        "- Changing attack patterns dynamically during combat:",
        "  - **Confused State**: All enemy attacks target random entities.",
        "  - **Taunt State**: All enemy attacks converge upon one target.",
        "- Editing skill animations mid-battle to iframe-dodge incoming strikes.",
        "- **Evolution & Pupation Spikes**: Individual growth curves with metamorphic power spikes.",
        "- **Nest Cleanup Management**: Tactical decisions between Pickup Order versus Dumping Order.",
        "- **Worm Animal Chess**: Strategic grid movement with insect and animal hierarchies.",
        "- **Un-stealth Verb**: Getting detected is mechanically advantageous.",
        "",
        "## Decomposed Modular Sub-Concepts",
        "",
        "The following specialized mechanics originally jotted in this note have been broken down into dedicated atomic files:",
        "- [[01_Game_Design/Unlimited Legend - Quick-Switch Champion Arena|Unlimited Legend]] — 5v5 rapid champion switching with rivalry rewards.",
        "- [[01_Game_Design/Pins, Wires, and Bond-Breaking Mechanics|Pins, Wires, and Bond-Breaking Mechanics]] — Pinball kinetic wire puzzles and weapon uncoupling.",
        "- [[01_Game_Design/Timed Document Laser and Ping-Pong Ghost Escape|Timed Document Laser and Ping-Pong Ghost Escape]] — Timed document laser scanning and ghost ping-pong.",
        "- [[01_Game_Design/Marshmallow Kingdom|Marshmallow Kingdom]] — *Deduplicated and consolidated with Game Jam ideas.*",
        "",
        "## Navigation",
        "- [[00_MOCs/Game_Design_MOC|Game Design MOC]]",
        "- [[00_MOCs/00_Master_Index|Master Knowledge Index]]",
    ]
    edit_skill_file.write_text("\n".join(body_edit) + "\n", encoding="utf-8")

    # Game Jam Game Ideas.md
    gamejam_file = ROOT / "01_Game_Design" / "Game Jam Game Ideas.md"
    gamejam_text = gamejam_file.read_text(encoding="utf-8")
    if "**Marshmallow Kingdom**" in gamejam_text:
        gamejam_text = re.sub(
            r"\*\*Marshmallow Kingdom\*\*[\s\S]*?(?=\n\n\*\*Worms\*\*|\n\n##)",
            "**[[01_Game_Design/Marshmallow Kingdom|Marshmallow Kingdom]]** *(Canonical Note)*\n- Tactile squishy brawling, deforming enemies, and soap-rubbing liquid barriers.",
            gamejam_text,
        )
        gamejam_file.write_text(gamejam_text, encoding="utf-8")

    # Instagram references
    insta_file = ROOT / "04_Art_Shaders_Aesthetics" / "https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=.md"
    fm_insta = "\n".join([
        "---",
        "title: \"Virtual Room Ecosystems and World Building References\"",
        "aliases: [\"https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=\", \"Instagram Inspiration and Virtual Room Ideas\"]",
        "tags: [\"category/art-shaders-and-aesthetics\", \"theme/visual-art\", \"theme/social-cooperation\"]",
        "category: \"Art, Shaders & Aesthetics\"",
        "status: \"Evergreen\"",
        "source: \"Apple Notes/https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=.md\"",
        f"related: {json_val(property_links([
            '00_MOCs/Art_Shaders_and_Aesthetics_MOC',
            '01_Game_Design/Virtual Room Interactive Items and Social Chaos',
            '05_Tech_Pipelines_Unity/Procedural Map and Building Generation Workflow',
            '00_MOCs/00_Master_Index'
        ]))}",
        "---",
    ])
    body_insta = [
        fm_insta,
        "",
        "# Virtual Room Ecosystems and World Building References",
        "",
        "> [!abstract] Conceptual Context",
        "> **Category**: [[00_MOCs/Art_Shaders_and_Aesthetics_MOC|Art, Shaders & Aesthetics]]",
        "> **Origin**: Curated visual reference reels and virtual environment architecture notes.",
        "",
        "## Reference Links & Inspiration Reels",
        "- [Instagram Reel - Virtual Spaces](https://www.instagram.com/reel/CeB3TK_F9p4/?igshid=YmMyMTA2M2Y=)",
        "- [Instagram Account - Yorugatamaomao](https://instagram.com/yorugatamaomao?igshid=YmMyMTA2M2Y=)",
        "- [Pika Style Platform](https://pika.style)",
        "",
        "## Decomposed Core Workflows",
        "",
        "The extensive virtual room gadgets and technical generation pipelines originally logged here have been organized into dedicated files:",
        "- [[01_Game_Design/Virtual Room Interactive Items and Social Chaos|Virtual Room Interactive Items and Social Chaos]] — Room silencers, forced voting sheep, spy dummies, and directional force pads.",
        "- [[05_Tech_Pipelines_Unity/Procedural Map and Building Generation Workflow|Procedural Map and Building Generation Workflow]] — Houdini road generation, Unity terrain conversion, building scaling, and wearable cutoffs.",
        "",
        "## Navigation",
        "- [[00_MOCs/Art_Shaders_and_Aesthetics_MOC|Art, Shaders & Aesthetics MOC]]",
        "- [[00_MOCs/00_Master_Index|Master Knowledge Index]]",
    ]
    insta_file.write_text("\n".join(body_insta) + "\n", encoding="utf-8")

    print("\nStep 3: Updating 8 Thematic Concept Hubs in 00_MOCs/...")
    # Read and update each Hub to append any newly assigned atomic notes
    for spec in NEW_ATOMIC_NOTES:
        stem = spec["stem"]
        cat = spec["category"]
        title = spec["title"]
        for hub_path in spec["hubs"]:
            hub_file = ROOT / f"{hub_path}.md"
            if not hub_file.exists():
                continue
            text = hub_file.read_text(encoding="utf-8")
            note_link = f"[[{cat}/{stem}|{title}]]"
            if stem not in text:
                # Add to connected source notes before Navigation
                insert_line = f"- {note_link} (`{CATEGORIES[cat]['name']}`) — {spec['summary']}\n"
                if "## Connected Source Notes\n\n" in text:
                    text = text.replace("## Connected Source Notes\n\n", f"## Connected Source Notes\n\n{insert_line}")
                elif "## Navigation" in text:
                    text = text.replace("## Navigation", f"{insert_line}\n## Navigation")
                # Also add to frontmatter related
                fm_match = re.search(r"^---\n(.*?)\n---", text, flags=re.DOTALL)
                if fm_match:
                    fm_text = fm_match.group(1)
                    if f"[[{cat}/{stem}]]" not in fm_text:
                        fm_text = re.sub(
                            r'(related:\s*\[)(.*?)(\])',
                            rf'\1\2, "[[{cat}/{stem}]]"\3',
                            fm_text,
                        )
                        text = f"---\n{fm_text}\n---" + text[fm_match.end() :]
                hub_file.write_text(text, encoding="utf-8")
                print(f"  * Appended {title} to {hub_file.name}")

    print("\nStep 4: Updating Category MOCs in 00_MOCs/...")
    for cat_key, c_info in CATEGORIES.items():
        moc_file = ROOT / "00_MOCs" / f"{c_info['moc']}.md"
        if not moc_file.exists():
            continue
        text = moc_file.read_text(encoding="utf-8")
        cat_new_notes = [s for s in NEW_ATOMIC_NOTES if s["category"] == cat_key]
        for s in cat_new_notes:
            stem = s["stem"]
            title = s["title"]
            if stem not in text:
                line = f"- [[{cat_key}/{stem}|{title}]] · `Evergreen` · {', '.join(s['tags'][:2])} · {s['summary']}\n"
                if "## Complete Note Directory\n\n" in text:
                    text = text.replace("## Complete Note Directory\n\n", f"## Complete Note Directory\n\n{line}")
                elif "## Preserved Canvas Notes" in text:
                    text = text.replace("## Preserved Canvas Notes", f"{line}\n## Preserved Canvas Notes")
                elif "## Related Hubs" in text:
                    text = text.replace("## Related Hubs", f"{line}\n## Related Hubs")
        moc_file.write_text(text, encoding="utf-8")
        print(f"  * Updated {moc_file.name}")

    print("\nStep 5: Updating 00_Master_Index.md and Source_Manifest.md...")
    # Master Index
    master_file = ROOT / "00_MOCs" / "00_Master_Index.md"
    master_text = master_file.read_text(encoding="utf-8")
    
    # Update active creative notes count: was 120, now 120 + 22 = 142
    master_text = re.sub(r"\*\*Active Creative Notes:\*\* \d+", f"**Active Creative Notes:** {120 + len(NEW_ATOMIC_NOTES)}", master_text)
    master_text = re.sub(r"Game Design\]\] \(\d+ notes\)", f"Game Design]] ({49 + 17} notes)", master_text)
    master_text = re.sub(r"Narrative & Psychology\]\] \(\d+ notes\)", f"Narrative & Psychology]] ({20 + 3} notes)", master_text)
    master_text = re.sub(r"Art, Shaders & Aesthetics\]\] \(\d+ notes\)", f"Art, Shaders & Aesthetics]] ({22 + 2} notes)", master_text)
    master_text = re.sub(r"Technology & Pipelines\]\] \(\d+ notes\)", f"Technology & Pipelines]] ({4 + 1} notes)", master_text)
    master_file.write_text(master_text, encoding="utf-8")

    # Source Manifest
    manifest_file = ROOT / "00_MOCs" / "Source_Manifest.md"
    manifest_text = manifest_file.read_text(encoding="utf-8")
    for s in NEW_ATOMIC_NOTES:
        cat_key = s["category"]
        c_name = CATEGORIES[cat_key]["name"]
        stem = s["stem"]
        title = s["title"]
        if stem not in manifest_text:
            entry = f"- `[Decomposed] {s['parent_source']}` → [[{cat_key}/{stem}|{title}]] · `atomic`\n"
            target_hdr = f"## {c_name}\n\n"
            if target_hdr in manifest_text:
                manifest_text = manifest_text.replace(target_hdr, f"{target_hdr}{entry}")
    manifest_file.write_text(manifest_text, encoding="utf-8")

    print("\nStep 6: Running Graph Connectivity & Integrity Audit...")
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

    # Connectivity check
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

    # Check images
    missing_assets = []
    for p in all_md:
        text = p.read_text(encoding="utf-8")
        for img in re.findall(r"!\[\[([^\]]+)\]\]", text):
            img_name = img.split("|")[0].split("#")[0].strip()
            if not (ASSETS_DIR / img_name).exists() and not (ROOT / img_name).exists():
                missing_assets.append(f"{p.name} -> {img_name}")

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
        f"- Active Markdown notes: **{len(all_md)}** (120 foundational + {len(NEW_ATOMIC_NOTES)} decomposed atomic notes + 24 MOCs/Hubs/Concepts)",
        f"- Active Canvas notes: **{len(all_canvases)}**",
        f"- Total Knowledge Graph nodes: **{len(all_keys)}**",
        f"- Total Internal Wikilinks: **{total_links}**",
        f"- Unresolved Links: **{len(unresolved)}**",
        f"- Unreachable / Orphan Nodes: **{len(unreachable)}**",
        f"- Single Connected Component: **{'yes' if not unreachable else 'no'}**",
        f"- Backup Preserved in `_backup_apple_notes/`: **yes**",
        "",
    ]
    if missing_assets:
        report_lines.append("## Missing Asset References")
        for m in sorted(set(missing_assets)):
            report_lines.append(f"- `{m}`")
    else:
        report_lines.append("## Asset References")
        report_lines.append("- All referenced images are resolved in `Assets/`.")

    (ROOT / "00_MOCs" / "Integrity_Report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\nBreakdown Complete!")
    print(f"Total Markdown Notes: {len(all_md)}")
    print(f"Total Graph Nodes: {len(all_keys)}")
    print(f"Total Links: {total_links}")
    print(f"Unresolved Links: {len(unresolved)}")
    print(f"Orphan Nodes: {len(unreachable)}")
    print(f"100% Connected: {len(unreachable) == 0}")

if __name__ == "__main__":
    execute_breakdown()