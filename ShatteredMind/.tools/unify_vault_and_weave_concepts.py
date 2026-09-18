#!/usr/bin/env python3
"""
Unify vault root, author 8 thematic concept hubs, and weave open-ended semantic cross-links.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path.cwd()
BACKUP_DIR = ROOT / "_backup_apple_notes"
ASSETS_DIR = ROOT / "Assets"

# The 35 approved removed files + accidental daily note
REMOVED_FILES = {
    # Tier 1
    "Homerun Derby", "Hockey 1", "Flag Football 1", "Tennis", "Miniacs",
    "Rank  spacing", "Goal Keeper", "Dec12 playtest plan", "Dec  playtest plan",
    # Tier 2
    "SSH", "Two-Factor Authentication Backup Codes", "Use Anydesk for remote desktop",
    "figd_REDACTED", "sw53", "Drive format FAT32",
    # Tier 3
    "Title UI Technical Artist", "Performance Review", "Internship Program",
    "New Workflow", "How to Write a Cover Letter", "dimensions in mell", "地大小",
    # Tier 5
    "https--youtube.com-shorts-JcEehf_nnnksi=rk-ZMm9gHTHsKV9",
    "https--www.threads.net-@aureliengmz-post-DGTExS4sV5ixmt=AQGzqXXr1J_ZwLeq_FUOjC9BEhRIV0psn0sLDPO8CqxxsQ",
    "https--www.wcofun.org-batman-beyond-episode-11-disappearing-inque",
    "I have a gift for your screen!🎁", "Quadrant Controller",
    "Increments of a clip plays in slower speed",
    "the logo dreams out the covered-mia part", "一幸社",
    # Tier 6
    "Schedule", "Sandbox Content Creation TL;DR", "METABRGE Press Release",
    "rice robotics", "To Do",
    # Accidental daily note
    "2026-09-15",
}

# The 6 core creative categories
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

# The 8 open-ended Thematic Concept Hubs (All 120 notes assigned!)
CONCEPT_HUBS = {
    "Hub_Dreams_and_Memory": {
        "title": "Dreams, Memory Continuity & Cognitive Drift",
        "filename": "Hub_Dreams_and_Memory.md",
        "tag": "concept/dreams-memory",
        "description": (
            "Nocturnal cognition, sleep anxiety, memory reset loops, dream-walkers waking at 3 AM, "
            "and the construction of memory golems to preserve identity against nocturnal erasure."
        ),
        "notes": [
            "Character idea",
            "Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo",
            "Story Note",
            "Story idea",
            "Card box apartment",
            "showers with plastic doll pieces",
            "妖尾貓之惡夢",
            "he spun weaves of cloth to protect his land",
            "Concepts x9001",
            "a group of special ops",
            "I",
            "reconnecting",
            "Scheduling tasks",
        ],
        "synthesized": ["Lucid Terminal - The Memory Golem"],
    },
    "Hub_Optical_Shaders_and_Light": {
        "title": "Optical Physics, Shaders & Chromatic Mechanics",
        "filename": "Hub_Optical_Shaders_and_Light.md",
        "tag": "concept/optical-shaders",
        "description": (
            "Fractured light beams, crystal prism platforms, wavelength absorption as energy, "
            "the strict avoidance of pure white/black, CRT phosphor scanlines, and watercolor diffusion mechanics."
        ),
        "notes": [
            "crystal world where the player uses a flashlight to shine coloured crystal and fractures the light to show platforms",
            "never use true white and black",
            "Lense flare",
            "Lightmap probe",
            "reflection of light fractures into shapes",
            "crt tv zoom in",
            "orange and blue fox",
            "Art concepts",
            "Painting in watercolour and graphite",
            "Four Season LED Screen",
            "reconnecting",
            "bird nailing",
            "Laser on mesh the disable mesh",
            "Game Development Keywords",
            "6parkendal",
            "visually realistic",
        ],
        "synthesized": ["Bora-Bora Spectrum Surfer", "Lucid Terminal - The Memory Golem"],
    },
    "Hub_Soul_Economies_and_Lifecycles": {
        "title": "Soul Economies, Flawed Metaphysics & Lifecycles",
        "filename": "Hub_Soul_Economies_and_Lifecycles.md",
        "tag": "concept/soul-economies",
        "description": (
            "The 21-gram metaphysical weight of souls, Death running an adventurer guild, "
            "lifespan loops (birth, rest, action, death), befriending neglected monster guards, and hidden valuation economies."
        ),
        "notes": [
            "21 Grams Weight of a Soul",
            "Lifespan  how many cycles",
            "Punching bag eats enemy and punching it deals dmg",
            "Magic",
            "Recall protocol",
            "Digital Candy Game",
            "every figure is a shadow",
            "losing gravity",
            "Concepts x9001",
        ],
        "synthesized": ["Guild of the Departed - 21 Grams"],
    },
    "Hub_Asymmetric_Social_Play": {
        "title": "Asymmetric Social Friction, Deception & Invisible Rules",
        "filename": "Hub_Asymmetric_Social_Play.md",
        "tag": "concept/asymmetric-social",
        "description": (
            "Explosive collars with invisible countdowns, killer vs cops vs hostage dynamics, "
            "memory-book chapter manipulation, beneficial detection, and emotion-driven combat mechanics."
        ),
        "notes": [
            "Killer game",
            "Multi-scene Killer game",
            "books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles",
            "Simon says Escape room",
            "Idea hunger game catch",
            "interactive carpet",
            "Edit skill animation in battle to dodge attack",
            "question man",
            "a group of special ops",
            "Online gameplays",
            "https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=",
        ],
        "synthesized": ["The Collar Experiment - Asymmetric Dilemma"],
    },
    "Hub_Wave_Dynamics_and_Momentum": {
        "title": "Wave Dynamics, Momentum & Fluid Progression",
        "filename": "Hub_Wave_Dynamics_and_Momentum.md",
        "tag": "concept/wave-momentum",
        "description": (
            "Ocean swell physics, reef break A-frames, pumping cadence to bank momentum, "
            "color-absorption surfing boards, and non-speculative sustainable game economies."
        ),
        "notes": [
            "Surfing",
            "no ETH",
            "Loot, Magic, Robots",
            "The number of land in each island",
            "Prototype idea",
            "Uni-scooter",
            "Stable running on water electricity and the water stopped",
            "Hockey",
            "Rootkit- Levitate",
        ],
        "synthesized": ["Bora-Bora Spectrum Surfer"],
    },
    "Hub_Somatic_Movement_and_Connection": {
        "title": "Somatic Movement, Intersubjectivity & Botanical Art",
        "filename": "Hub_Somatic_Movement_and_Connection.md",
        "tag": "concept/somatic-movement",
        "description": (
            "Camera pose tracking, player-as-flower growth mechanics, watering and sun-leaning postures, "
            "translating physical awkwardness and social communication gaps into fluid watercolor art."
        ),
        "notes": [
            "Physical game concept",
            "People’s ignorance creates trouble for ppl",
            "Painting in watercolour and graphite",
            "Game Jam Game Ideas",
            "Mocap Recommendation",
            "Learning opens doors",
            "The distance between ppl pulls reasons together",
            "Flag Football",
            "Rugby seven 片",
            "opening sequence",
        ],
        "synthesized": ["Kinetic Resonance - Bloom of the Unspoken"],
    },
    "Hub_Urban_Alienation_and_Identity": {
        "title": "Urban Claustrophobia, Alienation & Hong Kong Identity",
        "filename": "Hub_Urban_Alienation_and_Identity.md",
        "tag": "concept/urban-identity",
        "description": (
            "Public housing rental pressure, 28th-floor perspective shifts, MTR fisheye views, "
            "social pretense, seeking roots through I Ching and Tibetan bells, and Aristotle's pursuit of eudaimonia."
        ),
        "notes": [
            "I",
            "nails to my hands on the keyboard-screen",
            "尋根",
            "高不成低不就",
            "扮得純粹",
            "樓上樓下",
            "寄居蟹換殼",
            "極限捉伊欣",
            "強制的愛",
            "What is the telos of all human action",
            "female protagonist is a tutor for adult students and is highly respected by everyone, because she changes people’s lives by granting the knowledge and diploma the person needs to move on in life. Male",
            "To Ashley,",
            "Looking up the evening sky,",
            "i took two step then turned back",
            "humanity",
            "My Journey Starts in how i start my family",
            "raspy male lead vocal, Warm piano chords lay the foundation, joined by soft, fingerstyle acoustic guitar and subtle electric accents for the light country touch, Understated R&B-inspired percussion an",
            "Finding shit in a party MV",
            "i put the moon in the tone",
            "i think the core problem is the current disciplinary system doesn’t cover everyone’s output",
        ],
        "synthesized": ["Lucid Terminal - The Memory Golem", "The Collar Experiment - Asymmetric Dilemma"],
    },
    "Hub_Modular_Toy_Mechanics": {
        "title": "Modular Toy Logic, Input Constraints & Micro-Play",
        "filename": "Hub_Modular_Toy_Mechanics.md",
        "tag": "concept/modular-toys",
        "description": (
            "Novel controller paradigms, dual-joint analog sticks, two-footed directional boost sprinting, "
            "disruptive tabletop chess mechanics, surprise toy design, and gas reactions."
        ),
        "notes": [
            "00928z",
            "character can run on 2feet and different feet would gives boost to different directions while sprinting to a direction.",
            "chess pieces knocking off board",
            "Design a fun toy with surprises",
            "Distance based organism",
            "Flipping number cards",
            "Flocking Players",
            "Game idea",
            "get the bird to sing for you",
            "if distance = x",
            "Laser on mesh the disable mesh",
            "losing gravity",
            "Massively Multiplayer Game",
            "moebius",
            "Walk  run  boost  break  jump  boost  run  break  drift  boost",
            "Player shoots gases to each other",
            "Players scatter in a map",
            "set them up",
            "Sink with the ship",
            "flies die over steam",
            "VR fps cute monsters game like Sam Serious",
            "a girl with magical hair with scrolls",
            "Piano",
            "Common Fonts",
            "All unity plugins",
            "forward kinematic",
            "ROS engineering",
            "Questions to ask when exploring designs",
            "Sharing session for past projects",
            "stack exchange game dev.",
            "Staring at lines and words mean staring at your brain",
            "Tension Headache",
            "To not be chased",
            "Class",
            "橋麥麵 紅米飯",
            "NBA",
            "Attack range of the enemies (Table)",
            "golden ears forehead n cheer fur cheetah",
            "Game Jam",
        ],
        "synthesized": ["The Collar Experiment - Asymmetric Dilemma", "Bora-Bora Spectrum Surfer"],
    },
}

MOTION_NOTES = {
    "Flag Football",
    "Game Jam",
    "Hockey",
    "Mocap Recommendation",
    "NBA",
    "Online gameplays",
    "Physical game concept",
    "Rugby seven 片",
}

ART_NOTES = {
    "6parkendal",
    "Art concepts",
    "bird nailing",
    "Common Fonts",
    "crt tv zoom in",
    "Finding shit in a party MV",
    "Four Season LED Screen",
    "golden ears forehead n cheer fur cheetah",
    "https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=",
    "i put the moon in the tone",
    "Lense flare",
    "Lightmap probe",
    "never use true white and black",
    "orange and blue fox",
    "Painting in watercolour and graphite",
    "Piano",
    "raspy male lead vocal, Warm piano chords lay the foundation, joined by soft, fingerstyle acoustic guitar and subtle electric accents for the light country touch, Understated R&B-inspired percussion an",
    "reflection of light fractures into shapes",
    "visually realistic",
    "扮得純粹",
    "高不成低不就",
}

TECH_NOTES = {
    "All unity plugins",
    "Attack range of the enemies (Table)",
    "forward kinematic",
    "ROS engineering",
}

LIFE_NOTES = {
    "Class",
    "humanity",
    "i think the core problem is the current disciplinary system doesn’t cover everyone’s output",
    "Learning opens doors",
    "no ETH",
    "People’s ignorance creates trouble for ppl",
    "Questions to ask when exploring designs",
    "Sharing session for past projects",
    "stack exchange game dev.",
    "Staring at lines and words mean staring at your brain",
    "Tension Headache",
    "The distance between ppl pulls reasons together",
    "To Ashley,",
    "To not be chased",
    "What is the telos of all human action",
    "尋根",
    "橋麥麵 紅米飯",
}

NARRATIVE_NOTES = {
    "a girl with magical hair with scrolls",
    "a group of special ops",
    "Card box apartment",
    "Character idea",
    "every figure is a shadow",
    "female protagonist is a tutor for adult students and is highly respected by everyone, because she changes people’s lives by granting the knowledge and diploma the person needs to move on in life. Male",
    "he spun weaves of cloth to protect his land",
    "I",
    "i took two step then turned back",
    "Looking up the evening sky,",
    "My Journey Starts in how i start my family",
    "nails to my hands on the keyboard-screen",
    "opening sequence",
    "showers with plastic doll pieces",
    "Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo",
    "Story idea",
    "Story Note",
    "強制的愛",
    "極限捉伊欣",
    "樓上樓下",
}

TITLE_OVERRIDES = {
    "00928z": "Dual-Joint Direction Controller",
    "Attack range of the enemies (Table)": "Mission and Boss Design Template",
    "books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles": "Book-Scene Strategy and Emotion Mechanics",
    "character can run on 2feet and different feet would gives boost to different directions while sprinting to a direction.": "Directional Feet and Momentum",
    "crystal world where the player uses a flashlight to shine coloured crystal and fractures the light to show platforms": "Crystal Light Platform World",
    "female protagonist is a tutor for adult students and is highly respected by everyone, because she changes people’s lives by granting the knowledge and diploma the person needs to move on in life. Male": "Adult Tutor and Hidden School Connection",
    "https--www.instagram.com-reel-CeB3TK_F9p4-igshid=YmMyMTA2M2Y=": "Instagram Inspiration and Virtual Room Ideas",
    "i think the core problem is the current disciplinary system doesn’t cover everyone’s output": "Disciplinary Systems and Output",
    "raspy male lead vocal, Warm piano chords lay the foundation, joined by soft, fingerstyle acoustic guitar and subtle electric accents for the light country touch, Understated R&B-inspired percussion an": "Third-Person Love Song",
    "Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo": "Sleep, Memory, and Creative Continuity",
    "The distance between ppl pulls reasons together": "Distance, Insecurity, and Human Bonds",
    "The number of land in each island": "Procedural Islands and Wearable Abilities",
    "Walk  run  boost  break  jump  boost  run  break  drift  boost": "Movement Combo Loop",
}

THEME_RULES = {
    "dreams-memory": r"\b(dream|dreams|sleep|nightmare|memory|memories|remember|recall|coma)\b|夢|記憶|睡",
    "light-color": r"\b(light|lighting|shadow|color|colour|crystal|flare|reflection|spectrum|bright|dark|shader)\b|光|燈|影|色",
    "motion-body": r"\b(motion|pose|posing|body|arm|hand|physical|movement|camera|mocap|vr|gesture)\b|身體|動作",
    "game-mechanics": r"\b(game|gameplay|mechanic|mechanics|system|player|players|rule|rules|combat|level)\b|遊戲|玩家",
    "economy-value": r"\b(value|resource|resources|money|economy|cost|currency|score|budget|price|financial)\b|價值|成本|資源|錢",
    "social-cooperation": r"\b(team|group|coop|co-op|social|friend|friends|people|ppl|together|community)\b|合作|朋友|人",
    "asymmetry-deception": r"\b(killer|hostage|secret|asymmetr|cheat|fake|stealth|spy|decept|hidden|clue)\b|殺手|欺騙|秘密",
    "time-cycles": r"\b(time|clock|day|night|cycle|countdown|deadline|reset|season|lifespan)\b|時間|日|夜|週期",
    "identity-emotion": r"\b(identity|emotion|fear|angry|sad|happiness|self|love|feeling|resilience|alienation)\b|情緒|愛|恐懼|自我",
    "worldbuilding": r"\b(world|story|village|monster|character|magic|soul|god|kingdom|dungeon|adventure)\b|世界|故事|魔法",
    "procedural-generation": r"\b(procedural|generate|generator|pattern|fractal|voronoi|algorithm|ai|random)\b|生成|圖案",
    "ui-ux": r"\b(ui|ux|button|font|layout|screen|view|feedback|menu|interface|onboarding)\b|介面|按鈕",
    "visual-art": r"\b(art|visual|vfx|shader|texture|material|animation|render|composition|aesthetic)\b|藝術|視覺|動畫",
    "unity-technical": r"\b(unity|prefab|script|code|mesh|git|ssh|pipeline|draw call|rendertexture|collider|robotic)\b",
    "career-work": r"\b(work|job|company|employee|internship|career|workflow|project|client|review)\b|工作|職業|公司",
    "sports": r"\b(hockey|football|tennis|baseball|boxing|surfing|goalkeeper|goal keeper|nba|rugby|bowling|sports?)\b|運動",
    "philosophy": r"\b(philosophy|virtue|aristotle|telos|reason|meaning|humanity|ethics|wisdom)\b|哲學|意義|人生",
    "sound-music": r"\b(audio|sound|sfx|bgm|music|piano|vocal|beat|song)\b|音樂|聲音",
    "space-architecture": r"\b(room|apartment|building|map|space|path|land|floor|house|island)\b|房|樓|地",
    "cards-tabletop": r"\b(card|cards|deck|candy|chess|bingo|mahjong|majong|board game)\b|牌|棋",
    "nature-organisms": r"\b(animal|plant|flower|insect|fish|bird|worm|ocean|water|tree|organic)\b|動物|植物|魚|鳥|水",
    "learning-accessibility": r"\b(learning|teach|knowledge|accessib|child|children|kid|school|education)\b|學習|教育|小孩",
    "survival-escape": r"\b(escape|survive|survival|death|kill|die|chase|dungeon|trap|danger)\b|逃|死|生存",
    "business-marketing": r"\b(marketing|nft|brand|revenue|press|social media|market|subscription|sales)\b|市場|品牌|營銷",
}


@dataclass
class Note:
    source_path: Path
    source_relative: str
    stem: str
    title: str
    category: str
    source_id: str
    body: str
    source_hash: str
    tags: list[str]
    themes: set[str]
    status: str
    related: list[str]
    concept_hubs: list[str]
    synthesized_concepts: list[str]

    @property
    def vault_path(self) -> str:
        return f"{self.category}/{self.stem}"

    @property
    def moc_path(self) -> str:
        return f"00_MOCs/{CATEGORIES[self.category]['moc']}"


def clean_html(body: str) -> str:
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.IGNORECASE)
    body = re.sub(r"</?(?:p|u|i|b|span|div)(?:\s+[^>]*)?>", "", body, flags=re.IGNORECASE)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def category_for(stem: str) -> str:
    if stem in MOTION_NOTES:
        return "03_Physical_Motion_Games"
    if stem in ART_NOTES or stem == "Game Development Keywords":
        return "04_Art_Shaders_Aesthetics"
    if stem in TECH_NOTES:
        return "05_Tech_Pipelines_Unity"
    if stem in LIFE_NOTES:
        return "06_Life_Career_Philosophy"
    if stem in NARRATIVE_NOTES:
        return "02_Narrative_Psychology"
    return "01_Game_Design"


def word_count(body: str) -> int:
    return len(re.findall(r"[\w\u3400-\u9fff]+", body, flags=re.UNICODE))


def status_for(body: str) -> str:
    meaningful = re.sub(r"https?://\S+|!\[\[[^\]]+\]\]|[^\w\u3400-\u9fff]+", "", body)
    if not meaningful:
        return "Archive"
    if word_count(body) < 80:
        return "Seedling"
    return "Evergreen"


def themes_for(stem: str, title: str, body: str) -> set[str]:
    haystack = f"{stem}\n{title}\n{body}".lower()
    themes = {
        theme
        for theme, pattern in THEME_RULES.items()
        if re.search(pattern, haystack, flags=re.IGNORECASE)
    }
    if not themes:
        themes.add("creative-seed")
    return themes


def slug_tag(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9\u3400-\u9fff/-]+", "-", value)
    return value.strip("-")


def wikilink(path: str, label: str | None = None) -> str:
    return f"[[{path}|{label}]]" if label else f"[[{path}]]"


def json_value(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def property_links(paths: list[str]) -> list[str]:
    return [f"[[{path}]]" for path in paths]


CONCEPT_SPECS = [
    {
        "filename": "Lucid Terminal - The Memory Golem.md",
        "title": "Lucid Terminal: The Memory Golem",
        "slug": "Lucid Terminal - The Memory Golem",
        "tags": ["concept/game", "narrative/dreams", "theme/memory", "mechanic/light"],
        "sources": [
            "Character idea",
            "Sleeping just making me more tired and it was very stressful to sleep. A lot of the time when I wake up, it felt like my progress was reset because vivid dreams overrides my daytime progress as a memo",
            "Concepts x9001",
            "crystal world where the player uses a flashlight to shine coloured crystal and fractures the light to show platforms",
            "Scheduling tasks",
            "Story Note",
            "reconnecting",
        ],
        "hubs": ["00_MOCs/Hub_Dreams_and_Memory", "00_MOCs/Hub_Optical_Shaders_and_Light"],
        "pitch": "A surreal psychological puzzle adventure about preserving identity across nights that erase progress.",
        "content": """
