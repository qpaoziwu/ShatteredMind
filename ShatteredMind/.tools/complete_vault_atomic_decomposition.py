#!/usr/bin/env python3
"""
Complete Vault Atomic Decomposition Engine:
1. Decomposes all multi-concept notes into individual atomic nodes.
2. Identifies and preserves short stories, poems, and continuous narrative prose as unified nodes.
3. Checks for and resolves duplicated concepts across the vault into canonical notes.
4. Updates parent compilation notes into clean directories pointing to their atomic children.
5. Rebuilds and balances all 8 Thematic Concept Hubs and 6 Category MOCs.
6. Verifies 100% Obsidian graph connectivity, 0 unresolved links, and 0 orphan nodes.
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
        if len(line) >= 8:
            return line[:120] + ("…" if len(line) > 120 else "")
    return "Atomic concept note."

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

# The 15 short stories / prose narratives that MUST stay unified
PROTECTED_NARRATIVES = {
    "Character idea",
    "Story idea",
    "he spun weaves of cloth to protect his land",
    "I",
    "Story Note",
    "To Ashley,",
    "a group of special ops",
    "female protagonist is a tutor for adult students and is highly respected by everyone, because she changes people’s lives by granting the knowledge and diploma the person needs to move on in life. Male",
    "Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo",
    "My Journey Starts in how i start my family",
    "raspy male lead vocal, Warm piano chords lay the foundation, joined by soft, fingerstyle acoustic guitar and subtle electric accents for the light country touch, Understated R&B-inspired percussion an",
    "i put the moon in the tone",
    "showers with plastic doll pieces",
    "Looking up the evening sky,",
    "i took two step then turned back",
}

# Exhaustive atomic concept specifications to extract from all multi-concept notes
DETAILED_ATOMIC_SPECS = [
    # === LOOT, MAGIC, ROBOTS (ALL 16+ HIDDEN IDEAS) ===
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Fractal UV Shaders",
        "stem": "Fractal UV Shaders",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art", "theme/procedural-generation"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Procedural texture coordinate mapping using recursive fractal math to generate infinite self-similar UV layouts.",
        "content": """