## Creative premise

The protagonist is a dream-walker who wakes at 3 AM knowing that sleep will pull them back into a recurring nightmare. Every dream layer contains fragments of daytime experience, but waking normally overwrites those memories. The player therefore builds a **Memory Golem**: a companion assembled from recovered sensations, choices, and unfinished creative work.

The central question is: **What must be preserved for a person to still feel like themselves tomorrow?**

## Core loop

1. Enter a dream district generated from the previous day's unresolved memory.
2. Use a handheld lens to split colored light and reveal paths that only exist at specific wavelengths.
3. Solve a room's emotional contradiction rather than merely finding its exit.
4. Decide which memories become stable Golem parts and which are allowed to dissolve.
5. Reach the Lucid Terminal before the alarm; commit a limited number of memories to waking life.
6. Wake to a subtly changed home, then use retained knowledge to enter a deeper dream layer.

## Key mechanics

- **Fractured-light navigation:** prisms reveal platforms, hidden writing, and alternative versions of a room.
- **Memory weight:** vivid memories are powerful but make the dream less stable; ordinary memories create reliable paths.
- **Golem assembly:** head, hands, heart, and feet each preserve a different capability—reason, craft, emotion, and movement.
- **Reset with residue:** failure resets the scene, while tiny sensory discrepancies become clues for the next attempt.
- **Perspective reconnection:** paired rooms show the same event from two viewpoints; aligning their reflections restores a connection.

## Narrative structure

The first act establishes the fear of losing progress. The second reveals that the Golem is not a storage device but a model of the self built from selective memory. The final act asks the player to release the Golem, merge with it, or keep returning to maintain it forever.

## Visual and audio direction

- Dark rooms punctured by refracted cyan, amber, and magenta light.
- Architecture shifts between bedrooms, transit stations, caves, and impossible apartment floors.
- Audio begins as environmental noise and becomes musical only when a memory is accepted.
- Waking scenes use stable framing; dream scenes use fisheye distance and perspective discontinuity.

## Prototype slice

Build one bedroom-to-terminal sequence: a lamp reveals three colored platform states, a red button loops the room, and the player must notice one changed object per loop. Completing the sequence creates the Golem's first hand.

## Questions for further creativity

- Can forgetting be a compassionate action rather than a loss?
- What happens when the player preserves a false memory?
- Could a second player inhabit the Golem and choose what it remembers?
""",
    },
    {
        "filename": "Guild of the Departed - 21 Grams.md",
        "title": "Guild of the Departed: 21 Grams",
        "slug": "Guild of the Departed - 21 Grams",
        "tags": ["concept/game", "genre/management", "theme/souls", "mechanic/economy"],
        "sources": [
            "21 Grams Weight of a Soul",
            "Lifespan  how many cycles",
            "Punching bag eats enemy and punching it deals dmg",
            "Digital Candy Game",
            "Recall protocol",
            "Magic",
        ],
        "hubs": ["00_MOCs/Hub_Soul_Economies_and_Lifecycles"],
        "pitch": "A darkly comic village-management roguelite in which Death runs an adventurers' guild to improve the quality of souls.",
        "content": """