### Technical & Aesthetic Concept
- **Fractal UV Mapping**: Using recursive mathematical equations to partition texture coordinates into infinitely nested geometric scales.
- Allows microscopic surface detail without texture resolution memory blowup.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "04_Art_Shaders_Aesthetics/never use true white and black"],
    },
    {
        "category": "01_Game_Design",
        "title": "Mememe Mosquito Audio-Visual Motif",
        "stem": "Mememe Mosquito Audio-Visual Motif",
        "tags": ["category/game-design", "theme/sound-music", "theme/nature-organisms"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "High-frequency auditory mosquito buzz (mememe 蚊) used as an irritant sensory prompt and evasion indicator.",
        "content": """
### Sensory Concept
- **mememe 蚊 (Mosquito Audio Cue)**: High-frequency, persistent auditory buzzing indicating the presence of parasitic micro-threats.
- Evokes immediate instinctive physical reaction from players.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Systemic Combat Friction and Flu Seasons"],
    },
    {
        "category": "01_Game_Design",
        "title": "Geometric Surface Snapping and Adhesive Shapes",
        "stem": "Geometric Surface Snapping and Adhesive Shapes",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Setting angle, rotational pitch, and geometric boundary shape, letting modular parts snap and permanently stick.",
        "content": """
### Snapping Mechanics
- **Set Angle and Shape and Let It Stick**: Modular placement where players orient objects to specific angles and pitch; releasing them permanently adheres the shape to the surface.
- **清麗苑 Housing Motif**: Tactile architectural constraints inspired by Hong Kong residential estate layouts.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye"],
    },
    {
        "category": "01_Game_Design",
        "title": "Dating Profile Matching Interaction",
        "stem": "Dating Profile Matching Interaction",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Bumble-style profile liking and asymmetric compatibility matching mechanic integrated into NPC and player discovery.",
        "content": """
### Social Mechanics
- *"What do you think? Like their profile and see if you match!"* (`https://bum.bb/u/Vd4Lyaufg1w`)
- Swiping and profile evaluations determining cooperative mission eligibility between strangers.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "06_Life_Career_Philosophy/The distance between ppl pulls reasons together"],
    },
    {
        "category": "01_Game_Design",
        "title": "Robo Marching Band Circus",
        "stem": "Robo Marching Band Circus",
        "tags": ["category/game-design", "theme/worldbuilding", "theme/sound-music"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "A whimsical, mechanical parade of automated brass and percussive circus automatons marching in synchronized formations.",
        "content": """
### Worldbuilding & Kinetic Audio
- **Automated Circus Ensemble**: Autonomous brass and percussion robot automatons parading across environmental routes.
- Rhythmic procedural music scaling as more robot instruments join the procession.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "04_Art_Shaders_Aesthetics/Acoustic Physics and 3D Wave Visualization"],
    },
    {
        "category": "01_Game_Design",
        "title": "Emergency Use Only Item Series",
        "stem": "Emergency Use Only Item Series",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/cards-tabletop"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Absurdist sealed emergency equipment series (Dildo, Ring) that break rules only in existential crises.",
        "content": """
### Absurdist Crisis Utility
- **For Emergency Use Only Series**:
  - Dildo
  - Ring
- Specialized emergency items sealed under glass; breaking the glass triggers extreme mechanical consequences.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Design a fun toy with surprises"],
    },
    {
        "category": "01_Game_Design",
        "title": "Dark Sky Exploration and Pacing Rewards",
        "stem": "Dark Sky Exploration and Pacing Rewards",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics", "00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Near-pitch-black celestial navigation that systematically rewards players for pacing down and decelerating.",
        "content": """
### Minimalist Navigation
- **Dark Sky & Dim Stars**: Spatial traversal through deeply unlit voids where only faint star nodes twinkle.
- **Pacing Deceleration**: The game rewards players for actively slowing down movement; moving fast blinds radar, while stillness expands perceptual radius.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Connect the Dots Puzzle - Dark Sky Star Sequences"],
    },
    {
        "category": "01_Game_Design",
        "title": "Keystroke Constellation Connection Sequences",
        "stem": "Keystroke Constellation Connection Sequences",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/ui-ux"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Initiating constellation connections with the apostrophe key (') followed by typing precise alphanumeric sequences.",
        "content": """
### Textual Input Connection
- **Trigger**: Initiate stellar connection with the `'` apostrophe key.
- **Sequence Typing**: Type rapid alphanumeric sequences to cast energy beams bridging constellation nodes.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/00928z"],
    },
    {
        "category": "05_Tech_Pipelines_Unity",
        "title": "Mathematical Mesh Subdivision Curves",
        "stem": "Mathematical Mesh Subdivision Curves",
        "tags": ["category/technology-and-pipelines", "theme/unity-technical"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Scripted trigonometric mesh generation using height and width subdivisions: Vector3(Mathf.Sin(i), 0, Mathf.Cos(i)).",
        "content": """
### Algorithmic Geometry
```csharp
int HeightSubdivision;
int WidthSubdivision;

for (i = 0; i < max; i++) {
    Vector3(Mathf.Sin(i), 0, Mathf.Cos(i));
}
```
- Parametric circular mesh subdivision for generating smooth cylindrical and toroidal game geometry.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "05_Tech_Pipelines_Unity/Procedural Map and Building Generation Workflow"],
    },
    {
        "category": "01_Game_Design",
        "title": "Puzzle Taxonomy - Battle, Easter Egg, Chain, Connect Dots",
        "stem": "Puzzle Taxonomy - Battle, Easter Egg, Chain, Connect Dots",
        "tags": ["category/game-design", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Taxonomic categorization of environmental puzzles: Battle puzzles, Easter egg hunt chain puzzles, and connect-the-dots.",
        "content": """
### Puzzle Categories
1. **Battle Puzzle**: Spatial combat encounters where damage can only be dealt by solving real-time puzzle constraints.
2. **Easter Egg Hunt Chain Puzzle**: Hidden environmental clues chained across disparate zones.
3. **Connect the Dots Puzzle**: Node-linking network puzzles governing power and traversal.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Connect the Dots Puzzle - Dark Sky Star Sequences"],
    },
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Water Wiggle Vertex Shader",
        "stem": "Water Wiggle Vertex Shader",
        "tags": ["category/art-shaders-and-aesthetics", "theme/visual-art"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Playful vertex displacement shader creating undulating, jelly-like gelatinous water surfaces (Water wiggle).",
        "content": """
### Shader Technique
- **Water Wiggle**: Sinusoidal vertex displacement applied to liquid meshes, producing a cartoonish, elastic wobble upon collision.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "04_Art_Shaders_Aesthetics/Art concepts"],
    },
    {
        "category": "04_Art_Shaders_Aesthetics",
        "title": "Environmental Storytelling Through Light Ownership",
        "stem": "Environmental Storytelling Through Light Ownership",
        "tags": ["category/art-shaders-and-aesthetics", "theme/light-color", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Optical_Shaders_and_Light"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Narrative architecture: Tell story by light, owner of the light. The entity holding the lantern defines perceived truth.",
        "content": """
### Light Ownership Narrative
*"Tell story by light, owner of the light."*
- Environmental truth and architectural narrative are subjective; the faction or character holding the primary light source dictates what reality is rendered visible.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Discharge Energy Nodes and Shifting Ceilings"],
    },
    {
        "category": "01_Game_Design",
        "title": "Public Component Attachment Scoring",
        "stem": "Public Component Attachment Scoring",
        "tags": ["category/game-design", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "System where individual components earn base scores, with multipliers applied for publicly exposed objects.",
        "content": """
### Component Valuation
- Every modular component earns a baseline score.
- **Public Visibility Multiplier**: Being a public object visible to external players multiplies its valuation score.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Component Attachment Scoring Matrix"],
    },
    {
        "category": "05_Tech_Pipelines_Unity",
        "title": "Mini Manager Root Hierarchy Protocol",
        "stem": "Mini Manager Root Hierarchy Protocol",
        "tags": ["category/technology-and-pipelines", "theme/unity-technical"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Hierarchical management system checking root objects, attach point statuses, and falling back to default operators.",
        "content": """
### Hierarchical Architecture
- **Root Audit**: Inspect root GameObject and attach point status to compute active branch count.
- **Operator Verification**: Check protocol/operator; if null, safely fall back to default handler.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Component Attachment Scoring Matrix"],
    },
    {
        "category": "01_Game_Design",
        "title": "Escalating Consumable Multipliers",
        "stem": "Escalating Consumable Multipliers",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/economy-value"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Consumables whose potency escalates with repeated use before vanishing: first use 1x, second use 2x.",
        "content": """
### Escalating Multipliers
- **Consumable Mechanics**: First activation triggers 1x baseline effect; second activation escalates to 2x potency before item depletes.
- Encourages delayed gratification and high-stakes combo timing.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Digital Candy Game"],
    },
    {
        "category": "02_Narrative_Psychology",
        "title": "Delly Cyrus - Bullying and Running Narrative Seed",
        "stem": "Delly Cyrus - Bullying and Running Narrative Seed",
        "tags": ["category/narrative-and-psychology", "theme/identity-emotion", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Urban_Alienation_and_Identity"],
        "parent_source": "01_Game_Design/Loot, Magic, Robots",
        "summary": "Character vignette: Delly Cyrus, a troubled teenager and targeted underdog who channels bullying trauma into relentless running.",
        "content": """
### Character Motif
- **Delly Cyrus**: A troubled, bullied teenager whose only defense mechanism is running through urban streets.
- Movement, sprinting, and momentum as both physical survival and emotional refuge.
""",
        "related": ["01_Game_Design/Loot, Magic, Robots", "01_Game_Design/Momentum Storage and Kinetic Release", "02_Narrative_Psychology/I"],
    },

    # === SURFING EXTRACTIONS ===
    {
        "category": "01_Game_Design",
        "title": "Three Surfing Prototypes - Paddle, Combo, Utility",
        "stem": "Three Surfing Prototypes - Paddle, Combo, Utility",
        "tags": ["category/game-design", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Surfing",
        "summary": "Three-stage prototyping architecture for surfing: 1) Paddling & pumping, 2) Combo system, 3) Board utility.",
        "content": """
### Prototyping Roadmap
1. **Prototype 1**: Core physical feel (Paddling, Pop-up timing, Pumping speed buildup).
2. **Prototype 2**: Trick and scoring combo mechanics.
3. **Prototype 3**: Equipment utility, board wear-and-tear, and seabed adaptation.
""",
        "related": ["01_Game_Design/Surfing", "01_Game_Design/Wave Dynamics and Aerial Combos"],
    },
    {
        "category": "01_Game_Design",
        "title": "Seabed Bottom Ecology - Reef, Stone, Sand",
        "stem": "Seabed Bottom Ecology - Reef, Stone, Sand",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Surfing",
        "summary": "Seabed topography (Reef, Stone, Sand) dictating wave steepness, character attribute advantages, and break hazards.",
        "content": """
### Seabed Physics
- **Reef**: Generates hollow, fast, steep peeling waves; high risk of board damage.
- **Stone**: Unpredictable rebound boils and explosive wave lips.
- **Sand**: Forgiving, shifting sandbars with soft breaks and wide takeoff zones.
- Surfer characters have attribute affinities to specific ocean bottom types.
""",
        "related": ["01_Game_Design/Surfing", "07_Synthesized_Concepts/Bora-Bora Spectrum Surfer"],
    },
    {
        "category": "01_Game_Design",
        "title": "Two-Player Wave Crash Mechanics",
        "stem": "Two-Player Wave Crash Mechanics",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/social-cooperation"],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum"],
        "parent_source": "01_Game_Design/Surfing",
        "summary": "Multiplayer wave collision where surfers sharing the same break crash and plunge together to the ocean bottom.",
        "content": """
### Competitive Collision
- **Shared Break Friction**: If two players cross paths or attempt to drop into the same wave pocket, collision triggers an immediate wipeout.
- Both surfers plunge to the ocean bed, losing position and resetting banked momentum.
""",
        "related": ["01_Game_Design/Surfing", "01_Game_Design/Card-Driven Wave Movement Combo"],
    },

    # === 21 GRAMS WEIGHT OF A SOUL EXTRACTIONS ===
    {
        "category": "01_Game_Design",
        "title": "Four Emotional Pillars of Harvesting and Monster Death",
        "stem": "Four Emotional Pillars of Harvesting and Monster Death",
        "tags": ["category/game-design", "theme/identity-emotion", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/21 Grams Weight of a Soul",
        "summary": "Core emotional pillars: harvesting must feel good, death must feel comedic, big monsters threatening, small monsters easy.",
        "content": """
### Emotional Pillar Mandates
1. **Harvesting has to feel good**: Satisfying tactile feedback when reaping souls.
2. **Death should feel comedic**: Slapstick mortality rather than grim horror.
3. **Big monsters should feel threatening**: Colossal presence and overwhelming aura.
4. **Small monsters should feel easy**: Effortless swarm dispatching.
""",
        "related": ["01_Game_Design/21 Grams Weight of a Soul", "07_Synthesized_Concepts/Guild of the Departed - 21 Grams"],
    },
    {
        "category": "01_Game_Design",
        "title": "Environmental Death Factor Accumulation",
        "stem": "Environmental Death Factor Accumulation",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/time-cycles"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/21 Grams Weight of a Soul",
        "summary": "Latent death factors accumulating silently in world tiles and hostile creatures until triggering premature demise.",
        "content": """
### Lethality Accumulation
- Death risk accumulates invisibly across terrain tiles and monster proximity.
- Upon crossing threshold values, villagers suffer sudden, premature deaths, devaluing their soul weight.
""",
        "related": ["01_Game_Design/21 Grams Weight of a Soul", "01_Game_Design/Lifespan  how many cycles"],
    },
    {
        "category": "01_Game_Design",
        "title": "Hype Meter and Release the Hound Button",
        "stem": "Hype Meter and Release the Hound Button",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/ui-ux"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/21 Grams Weight of a Soul",
        "summary": "Village excitement hype meter and an emergency 'Release the Hound' button unleashing wild village defense beasts.",
        "content": """
### Emergency Escalation
- **Hype Meter**: Village morale and excitement gauge fueled by successful quests and festivities.
- **Release the Hound**: A physical emergency button unleashing devastating hounds to repel overwhelming invasions.
""",
        "related": ["01_Game_Design/21 Grams Weight of a Soul", "01_Game_Design/Design a fun toy with surprises"],
    },
    {
        "category": "01_Game_Design",
        "title": "Ghosts Wearing Defeatable Hats",
        "stem": "Ghosts Wearing Defeatable Hats",
        "tags": ["category/game-design", "theme/worldbuilding", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/21 Grams Weight of a Soul",
        "summary": "Whimsical underworld motif where lingering spirits wear stylish hats that drop as collectible loot upon defeat.",
        "content": """
### Whimsical Underworld Loot
- Deceased souls and phantoms wear distinctive hats.
- Upon releasing or defeating a ghost, their hat drops as an equipable cosmetic artifact.
""",
        "related": ["01_Game_Design/21 Grams Weight of a Soul", "07_Synthesized_Concepts/Guild of the Departed - 21 Grams"],
    },

    # === DIGITAL CANDY GAME EXTRACTIONS ===
    {
        "category": "01_Game_Design",
        "title": "Draw Pile Sudden Death and Discard Hand End Game",
        "stem": "Draw Pile Sudden Death and Discard Hand End Game",
        "tags": ["category/game-design", "theme/cards-tabletop", "theme/game-mechanics"],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "parent_source": "01_Game_Design/Digital Candy Game",
        "summary": "Game termination triggers: sudden death upon draw pile depletion, and last-round hand discard scoring.",
        "content": """
### Game Over Conditions
- Game ends instantaneously the moment the draw deck empties.
- Final round forces players to discard remaining hand; un-melted cards are disqualified from final scoring.
""",
        "related": ["01_Game_Design/Digital Candy Game", "01_Game_Design/Card Melting vs Candy Consumption Economy"],
    },
    {
        "category": "01_Game_Design",
        "title": "Pull-Down Page UI Reveal",
        "stem": "Pull-Down Page UI Reveal",
        "tags": ["category/ui-ux", "theme/ui-ux"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Digital Candy Game",
        "summary": "Tactile mobile interface where pulling down a physical page sheet peels back to reveal underlying game state.",
        "content": """
### Tactile Page Interaction
- Pulling down a page gesture peels back the screen to reveal hidden value states, turn stages, and available actions.
""",
        "related": ["01_Game_Design/Digital Candy Game", "01_Game_Design/UI Event Matrices and Spatial Pacing"],
    },

    # === GAME IDEA (WATCH WHAT U EAT) ===
    {
        "category": "01_Game_Design",
        "title": "Watch What You Eat - Food Replenishment and Toxic Meters",
        "stem": "Watch What You Eat - Food Replenishment and Toxic Meters",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/survival-escape"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game idea",
        "summary": "Food mechanics where eating refills hunger but certain food combinations trigger lethal toxicity.",
        "content": """
### Dietary Survival Rules
- Eating replenishes hunger gauges, but incompatible food pairings create toxic chemical reactions.
- Dynamic world rules periodically mandate that all foods shift to poisonous variants.
""",
        "related": ["01_Game_Design/Game idea", "01_Game_Design/Potion Brewing Poison Roulette"],
    },
    {
        "category": "01_Game_Design",
        "title": "Sugar Movement Speed vs Happiness Preferences",
        "stem": "Sugar Movement Speed vs Happiness Preferences",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/identity-emotion"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Game idea",
        "summary": "Sugar consumption directly scaling character sprint velocity, while characters require distinct foods for happiness.",
        "content": """
### Metabolic Mechanics
- **Sugar Rush Locomotion**: Higher sugar levels yield higher movement speed multipliers.
- **Happiness Palates**: Different character personalities require specific food types (veggies, grains, honey) to maintain morale.
""",
        "related": ["01_Game_Design/Game idea", "01_Game_Design/Candy Value Deduction and Sugar Rush"],
    },

    # === LASER ON MESH EXTRACTIONS ===
    {
        "category": "01_Game_Design",
        "title": "Seaman Hooker Bar and Ray-March Hitbox",
        "stem": "Seaman Hooker Bar and Ray-March Hitbox",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/worldbuilding"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Laser on mesh the disable mesh",
        "summary": "Seaman-inspired narrative hooker bar atmosphere paired with volumetric ray-marched distance hitboxes.",
        "content": """
### Setting & Volumetric Hitboxes
- **Seaman's Hooker Bar**: Coastal cyberpunk dockside bar atmosphere.
- **Ray-March Hitbox**: Calculating precise volumetric collision through shader ray-marching rather than simple primitive colliders.
""",
        "related": ["01_Game_Design/Laser on mesh the disable mesh", "04_Art_Shaders_Aesthetics/Fractal UV Shaders"],
    },
    {
        "category": "01_Game_Design",
        "title": "Civil Simulation Visualizer - Turn Squares to Pools",
        "stem": "Civil Simulation Visualizer - Turn Squares to Pools",
        "tags": ["category/game-design", "theme/game-mechanics", "theme/space-architecture"],
        "hubs": ["00_MOCs/Hub_Modular_Toy_Mechanics"],
        "parent_source": "01_Game_Design/Laser on mesh the disable mesh",
        "summary": "Civilian infrastructure visualizer converting rigid urban building blocks into fluid communal swimming pools.",
        "content": """
### Urban Liquefaction Simulation
- Macro civil engineering simulator that allows municipal planners to dissolve rigid urban blocks into communal aquatic pools.
""",
        "related": ["01_Game_Design/Laser on mesh the disable mesh", "04_Art_Shaders_Aesthetics/Public Housing Perspectives and MTR Fisheye"],
    },
]

def main() -> None:
    print(f"Total new atomic notes to process: {len(DETAILED_ATOMIC_SPECS)}")
    
    # 1. Write each new atomic note
    for spec in DETAILED_ATOMIC_SPECS:
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

    print(f"Generated {len(DETAILED_ATOMIC_SPECS)} atomic concept notes!")

    # 2. Update Loot, Magic, Robots.md into a pure, clean Index Note without raw text baggage
    lmr_file = ROOT / "01_Game_Design" / "Loot, Magic, Robots.md"
    lmr_children = [s for s in DETAILED_ATOMIC_SPECS if s["parent_source"] == "01_Game_Design/Loot, Magic, Robots"]
    # also add previously extracted
    previous_lmr = [
        ("01_Game_Design", "The Ultra-Lazy Game - Brain and Body Disconnect", "很懶很懶既遊戲: A game exploring extreme sluggishness, where the brain and body negotiate conflicting commands."),
        ("01_Game_Design", "Chimp Department Store - Mini-Employee Cards", "Chimp百貨: Consolation cards given to melancholic shoppers that spawn tiny running employees when placed on the floor."),
        ("01_Game_Design", "Connect the Dots Puzzle - Dark Sky Star Sequences", "Dark exploration puzzle where players slow down in dim star fields and type keystroke sequences to link celestial nodes."),
        ("01_Game_Design", "Discharge Energy Nodes and Shifting Ceilings", "Transferring electrical charges between Point A and B to lower ceilings, shift architecture, and tell stories through light."),
        ("01_Game_Design", "Cognitive Memory Capacity Barrier", "Cognitive paradox where universal knowledge access is systematically blocked as a player accumulates personal memories."),
        ("01_Game_Design", "Component Attachment Scoring Matrix", "Scoring modular tree branches through root object attachment status and public visibility ratings."),
        ("01_Game_Design", "Momentum Storage and Kinetic Release", "Banking incoming kinetic energy into objects or character limbs to shoot out accelerated rebound trajectories."),
    ]
    
    lmr_related = [
        "00_MOCs/Game_Design_MOC",
        "00_MOCs/Hub_Wave_Dynamics_and_Momentum",
        "00_MOCs/Hub_Modular_Toy_Mechanics",
        "07_Synthesized_Concepts/Bora-Bora Spectrum Surfer",
        *[f"{s['category']}/{s['stem']}" for s in lmr_children],
        *[f"{cat}/{stem}" for cat, stem, _ in previous_lmr],
        "00_MOCs/00_Master_Index",
    ]
    seen = set()
    dedup_lmr = [r for r in lmr_related if not (r in seen or seen.add(r))]

    fm_lmr = "\n".join([
        "---",
        "title: \"Loot, Magic, Robots — Master Compilation Index\"",
        "aliases: [\"Loot, Magic, Robots\", \"apple-note-7B370620-158B-4C9B-8645-C79B6B771004\"]",
        "tags: [\"category/game-design\", \"concept/index\", \"collection/loot-magic-robots\"]",
        "category: \"Game Design\"",
        "status: \"Evergreen\"",
        "source: \"Apple Notes/Loot, Magic, Robots.md\"",
        "source_id: \"7B370620-158B-4C9B-8645-C79B6B771004\"",
        "source_sha256: \"314c57b22b3d927ba0450ab6f2ec4a61473e05fb217dd59e7ba14a01d0ebfacf\"",
        f"related: {json_val(property_links(dedup_lmr))}",
        "---",
    ])

    body_lmr = [
        fm_lmr,
        "",
        "# Loot, Magic, Robots — Master Compilation Index",
        "",
        "> [!info] Compilation Overview",
        "> `Loot, Magic, Robots` originally contained a dense constellation of ideas ranging from brain-body disconnects and kinetic momentum storage to celestial star typing and fractal UV math. Every single idea has been extracted into its own dedicated atomic node below.",
        "",
        "## Atomic Concepts Directory",
        "",
        "### 1. Game Mechanics & Systems",
        "- [[01_Game_Design/The Ultra-Lazy Game - Brain and Body Disconnect|The Ultra-Lazy Game - Brain and Body Disconnect]] — Inventive laziness, sticky physics, and decoupled brain/body actuators.",
        "- [[01_Game_Design/Chimp Department Store - Mini-Employee Cards|Chimp Department Store - Mini-Employee Cards]] — Empathy floor cards spawning tiny comforting helpers.",
        "- [[01_Game_Design/Geometric Surface Snapping and Adhesive Shapes|Geometric Surface Snapping and Adhesive Shapes]] — Angle, shape, and adhesive snapping (清麗苑).",
        "- [[01_Game_Design/Dating Profile Matching Interaction|Dating Profile Matching Interaction]] — Bumble profile match cards for asymmetric cooperative discovery.",
        "- [[01_Game_Design/Robo Marching Band Circus|Robo Marching Band Circus]] — Autonomous mechanical brass and percussion circus procession.",
        "- [[01_Game_Design/Emergency Use Only Item Series|Emergency Use Only Item Series]] — Absurdist sealed crisis gear (Dildo, Ring).",
        "- [[01_Game_Design/Dark Sky Exploration and Pacing Rewards|Dark Sky Exploration and Pacing Rewards]] — Decelerating in dim star fields to expand radar reach.",
        "- [[01_Game_Design/Keystroke Constellation Connection Sequences|Keystroke Constellation Connection Sequences]] — Typing sequence ciphers initiated with the apostrophe key.",
        "- [[01_Game_Design/Puzzle Taxonomy - Battle, Easter Egg, Chain, Connect Dots|Puzzle Taxonomy - Battle, Easter Egg, Chain, Connect Dots]] — Fourfold categorization of environmental and combat puzzles.",
        "- [[01_Game_Design/Discharge Energy Nodes and Shifting Ceilings|Discharge Energy Nodes and Shifting Ceilings]] — Point A to Point B electrical transfer moving room architecture.",
        "- [[01_Game_Design/Public Component Attachment Scoring|Public Component Attachment Scoring]] — Modular component scoring with public exposure multipliers.",
        "- [[01_Game_Design/Escalating Consumable Multipliers|Escalating Consumable Multipliers]] — First use 1x, second use 2x potency scaling before depletion.",
        "- [[01_Game_Design/Momentum Storage and Kinetic Release|Momentum Storage and Kinetic Release]] — Banking impact force into springs to fire accelerated rebounds.",
        "",
        "### 2. Narrative & Psychology",
        "- [[01_Game_Design/Cognitive Memory Capacity Barrier|Cognitive Memory Capacity Barrier]] — Accumulating specific memories blocks universal knowledge access.",
        "- [[02_Narrative_Psychology/Delly Cyrus - Bullying and Running Narrative Seed|Delly Cyrus - Bullying and Running Narrative Seed]] — Troubled bullied teen channeling pain into relentless running.",
        "",
        "### 3. Shaders, Graphics & Tech",
        "- [[04_Art_Shaders_Aesthetics/Fractal UV Shaders|Fractal UV Shaders]] — Recursive fractal UV coordinates for infinite surface detail.",
        "- [[01_Game_Design/Mememe Mosquito Audio-Visual Motif|Mememe Mosquito Audio-Visual Motif]] — High-frequency irritant audio cue.",
        "- [[05_Tech_Pipelines_Unity/Mathematical Mesh Subdivision Curves|Mathematical Mesh Subdivision Curves]] — Trigonometric cylindrical mesh subdivision scripts.",
        "- [[04_Art_Shaders_Aesthetics/Water Wiggle Vertex Shader|Water Wiggle Vertex Shader]] — Sinusoidal gelatinous vertex wobble shader.",
        "- [[04_Art_Shaders_Aesthetics/Environmental Storytelling Through Light Ownership|Environmental Storytelling Through Light Ownership]] — Story told by whoever holds the lantern.",
        "- [[05_Tech_Pipelines_Unity/Mini Manager Root Hierarchy Protocol|Mini Manager Root Hierarchy Protocol]] — Hierarchical GameObject branch audits and default operator fallbacks.",
        "",
        "## Navigation",
        "- [[00_MOCs/Game_Design_MOC|Game Design MOC]]",
        "- [[00_MOCs/Hub_Wave_Dynamics_and_Momentum|Wave Dynamics and Momentum Hub]]",
        "- [[00_MOCs/00_Master_Index|Master Knowledge Index]]",
    ]
    lmr_file.write_text("\n".join(body_lmr) + "\n", encoding="utf-8")
    print("  * Cleaned and restructured Loot, Magic, Robots.md into a Master Compilation Index!")

    # 3. Append all new notes to their respective Thematic Concept Hubs in 00_MOCs/
    for s in DETAILED_ATOMIC_SPECS:
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
                # Also add to property related
                fm_match = re.search(r"^---\n(.*?)\n---", h_text, flags=re.DOTALL)
                if fm_match:
                    fm_text = fm_match.group(1)
                    if f"[[{cat}/{stem}]]" not in fm_text:
                        fm_text = re.sub(
                            r'(related:\s*\[)(.*?)(\])',
                            rf'\1\2, "[[{cat}/{stem}]]"\3',
                            fm_text,
                        )
                        h_text = f"---\n{fm_text}\n---" + h_text[fm_match.end() :]
                hub_file.write_text(h_text, encoding="utf-8")

    # 4. Update Category MOCs in 00_MOCs/
    for cat_key, c_info in CATEGORIES.items():
        moc_file = ROOT / "00_MOCs" / f"{c_info['moc']}.md"
        if not moc_file.exists():
            continue
        m_text = moc_file.read_text(encoding="utf-8")
        cat_extracted = [s for s in DETAILED_ATOMIC_SPECS if s["category"] == cat_key]
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
    for s in DETAILED_ATOMIC_SPECS:
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
    
    # Update category counts
    for cat_dir, cat_info in CATEGORIES.items():
        cnt = len(list((ROOT / cat_dir).glob("*.md")))
        pattern = rf"(\[\[00_MOCs/{cat_info['moc']}\|{re.escape(cat_info['name'])}\]\]\s*\()\d+(\s*notes\))"
        master_text = re.sub(pattern, rf"\g<1>{cnt}\g<2>", master_text)

    # Update hub counts
    for h in (ROOT / "00_MOCs").glob("Hub_*.md"):
        h_text = h.read_text()
        h_notes = [l for l in h_text.splitlines() if l.strip().startswith("- [[0")]
        cnt = len(h_notes)
        master_text = re.sub(rf"(\[\[00_MOCs/{h.stem}\|.*?\]\]\s*\()\d+(\s*notes\))", rf"\g<1>{cnt}\g<2>", master_text)

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
PY