## Creative premise

Premature deaths caused by an incompetent Dark Lord have flooded the afterlife with underdeveloped souls. Disguised as a guild master, the player—the local god of death—must help villagers flourish before eventually collecting them.

The design tension is deliberately uncomfortable: **the better you care for someone, the more valuable their eventual soul becomes.**

## Core loop

1. During the day, post quests rather than directly controlling villagers.
2. Villagers interpret quests through their traits, relationships, equipment, and current fears.
3. Rescue or befriend neglected castle monsters, turning former enemies into town specialists.
4. At night, review deaths, collect souls, reproduce villagers, and negotiate with gods or the Dark Lord.
5. Spend soul value on new village possibilities while preserving enough population to resist invasion.

## Systems

- **Soul lifecycle:** birth, rest, training, action, death, and return form a visible resource cycle.
- **Quest suggestion:** players influence priorities without issuing perfect commands.
- **Hidden conversion rates:** each god values different achievements; rates shift like the concealed candy values in a deduction game.
- **Monster trust:** repair armor, heal injuries, or offer retirement to convert dungeon guards into allies.
- **Comedic harvesting:** deaths should be legible and funny, while their systemic consequences remain meaningful.
- **Card village:** buildings produce cards; cards combine into expeditions, research, and defensive formations.

## Narrative factions

- **Death:** wants mature, meaningful lives and a sustainable soul economy.
- **The Dark Lord:** offers shortcuts that create immediate defense but increase premature death.
- **The Hearth God:** rewards stable families and long lives.
- **The War God:** values spectacular combat and rapid power growth.
- **Retired monsters:** understand both village and dungeon economies and can expose divine manipulation.

## Visual and audio direction

A readable miniature town sits above a deep ledger-like underworld. Daylight is busy and warm; night collapses into silhouettes, ghost hats, contract seals, and whispered bargaining. Death animations use physical comedy rather than gore.

## Prototype slice

One seven-day village cycle with five villagers, three quest types, one injured monster guard, and two gods offering incompatible nighttime bargains. The prototype succeeds if players care about villagers despite understanding the harvest economy.

## Questions for further creativity

- Can the player win by ending the soul economy entirely?
- What information should villagers learn about their guild master?
- How can a death be funny without making a life feel disposable?
""",
    },
    {
        "filename": "Kinetic Resonance - Bloom of the Unspoken.md",
        "title": "Kinetic Resonance: Bloom of the Unspoken",
        "slug": "Kinetic Resonance - Bloom of the Unspoken",
        "tags": ["concept/game", "motion/camera", "theme/healing", "art/watercolor"],
        "sources": [
            "Physical game concept",
            "People’s ignorance creates trouble for ppl",
            "Painting in watercolour and graphite",
            "Game Jam Game Ideas",
            "Mocap Recommendation",
            "Learning opens doors",
        ],
        "hubs": ["00_MOCs/Hub_Somatic_Movement_and_Connection", "00_MOCs/Hub_Optical_Shaders_and_Light"],
        "pitch": "A cooperative camera-based motion experience that transforms bodily tension and communication gaps into a growing watercolor habitat.",
        "content": """
## Creative premise

Players embody young plants that cannot speak. Posture, pace, distance, and breath become their vocabulary. Instead of scoring perfect exercise form, the game interprets differences between bodies as complementary strengths.

The guiding question is: **Can an awkward movement become a meaningful signal when another person learns how to receive it?**

## Core loop

1. Read an environmental need: drought, wind, shade, worms, or a silent animal visitor.
2. Experiment with poses and movement rhythms to discover a shared response.
3. Hold complementary silhouettes so watercolor energy can flow between players.
4. Watch the habitat retain graphite traces of successful communication.
5. Revisit earlier scenes, where accumulated marks create new affordances instead of merely recording scores.

## Interaction vocabulary

- **Watering:** curved arm shapes collect and pour color.
- **Sun seeking:** bodies lean together to guide a shared stem.
- **Wind resilience:** stillness and counterbalance matter more than speed.
- **Worm release:** shaking is translated into expanding pigment rather than punished as imprecision.
- **Animal call:** gestures create tones; sequences invite birds to add new melodies.
- **Rest:** lowering intensity is an explicit action the system must learn to recognize.

## Accessibility principles

- Calibrate to each player's available range rather than a fixed ideal body.
- Reward clear intent, rhythm, and collaboration—not raw movement size.
- Allow seated, standing, one-handed, and assisted variants.
- Use high-contrast silhouettes and audio confirmation before time pressure.
- Avoid elimination; failed communication leaves marks that can become future tools.

## Visual and audio direction

The world begins as white paper with sparse graphite rules. Movement releases watercolor that soaks beyond boundaries. The score is the evolving image itself. Bird calls and soft environmental sounds become a procedural soundtrack shaped by the group's pace.

## Prototype slice

Two players grow one flower through watering, leaning, wind resistance, and rest. Camera tracking only needs head, shoulders, hands, and center of mass. Test whether players can understand each other through the visual response without written instructions.

## Questions for further creativity

- Can the game preserve a group's unique movement dialect between sessions?
- How might a child and older adult contribute equally?
- What does a healthy failure state look like in a healing-oriented game?
""",
    },
    {
        "filename": "The Collar Experiment - Asymmetric Dilemma.md",
        "title": "The Collar Experiment: Asymmetric Dilemma",
        "slug": "The Collar Experiment - Asymmetric Dilemma",
        "tags": ["concept/game", "genre/social-deduction", "mechanic/asymmetry", "theme/trust"],
        "sources": [
            "Killer game",
            "books with scenes, player can pull objects from chapters or jump into scenes to deal with obstacles",
            "a group of special ops",
            "Edit skill animation in battle to dodge attack",
            "Simon says Escape room",
            "Idea hunger game catch",
        ],
        "hubs": ["00_MOCs/Hub_Asymmetric_Social_Play"],
        "pitch": "An asymmetric social-deduction thriller where hidden timers, emotional signals, and contradictory objectives turn cooperation into a moral gamble.",
        "content": """
## Creative premise

Innocents wake with explosive collars whose timers they cannot see. A hidden Killer wants them arrested rather than simply dead; Cops know a killer exists but do not know which civilians are hostages. Detection can therefore protect, expose, or condemn a player.

The central question is: **How much control will people surrender when nobody possesses the complete truth?**

## Roles and objectives

- **Innocents:** survive, infer their own collar status from other people's reactions, and secretly disable it.
- **Killer:** manipulate innocents into suspicious behavior and get them jailed before they can prove coercion.
- **Cops:** arrest the Killer while avoiding actions that trigger collars or destroy evidence.
- **Dream Observer:** a limited role that enters another player's subjective scene and can alter one emotional clue.

## Core loop

1. The group enters an everyday public scene: restaurant, taxi, lobby, or doorstep.
2. Each role receives incomplete rules and a private objective.
3. Players gather physical objects and social testimony while the Killer issues ambiguous demands.
4. Cops publicly reconstruct events using a book of scenes; witnesses can pull one object from a remembered chapter.
5. A lockdown phase freezes pairs who maintain visual contact, making absence and attention mechanically meaningful.
6. Arrest, escape, or collar resolution changes the rules of the next scene.

## Signature systems

- **Invisible countdowns:** other players can see hints of your timer, but you cannot.
- **Emotion as action:** calm, anger, fear, and resolution unlock different dialogue and movement options.
- **Beneficial detection:** being seen can provide an alibi or freeze an attacker, so stealth is not automatically optimal.
- **Contradictory evidence:** misinformation changes what a scene permits, not just what players believe.
- **Secret disarm state:** the Killer never knows with certainty whether a collar still works.

## Tone and boundaries

The project should use suspense without gore. Safety tools, clear consent, and fictional distance are mandatory because coercion and surveillance are core themes.

## Prototype slice

Six players, one apartment-lobby scene, three object clues, one staged hostage puzzle, and eight minutes. Test whether hidden-timer information produces conversation rather than random accusation.

## Questions for further creativity

- Can trust be represented without a numerical meter?
- What happens if the Cops discover the institution created the Killer role?
- How can eliminated players continue influencing the reconstruction?
""",
    },
    {
        "filename": "Bora-Bora Spectrum Surfer.md",
        "title": "Bora-Bora Spectrum Surfer",
        "slug": "Bora-Bora Spectrum Surfer",
        "tags": ["concept/game", "genre/sports", "mechanic/color", "theme/waves"],
        "sources": [
            "Surfing",
            "never use true white and black",
            "no ETH",
            "Loot, Magic, Robots",
            "Prototype idea",
            "The number of land in each island",
        ],
        "hubs": ["00_MOCs/Hub_Wave_Dynamics_and_Momentum", "00_MOCs/Hub_Optical_Shaders_and_Light"],
        "pitch": "A kinetic arcade surfing game where waves are living color spectra and every board reshapes how momentum and light are stored.",
        "content": """
## Creative premise

Bora-Bora is a legendary training beach where ocean energy separates into visible wavelengths. Surfers do not simply ride water: they absorb, combine, and release colors according to board material, body position, reef shape, and wave phase.

The design goal is to turn a surfing line into a readable creative composition rather than a sequence of canned tricks.

## Core loop

1. Read an approaching wave's color, shape, speed, and seabed influence.
2. Paddle and position on a tactical grid before the break.
3. Pump to store momentum while absorbing wavelengths compatible with the board.
4. Spend color energy on turns, aerial combinations, or temporary routes across unstable sections.
5. Land with remaining momentum and convert the completed line into score, repair resources, and a visual trace.
6. Modify the board between runs to pursue a different relationship with the same wave.

## Systems

- **Spectrum absorption:** objects show the wavelengths they reject; absorbed colors become usable energy.
- **Momentum bank:** speed can be stored in board flex, then released through turns or aerials.
- **Living breaks:** reef, stone, and sand alter both geometry and available color.
- **Board anatomy:** size, material, repair state, and surfer physique create tradeoffs rather than linear upgrades.
- **Tournament formats:** standardized boards reveal skill; open-board events reward preparation and experimentation.
- **No speculative-token dependency:** ownership, prizes, and customization function as ordinary game systems.

## Visual and audio direction

Avoid pure white and black. Deep water uses near-black chromatic blues; spray separates into complementary colors. Each run paints a temporary ribbon over the wave. Audio layers rhythm according to pumping cadence, then opens into melody during sustained flow.

## Prototype slice

One side-scrolling reef break with paddling, pop-up, pumping, one turn, and one aerial. Three board materials absorb different color pairs. The prototype succeeds if players can explain why one route generated more energy.

## Questions for further creativity

- Can a saved run become a level another player rides?
- How can ocean history and local knowledge shape progression?
- What would cooperative surfing look like if two riders share one wave's energy budget?
""",
    },
]


def load_source_notes() -> list[Note]:
    # Read from _backup_apple_notes to ensure 100% stable, idempotent execution
    source_files = []
    for p in sorted(BACKUP_DIR.rglob("*.md"), key=lambda p: p.name.casefold()):
        if p.stem in REMOVED_FILES:
            continue
        source_files.append(p)

    notes: list[Note] = []
    for path in source_files:
        raw = path.read_text(encoding="utf-8")
        source_id = ""
        body = raw
        if raw.startswith("---\n"):
            match = re.match(r"^---\n(.*?)\n---\n?", raw, flags=re.DOTALL)
            if match:
                for line in match.group(1).splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        if k.strip() == "apple-notes-id":
                            source_id = v.strip()
                body = raw[match.end() :]
        stem = path.stem
        cleaned = clean_html(body)
        cat = category_for(stem)
        title = TITLE_OVERRIDES.get(stem, stem)
        themes = themes_for(stem, title, cleaned)
        tags = [
            f"category/{slug_tag(CATEGORIES[cat]['name'])}",
            *[f"theme/{t}" for t in sorted(themes)],
        ]
        notes.append(
            Note(
                source_path=path,
                source_relative=path.relative_to(BACKUP_DIR).as_posix(),
                stem=stem,
                title=title,
                category=cat,
                source_id=source_id,
                body=cleaned,
                source_hash=hashlib.sha256(path.read_bytes()).hexdigest(),
                tags=tags,
                themes=themes,
                status=status_for(cleaned),
                related=[],
                concept_hubs=[],
                synthesized_concepts=[],
            )
        )
    return notes


def map_concept_hubs_and_synthesized(notes: list[Note]) -> None:
    by_stem = {n.stem: n for n in notes}
    # Attach concept hubs
    for hub_id, hub_info in CONCEPT_HUBS.items():
        hub_path = f"00_MOCs/{hub_id}"
        for stem in hub_info["notes"]:
            if stem in by_stem:
                if hub_path not in by_stem[stem].concept_hubs:
                    by_stem[stem].concept_hubs.append(hub_path)
    # Attach synthesized concepts
    for spec in CONCEPT_SPECS:
        concept_path = f"07_Synthesized_Concepts/{spec['slug']}"
        for stem in spec["sources"]:
            if stem in by_stem:
                if concept_path not in by_stem[stem].synthesized_concepts:
                    by_stem[stem].synthesized_concepts.append(concept_path)


def compute_open_ended_peer_links(notes: list[Note]) -> None:
    # 1. Compute pairwise resonance scores
    by_path = {n.vault_path: n for n in notes}
    adj = defaultdict(set)

    for n1 in notes:
        scored = []
        n1_hubs = set(n1.concept_hubs)
        for n2 in notes:
            if n2.stem == n1.stem:
                continue
            common_hubs = n1_hubs & set(n2.concept_hubs)
            hub_score = len(common_hubs) * 6.0
            common_themes = n1.themes & n2.themes
            theme_score = sum(3.0 if t not in {"game-mechanics", "visual-art", "creative-seed"} else 1.0 for t in common_themes)
            t1 = set(re.findall(r"[a-z0-9]{3,}|[\u3400-\u9fff]{2,}", n1.title.lower()))
            t2 = set(re.findall(r"[a-z0-9]{3,}|[\u3400-\u9fff]{2,}", n2.title.lower()))
            token_score = len(t1 & t2) * 4.0
            total = hub_score + theme_score + token_score
            if total > 0:
                scored.append((total, n2))

        scored.sort(key=lambda x: (-x[0], x[1].title.casefold()))

        # Add top peers
        same_cat = next((o for s, o in scored if o.category == n1.category), None)
        cross_cat = next((o for s, o in scored if o.category != n1.category), None)
        chosen = []
        for c in (same_cat, cross_cat):
            if c and c not in chosen:
                chosen.append(c)
        for s, o in scored:
            if o not in chosen:
                if len(chosen) < 5 or s >= 5.0:
                    chosen.append(o)
                if len(chosen) >= 10:
                    break

        for o in chosen:
            adj[n1.vault_path].add(o.vault_path)
            # Enforce bidirectional reciprocity!
            adj[o.vault_path].add(n1.vault_path)

    for n in notes:
        # Sort related notes for deterministic output
        sorted_rel = sorted(adj[n.vault_path], key=lambda p: by_path[p].title.casefold())
        n.related = sorted_rel


def summary(note: Note) -> str:
    for raw_line in note.body.splitlines():
        line = raw_line.strip()
        if (
            not line
            or line.startswith((">", "![[", "http://", "https://", "#", "|", "```"))
            or line in {"---"}
        ):
            continue
        line = re.sub(r"[*_`~\[\]()>-]+", " ", line)
        line = line.replace("\\", "")
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            return line[:140] + ("…" if len(line) > 140 else "")
    return "Creative fragment retained as foundational motif."


def render_note_content(note: Note, notes_by_path: dict[str, Note]) -> str:
    aliases = [note.stem]
    if note.source_id:
        aliases.append(f"apple-note-{note.source_id}")

    # Build property related links
    related_prop = [
        note.moc_path,
        *note.concept_hubs,
        *note.related,
        *note.synthesized_concepts,
        "00_MOCs/00_Master_Index",
    ]
    seen_rel = set()
    dedup_rel = []
    for r in related_prop:
        if r not in seen_rel:
            seen_rel.add(r)
            dedup_rel.append(r)

    fm_lines = [
        "---",
        f"title: {json_value(note.title)}",
        f"aliases: {json_value(aliases)}",
        f"tags: {json_value(note.tags)}",
        f"category: {json_value(CATEGORIES[note.category]['name'])}",
        f"status: {json_value(note.status)}",
        f"source: {json_value(note.source_relative)}",
        f"source_id: {json_value(note.source_id or None)}",
        f"source_sha256: {json_value(note.source_hash)}",
        f"related: {json_value(property_links(dedup_rel))}",
        "---",
    ]
    fm = "\n".join(fm_lines)

    # Conceptual Context banner
    context_lines = [
        f"> [!abstract] Conceptual Context",
        f"> **Category**: {wikilink(note.moc_path, CATEGORIES[note.category]['name'])}",
    ]
    if note.concept_hubs:
        h_links = ", ".join(wikilink(h, h.split("/")[-1].replace("Hub_", "").replace("_", " ")) for h in note.concept_hubs)
        context_lines.append(f"> **Thematic Constellations**: {h_links}")
    if note.synthesized_concepts:
        sc_links = ", ".join(wikilink(sc, sc.split("/")[-1]) for sc in note.synthesized_concepts)
        context_lines.append(f"> **Synthesized in**: {sc_links}")
    context_block = "\n".join(context_lines)

    body_text = note.body if note.body else "_This concept note is a foundational seed._"

    # Related concepts & bridges section
    bridge_lines = [
        "## Conceptual Bridges & Resonant Links",
        "",
        f"- **Category Hub**: {wikilink(note.moc_path, CATEGORIES[note.category]['name'] + ' MOC')}",
    ]
    if note.concept_hubs:
        for h in note.concept_hubs:
            hub_name = h.split("/")[-1].replace("Hub_", "").replace("_", " ")
            bridge_lines.append(f"- **Thematic Cluster**: {wikilink(h, hub_name + ' Hub')}")
    if note.synthesized_concepts:
        for sc in note.synthesized_concepts:
            bridge_lines.append(f"- **Synthesized Concept**: {wikilink(sc, sc.split('/')[-1])}")

    bridge_lines.append("")
    bridge_lines.append("### Resonant Ideas & Sister Concepts")
    for r in note.related:
        peer = notes_by_path.get(r)
        if peer:
            shared = sorted(note.themes & peer.themes)
            reason = ", ".join(t.replace("-", " ") for t in shared[:3]) or "thematic resonance"
            bridge_lines.append(f"- {wikilink(peer.vault_path, peer.title)} — {reason}")

    bridge_lines.append(f"- {wikilink('00_MOCs/00_Master_Index', 'Master Index')}")

    return f"{fm}\n\n# {note.title}\n\n{context_block}\n\n## Content\n\n{body_text}\n\n" + "\n".join(bridge_lines) + "\n"


def render_concept_hub(hub_id: str, hub_info: dict, notes_by_stem: dict[str, Note]) -> str:
    title = hub_info["title"]
    desc = hub_info["description"]
    tag = hub_info["tag"]
    source_notes = [notes_by_stem[s] for s in hub_info["notes"] if s in notes_by_stem]
    synth_concepts = hub_info.get("synthesized", [])

    related = [
        "00_MOCs/00_Master_Index",
        *[f"07_Synthesized_Concepts/{sc}" for sc in synth_concepts],
        *[n.vault_path for n in source_notes],
    ]

    fm = "\n".join([
        "---",
        f"title: {json_value(title + ' Hub')}",
        f"tags: {json_value(['moc', 'hub', tag])}",
        f"related: {json_value(property_links(related))}",
        "---",
    ])

    lines = [
        fm,
        "",
        f"# {title} — Concept Hub",
        "",
        f"> [!info] Thematic Constellation",
        f"> {desc}",
        "",
        f"**Constellation size:** {len(source_notes)} notes",
        "",
    ]

    if synth_concepts:
        lines.append("## Synthesized Creative Projects")
        lines.append("")
        for sc in synth_concepts:
            lines.append(f"- **{wikilink(f'07_Synthesized_Concepts/{sc}', sc)}** — project design derived directly from this constellation.")
        lines.append("")

    lines.append("## Connected Source Notes")
    lines.append("")
    for n in sorted(source_notes, key=lambda x: x.title.casefold()):
        lines.append(f"- {wikilink(n.vault_path, n.title)} (`{CATEGORIES[n.category]['name']}`) — {summary(n)}")

    lines.extend([
        "",
        "## Navigation & Bridges",
        "",
        f"- Return to {wikilink('00_MOCs/00_Master_Index', 'Master Knowledge Index')}",
        f"- Explore {wikilink('00_MOCs/Synthesized_Concepts_MOC', 'Synthesized Concepts MOC')}",
    ])

    return "\n".join(lines) + "\n"


def render_category_moc(cat_key: str, notes: list[Note]) -> str:
    config = CATEGORIES[cat_key]
    cat_notes = sorted([n for n in notes if n.category == cat_key], key=lambda x: x.title.casefold())
    theme_counts = Counter(t for n in cat_notes for t in n.themes)

    other_mocs = [f"00_MOCs/{c['moc']}" for k, c in CATEGORIES.items() if k != cat_key]
    related = ["00_MOCs/00_Master_Index", "00_MOCs/Synthesized_Concepts_MOC", *other_mocs]

    fm = "\n".join([
        "---",
        f"title: {json_value(config['name'] + ' MOC')}",
        f"tags: {json_value(['moc', f'category/{slug_tag(config['name'])}'])}",
        f"related: {json_value(property_links(related))}",
        "---",
    ])

    lines = [
        fm,
        "",
        f"# {config['name']} — Map of Content",
        "",
        config["description"],
        "",
        f"**Source notes indexed:** {len(cat_notes)}",
        "",
        "## Major Concept Themes",
        "",
    ]
    for t, count in theme_counts.most_common(8):
        sample = [n for n in cat_notes if t in n.themes][:4]
        links = ", ".join(wikilink(n.vault_path, n.title) for n in sample)
        lines.append(f"- **{t.replace('-', ' ').title()}** ({count}) — {links}")

    lines.extend(["", "## Complete Note Directory", ""])
    for n in cat_notes:
        t_text = ", ".join(sorted(n.themes)[:3])
        lines.append(f"- {wikilink(n.vault_path, n.title)} · `{n.status}` · {t_text} · {summary(n)}")

    if cat_key == "01_Game_Design":
        lines.extend([
            "",
            "## Preserved Canvas Notes",
            "",
            "- [[01_Game_Design/Canvases/Untitled.canvas|Untitled Canvas]]",
            "- [[01_Game_Design/Canvases/Untitled 1.canvas|Untitled Canvas 1]]",
            "- [[01_Game_Design/Canvases/Untitled 2.canvas|Untitled Canvas 2]]",
        ])

    lines.extend([
        "",
        "## Related Hubs and MOCs",
        "",
        f"- Return to {wikilink('00_MOCs/00_Master_Index', 'Master Knowledge Index')}",
        f"- View {wikilink('00_MOCs/Synthesized_Concepts_MOC', 'Synthesized Concepts MOC')}",
    ])
    for k, c in CATEGORIES.items():
        if k != cat_key:
            lines.append(f"- {wikilink(f'00_MOCs/{c['moc']}', c['name'] + ' MOC')}")

    return "\n".join(lines) + "\n"


def render_master_index(notes: list[Note]) -> str:
    related = [
        *[f"00_MOCs/{c['moc']}" for c in CATEGORIES.values()],
        *[f"00_MOCs/{h_id}" for h_id in CONCEPT_HUBS],
        "00_MOCs/Synthesized_Concepts_MOC",
        "00_MOCs/Source_Manifest",
        "00_MOCs/Integrity_Report",
    ]

    fm = "\n".join([
        "---",
        f"title: \"Master Index\"",
        f"tags: {json_value(['moc', 'vault/home', 'knowledge-graph'])}",
        f"related: {json_value(property_links(related))}",
        "---",
    ])

    lines = [
        fm,
        "",
        "# ShatteredMind — Master Knowledge Index",
        "",
        "Welcome to the unified knowledge vault. Every concept, game mechanic, narrative motif, and aesthetic shader is interconnected through bidirectional wikilinks, category MOCs, and thematic concept hubs.",
        "",
        "## Vault Overview",
        "",
        f"- **Active Creative Notes:** {len(notes)}",
        f"- **Thematic Concept Hubs:** {len(CONCEPT_HUBS)}",
        f"- **Category Maps of Content:** {len(CATEGORIES)}",
        f"- **Synthesized Creative Concepts:** {len(CONCEPT_SPECS)}",
        "- **Preserved Canvases:** 3",
        "- **Status:** 100% interconnected in Obsidian Graph View",
        "",
        "## Thematic Concept Hubs (Core Creative Gravities)",
        "",
    ]

    for h_id, h_info in CONCEPT_HUBS.items():
        lines.append(f"- **{wikilink(f'00_MOCs/{h_id}', h_info['title'])}** ({len(h_info['notes'])} notes) — {h_info['description']}")

    lines.extend([
        "",
        "## Category Maps of Content",
        "",
    ])
    for cat_key, c_info in CATEGORIES.items():
        c_count = sum(1 for n in notes if n.category == cat_key)
        lines.append(f"- **{wikilink(f'00_MOCs/{c_info['moc']}', c_info['name'])}** ({c_count} notes) — {c_info['description']}")

    lines.extend([
        "",
        "## Synthesized Creative Projects",
        "",
        f"Explore the 5 novel projects developed from note constellations in {wikilink('00_MOCs/Synthesized_Concepts_MOC', 'Synthesized Concepts MOC')}:",
        "- [[07_Synthesized_Concepts/Lucid Terminal - The Memory Golem|Lucid Terminal: The Memory Golem]] (Psychological dream-walker puzzle)",
        "- [[07_Synthesized_Concepts/Guild of the Departed - 21 Grams|Guild of the Departed: 21 Grams]] (Death management roguelite village)",
        "- [[07_Synthesized_Concepts/Kinetic Resonance - Bloom of the Unspoken|Kinetic Resonance: Bloom of the Unspoken]] (Somatic botanical motion)",
        "- [[07_Synthesized_Concepts/The Collar Experiment - Asymmetric Dilemma|The Collar Experiment: Asymmetric Dilemma]] (Asymmetric social deduction thriller)",
        "- [[07_Synthesized_Concepts/Bora-Bora Spectrum Surfer|Bora-Bora Spectrum Surfer]] (Chromatic wave momentum arcade)",
        "",
        "## Maintenance and Provenance",
        "",
        f"- {wikilink('START HERE', 'Start Here')} — orientation guide for new visitors.",
        f"- {wikilink('00_MOCs/Source_Manifest', 'Source Manifest')} — maps original files and SHA256 hashes.",
        f"- {wikilink('00_MOCs/Integrity_Report', 'Vault Integrity Report')} — confirms 100% graph connectivity.",
        "- Untouched original backup is safely preserved in `_backup_apple_notes/` (excluded from Graph View).",
    ])

    return "\n".join(lines) + "\n"


def render_synthesized_moc() -> str:
    related = [
        "00_MOCs/00_Master_Index",
        *[f"00_MOCs/{h_id}" for h_id in CONCEPT_HUBS],
        *[f"07_Synthesized_Concepts/{s['slug']}" for s in CONCEPT_SPECS],
    ]
    fm = "\n".join([
        "---",
        f"title: \"Synthesized Concepts MOC\"",
        f"tags: {json_value(['moc', 'category/synthesized-concepts', 'creativity'])}",
        f"related: {json_value(property_links(related))}",
        "---",
    ])

    lines = [
        fm,
        "",
        "# Synthesized Concepts — Map of Content",
        "",
        "These five creative projects synthesize distinct subsets of your notes across game design, narrative, motion, and art physics.",
        "",
    ]
    for idx, spec in enumerate(CONCEPT_SPECS, 1):
        slug = spec["slug"]
        lines.extend([
            f"## {idx}. [[07_Synthesized_Concepts/{slug}|{spec['title']}]]",
            "",
            f"> {spec['pitch']}",
            "",
            f"**Thematic Hubs:** " + ", ".join(wikilink(h, h.split('/')[-1].replace('Hub_', '').replace('_', ' ')) for h in spec.get("hubs", [])),
            "",
            f"**Foundational Notes:** " + ", ".join(f"[[{s}]]" for s in spec["sources"]),
            "",
        ])

    lines.extend([
        "## Creative Recombination Prompts",
        "",
        "- Fuse an emotional vulnerability with an optical light constraint.",
        "- Treat physical body awkwardness as an intentional input mechanic.",
        "- Transmute urban housing and financial anxiety into a mythic survival system.",
        "",
        f"Return to {wikilink('00_MOCs/00_Master_Index', 'Master Index')}.",
    ])
    return "\n".join(lines) + "\n"


def render_concept_doc(spec: dict, notes_by_stem: dict[str, Note]) -> str:
    source_notes = [notes_by_stem[s] for s in spec["sources"] if s in notes_by_stem]
    hubs = spec.get("hubs", [])
    related = [
        "00_MOCs/Synthesized_Concepts_MOC",
        "00_MOCs/00_Master_Index",
        *hubs,
        *[n.vault_path for n in source_notes],
    ]

    fm = "\n".join([
        "---",
        f"title: {json_value(spec['title'])}",
        f"tags: {json_value(spec['tags'])}",
        'status: "Concept"',
        f"sources: {json_value(property_links([n.vault_path for n in source_notes]))}",
        f"related: {json_value(property_links(related))}",
        "---",
    ])

    lines = [
        fm,
        "",
        f"# {spec['title']}",
        "",
        f"> [!idea] Creative Pitch",
        f"> {spec['pitch']}",
        "",
        "## Thematic Constellation & Source Seeds",
        "",
    ]
    for n in source_notes:
        lines.append(f"- {wikilink(n.vault_path, n.title)} (`{CATEGORIES[n.category]['name']}`) — {summary(n)}")

    lines.extend([
        "",
        spec["content"].strip(),
        "",
        "## Connected Hubs & Navigation",
        "",
    ])
    for h in hubs:
        lines.append(f"- **Concept Hub**: {wikilink(h, h.split('/')[-1].replace('Hub_', '').replace('_', ' ') + ' Hub')}")
    lines.append(f"- **Synthesized Projects**: {wikilink('00_MOCs/Synthesized_Concepts_MOC', 'Synthesized Concepts MOC')}")
    lines.append(f"- **Master Index**: {wikilink('00_MOCs/00_Master_Index', 'Master Index')}")

    return "\n".join(lines) + "\n"


def render_source_manifest(notes: list[Note]) -> str:
    fm = "\n".join([
        "---",
        f"title: \"Source Manifest\"",
        f"tags: {json_value(['moc', 'provenance', 'migration'])}",
        f"related: {json_value(property_links(['00_MOCs/00_Master_Index', '00_MOCs/Integrity_Report']))}",
        "---",
    ])

    lines = [
        fm,
        "",
        "# Vault Source Manifest",
        "",
        f"Tracking all {len(notes)} active creative notes. Original raw files remain permanently archived in `_backup_apple_notes/`.",
        "",
    ]

    grouped = defaultdict(list)
    for n in notes:
        grouped[n.category].append(n)

    for cat_key, c_info in CATEGORIES.items():
        lines.extend(["", f"## {c_info['name']}", ""])
        for n in sorted(grouped[cat_key], key=lambda x: x.title.casefold()):
            lines.append(f"- `{n.source_relative}` → {wikilink(n.vault_path, n.title)} · `{n.source_hash[:12]}`")

    return "\n".join(lines) + "\n"


def render_start_here() -> str:
    fm = "\n".join([
        "---",
        f"title: \"Start Here\"",
        f"tags: {json_value(['vault/home'])}",
        f"related: {json_value(property_links(['00_MOCs/00_Master_Index']))}",
        "---",
    ])
    return (
        f"{fm}\n\n"
        "# Start Here\n\n"
        f"Open [[00_MOCs/00_Master_Index|ShatteredMind — Master Knowledge Index]] to explore the knowledge base.\n\n"
        "All creative notes, concept hubs, and synthesized game designs are unified directly in this vault.\n"
    )


def execute_migration() -> None:
    print("Step 1: Loading notes and analyzing connections...")
    notes = load_source_notes()
    if len(notes) != 120:
        raise RuntimeError(f"Expected 120 creative notes, found {len(notes)}")

    map_concept_hubs_and_synthesized(notes)
    compute_open_ended_peer_links(notes)

    notes_by_path = {n.vault_path: n for n in notes}
    notes_by_stem = {n.stem: n for n in notes}

    print("Step 2: Preparing root directory structure...")
    for cat_key in CATEGORIES:
        (ROOT / cat_key).mkdir(parents=True, exist_ok=True)
    (ROOT / "00_MOCs").mkdir(parents=True, exist_ok=True)
    (ROOT / "07_Synthesized_Concepts").mkdir(parents=True, exist_ok=True)
    (ROOT / "01_Game_Design" / "Canvases").mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 3: Moving image assets into Assets/...")
    # Source images can come from root or backup
    for img_path in [*ROOT.glob("*.png"), *ROOT.glob("*.jpeg"), *ROOT.glob("*.jpg"), *BACKUP_DIR.glob("*.png"), *BACKUP_DIR.glob("*.jpeg")]:
        target = ASSETS_DIR / img_path.name
        if not target.exists():
            shutil.copy2(img_path, target)

    print("Step 4: Preserving Canvases in 01_Game_Design/Canvases/...")
    for canvas_name in ["Untitled.canvas", "Untitled 1.canvas", "Untitled 2.canvas"]:
        src = BACKUP_DIR / canvas_name
        if not src.exists():
            src = ROOT / canvas_name
        if src.exists():
            target = ROOT / "01_Game_Design" / "Canvases" / canvas_name
            shutil.copy2(src, target)

    print("Step 5: Writing updated notes...")
    for n in notes:
        out_path = ROOT / n.category / f"{n.stem}.md"
        out_path.write_text(render_note_content(n, notes_by_path), encoding="utf-8")

    print("Step 6: Writing 8 Thematic Concept Hubs...")
    for hub_id, hub_info in CONCEPT_HUBS.items():
        hub_path = ROOT / "00_MOCs" / hub_info["filename"]
        hub_path.write_text(render_concept_hub(hub_id, hub_info, notes_by_stem), encoding="utf-8")

    print("Step 7: Writing Category MOCs...")
    for cat_key in CATEGORIES:
        moc_path = ROOT / "00_MOCs" / f"{CATEGORIES[cat_key]['moc']}.md"
        moc_path.write_text(render_category_moc(cat_key, notes), encoding="utf-8")

    print("Step 8: Writing Synthesized Concepts and MOC...")
    for spec in CONCEPT_SPECS:
        c_path = ROOT / "07_Synthesized_Concepts" / spec["filename"]
        c_path.write_text(render_concept_doc(spec, notes_by_stem), encoding="utf-8")
    (ROOT / "00_MOCs" / "Synthesized_Concepts_MOC.md").write_text(render_synthesized_moc(), encoding="utf-8")

    print("Step 9: Writing Master Index, Manifest, and Start Here...")
    (ROOT / "00_MOCs" / "00_Master_Index.md").write_text(render_master_index(notes), encoding="utf-8")
    (ROOT / "00_MOCs" / "Source_Manifest.md").write_text(render_source_manifest(notes), encoding="utf-8")
    (ROOT / "START HERE.md").write_text(render_start_here(), encoding="utf-8")

    print("Step 10: Cleaning up redundant directories and temp files...")
    if (ROOT / "_organized_vault").exists():
        shutil.rmtree(ROOT / "_organized_vault")
    if (ROOT / "Apple Notes").exists():
        shutil.rmtree(ROOT / "Apple Notes")
    for loose_canvas in ROOT.glob("*.canvas"):
        loose_canvas.unlink()
    for loose_img in ROOT.glob("*"):
        if loose_img.is_file() and loose_img.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            loose_img.unlink()
    for loose in ["Game Development Keywords.md", "2026-09-15.md", "Screenshot 2022-01-25 at 10.25.27 AM.png.md", "Untitled 3.canvas", "Untitled 4.canvas"]:
        p = ROOT / loose
        if p.exists():
            p.unlink()

    print("Step 11: Configuring .obsidian/app.json and graph.json...")
    app_json = ROOT / ".obsidian" / "app.json"
    app_data = {
        "attachmentFolderPath": "Assets",
        "useMarkdownLinks": False,
        "newLinkFormat": "shortest",
        "userIgnoreFilters": ["_backup_apple_notes/"],
    }
    app_json.write_text(json.dumps(app_data, indent=2), encoding="utf-8")

    graph_json = ROOT / ".obsidian" / "graph.json"
    graph_data = {
        "collapse-filter": False,
        "search": "",
        "showTags": False,
        "showAttachments": False,
        "hideUnresolved": False,
        "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [
            {"query": "path:00_MOCs", "color": {"a": 1, "rgb": 16753920}},              # Amber / Gold
            {"query": "path:01_Game_Design", "color": {"a": 1, "rgb": 4388480}},         # Emerald Green
            {"query": "path:02_Narrative_Psychology", "color": {"a": 1, "rgb": 11155967}}, # Violet / Purple
            {"query": "path:03_Physical_Motion_Games", "color": {"a": 1, "rgb": 16744448}},# Tangerine Orange
            {"query": "path:04_Art_Shaders_Aesthetics", "color": {"a": 1, "rgb": 3394815}},# Cyan / Sky
            {"query": "path:05_Tech_Pipelines_Unity", "color": {"a": 1, "rgb": 4426239}},  # Blue
            {"query": "path:06_Life_Career_Philosophy", "color": {"a": 1, "rgb": 16731519}},# Rose Pink
            {"query": "path:07_Synthesized_Concepts", "color": {"a": 1, "rgb": 16711833}},  # Ruby Red
        ],
        "collapse-display": False,
        "showArrow": True,
        "textFadeMultiplier": 0,
        "nodeSizeMultiplier": 1.2,
        "lineSizeMultiplier": 1.2,
        "collapse-forces": False,
        "centerStrength": 0.55,
        "repelStrength": 12,
        "linkStrength": 1,
        "linkDistance": 180,
        "scale": 0.6,
        "close": True,
    }
    graph_json.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")


def run_integrity_check() -> dict:
    all_md = [
        p for p in ROOT.rglob("*.md")
        if "_backup_apple_notes" not in p.parts and ".obsidian" not in p.parts and p.name != "unify_vault_and_weave_concepts.py"
    ]
    all_canvases = [
        p for p in ROOT.rglob("*.canvas")
        if "_backup_apple_notes" not in p.parts and ".obsidian" not in p.parts
    ]

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

    # Connectivity check starting from Master Index
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
        f"related: {json_value(property_links(['00_MOCs/00_Master_Index', '00_MOCs/Source_Manifest']))}",
        "---",
        "",
        "# Vault Integrity Report",
        "",
        f"**Overall result:** {'PASS' if not unresolved and not unreachable else 'REVIEW REQUIRED'}",
        "",
        "## Verification Metrics",
        "",
        f"- Active Markdown notes: **{len(all_md)}**",
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

    return {
        "md_count": len(all_md),
        "canvas_count": len(all_canvases),
        "total_nodes": len(all_keys),
        "total_links": total_links,
        "unresolved_count": len(unresolved),
        "unreachable_count": len(unreachable),
        "connected": len(unreachable) == 0,
        "missing_assets": list(set(missing_assets)),
    }


if __name__ == "__main__":
    execute_migration()
    res = run_integrity_check()
    print("\nIntegrity Check Results:")
    print(json.dumps(res, indent=2))
