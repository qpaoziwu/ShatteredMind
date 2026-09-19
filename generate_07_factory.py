#!/usr/bin/env python3
"""
ShatteredMind: 07_Factory Generator
Populates 07_Factory with 100 fully synthesized prototype cards.
"""

import os
from pathlib import Path

FACTORY_DIR = Path("07_Factory")
FACTORY_DIR.mkdir(parents=True, exist_ok=True)

# Catalog definitions (IDs 001 - 100)
CARDS = [
    # Hub 1 & 2
    ("PROTO-2026-001", "The 21-Gram Balance (廿一克的殘局)", "Hub_Soul_Economies_and_Lifecycles", "21 Grams Weight of a Soul", "Captured chess pieces transfer their 21g soul weight, tilting the physical board into the abyss."),
    ("PROTO-2026-002", "The Halogen Curfew (水銀燈下的宵禁)", "Hub_Optical_Shaders_and_Light", "Environmental Storytelling Through Light Ownership", "Holding the lantern alters physical geometry; unlit areas remain ethereal under sodium streetlamps."),
    ("PROTO-2026-003", "Saccharine Overdraft (糖分透支)", "Hub_Modular_Toy_Mechanics", "Candy Value Deduction and Sugar Rush", "Consuming candy grants speed and weapon multipliers but fills a lethal toxicity gauge."),
    ("PROTO-2026-004", "Bloom of the Distant (隔閡之花)", "Hub_Somatic_Movement_and_Connection", "Watercolor Mechanics Game Metaphor", "Maintaining exact rhythmic distance between two growing botanical stems prevents wilting on parchment."),
    ("PROTO-2026-005", "The Memory Golem's Alarm (記憶魔像的發條)", "Hub_Dreams_and_Memory", "Memory Golem and Dream Entity Network", "Feeding memory remnants to a bedside golem extends the 3 AM timer but scales up room furniture to giant size."),
    ("PROTO-2026-006", "Nocturnal Amnesia Sweep (忘卻黎明)", "Hub_Dreams_and_Memory", "Nocturnal Amnesia Village Curse", "Guide villagers to build defensive monuments before sleep resets their memories at dawn."),
    ("PROTO-2026-007", "The 3 AM Sloth Companion (三點鐘樹懶)", "Hub_Dreams_and_Memory", "The Resting Game and Emotional Geometry", "Sluggish platformer where muscle action is delayed by emotional geometry and exhaustion."),
    ("PROTO-2026-008", "Cognitive Memory Barrier (記憶超載壁)", "Hub_Dreams_and_Memory", "Cognitive Memory Capacity Barrier", "Gathering universal truths blocks personal memory slots; you must purge memories to fit keys."),
    ("PROTO-2026-009", "Buzzing Tool Chained Room (痙攣之榻)", "Hub_Dreams_and_Memory", "Buzzing Tool Chained Room", "Nightmare horror loop where rhythmic somatic breathing counters phantom tool vibrations."),
    ("PROTO-2026-010", "Rewind Cupboard 1980 (重疊壁櫥)", "Hub_Dreams_and_Memory", "Sea Lion Room and 80s HK Rewind Cupboard", "Stepping through a kitchen cupboard rewinds the estate to 1985; assets decompose if brought back."),
    ("PROTO-2026-011", "The Red Button Loop (紅鈕死循環)", "Hub_Dreams_and_Memory", "Red Button Micro-Loop Puzzle", "Breaking a room-reset loop requires finding the single microscopic tactile pressure variance."),
    ("PROTO-2026-012", "Daytime Override (晝夢覆蓋)", "Hub_Dreams_and_Memory", "Sleep, Memory, and Creative Continuity", "Nightmares leave terrain scars on the daytime map that must be paved over before sundown."),

    # Hub 2: Optical Physics & Light
    ("PROTO-2026-013", "Prism Break Platforms (稜鏡裂解)", "Hub_Optical_Shaders_and_Light", "Crystal Light Platform World", "Shining flashlights through rotating crystals splits light into solid chromatic platforms."),
    ("PROTO-2026-014", "Wavelength Blood Absorption (波長血噬)", "Hub_Optical_Shaders_and_Light", "Color as Wavelength Light Absorption", "Deep sea blood is green; underwater creatures absorb specific light spectrums to become invisible."),
    ("PROTO-2026-015", "CRT Phosphor 4-Switch (四維顯像管)", "Hub_Optical_Shaders_and_Light", "CRT Phosphor 4-Perspective Switch", "Puzzler toggling between 4 phosphor scanline perspectives to reveal hidden conduits."),
    ("PROTO-2026-016", "Watercolor Fiber Bleed (水墨滲透)", "Hub_Optical_Shaders_and_Light", "Watercolor Mechanics Game Metaphor", "Rules are linework; ink spreads across paper fibers, creating dynamic fluid bridges."),
    ("PROTO-2026-017", "Black Supernova Transition (黑超新星)", "Hub_Optical_Shaders_and_Light", "Black Supernova and Diffused Light Transitions", "Lighting inverts from 3D volumetric to 2D graphic silhouettes upon sensory flash."),
    ("PROTO-2026-018", "Fractal UV Labyrinth (分形緯線)", "Hub_Optical_Shaders_and_Light", "Fractal UV Shaders", "Navigating a geometry where texture coordinates recursively repeat into infinity."),
    ("PROTO-2026-019", "Filmstrip Screen Burn (膠卷灼痕)", "Hub_Optical_Shaders_and_Light", "Filmstrip Reel Screen Burn Mechanic", "Leaving a projector beam focused on a puzzle too long burns through the game screen permanently."),
    ("PROTO-2026-020", "Twilight Orb Transformation (暮光皮影)", "Hub_Optical_Shaders_and_Light", "Bedroom Twilight Orb Adventure", "Toggling bedside ambient lamps morphs domestic shadow cutouts into hostile shadow entities."),
    ("PROTO-2026-021", "Tidal Keyboard Acoustics (潮汐琴鍵)", "Hub_Optical_Shaders_and_Light", "Acoustic Physics and 3D Wave Visualization", "Acoustic ocean physics where soundwaves project dynamic 3D water topography."),
    ("PROTO-2026-022", "Polarized Dual-Tint Shadows (偏振雙色影)", "Hub_Optical_Shaders_and_Light", "Prohibition of Pure White and Black", "Strict avoidance of #000000; shadows split into indigo and sodium yellow paths."),
    ("PROTO-2026-023", "Match Flare Relativity (一瞬星系)", "Hub_Optical_Shaders_and_Light", "Match Flare Galaxy Relativity", "The level exists inside the strike of a single match; time moves at an imperceptible crawl."),
    ("PROTO-2026-024", "Mesh Worming Pulses (蛹動網格)", "Hub_Optical_Shaders_and_Light", "Asynchronous Rhythm Mesh Worming", "Wireframe lines crawl asynchronously; rhythm pulses eliminate meshes on every 4th beat."),
    ("PROTO-2026-025", "Rotating Acrylic Mirror Box (多面鏡盒)", "Hub_Optical_Shaders_and_Light", "Rotating Compartment Mystery Box", "Shifting perspective angles of acrylic boxes to reflect or vanish trapped souls."),

    # Hub 3: Soul Economies
    ("PROTO-2026-026", "Death's Adventurer Guild (死神工會)", "Hub_Soul_Economies_and_Lifecycles", "21 Grams Weight of a Soul", "Death runs a guild, deliberately sending adventurers on doomed quests to collect soul harvest bounties."),
    ("PROTO-2026-027", "Ghosts in Defeatable Hats (戴帽之魂)", "Hub_Soul_Economies_and_Lifecycles", "Ghosts Wearing Defeatable Hats", "Whimsical purgatory where wandering ghosts drop enchanted headwear upon comedic defeat."),
    ("PROTO-2026-028", "Unit Death ROI (殉職紅利)", "Hub_Soul_Economies_and_Lifecycles", "Unit Death Return on Investment", "Economic sim where worker units only pay out financial yields at the exact moment of their death."),
    ("PROTO-2026-029", "The Biological Action Loop (生滅循環)", "Hub_Soul_Economies_and_Lifecycles", "Biological Lifecycle Action Loop", "Cadence loop: Birth > Rest > Consume > Train > Action; skipping Rest causes cellular degradation."),
    ("PROTO-2026-030", "Earthbound Metal Chains (地縛重鏈)", "Hub_Soul_Economies_and_Lifecycles", "Earthbound Chains vs Weightless Youth", "Metaphysical puzzle where elders drag heavy iron chains while youth drift upward weightlessly."),
    ("PROTO-2026-031", "Retiring Dungeon Guards (卸甲地牢)", "Hub_Soul_Economies_and_Lifecycles", "Magic Dungeon Guard Trust and Retirement", "Befriending and repairing the armor of neglected skeleton guards so they can retire to farm."),
    ("PROTO-2026-032", "Tiered Magic Landscapes (地質階層魔法)", "Hub_Soul_Economies_and_Lifecycles", "Tiered Magic Terrain", "Geological ground tiers dictate the maximum spell tier invokeable; combat requires shaping soil."),
    ("PROTO-2026-033", "Environmental Death Factors (隱性死因)", "Hub_Soul_Economies_and_Lifecycles", "Environmental Death Factor Accumulation", "Latent environmental toxicity points accumulate invisibly until triggering sudden-death rules."),
    ("PROTO-2026-034", "Divine Bargaining Night (夜半神祇交易)", "Hub_Soul_Economies_and_Lifecycles", "Soul Harvesting and Divine Bargaining Economy", "Harvesting dead villagers at midnight to barter with dark gods for tomorrow's weather."),
    ("PROTO-2026-035", "Draw Pile Sudden Death (棄牌終局)", "Hub_Soul_Economies_and_Lifecycles", "Draw Pile Sudden Death and Discard Hand End Game", "Deckbuilder where every card played permanently shrinks the physical life pool."),
    ("PROTO-2026-036", "Seasonal Flu Nerfs (流感季的削弱)", "Hub_Soul_Economies_and_Lifecycles", "Systemic Combat Friction and Flu Seasons", "Seasonal climate waves inflict mechanical friction and attack latency on all factions."),
    ("PROTO-2026-037", "The Corporate Life-Force Bank (壽命實體化)", "Hub_Soul_Economies_and_Lifecycles", "Purchasable Power Corporate Finance", "Corporate finance game where currency is literal seconds subtracted from your life expectancy."),

    # Hub 4: Asymmetric Social Friction
    ("PROTO-2026-038", "The Collar Countdown (項圈倒數)", "Hub_Asymmetric_Social_Play", "Killer game", "4 innocents trapped in a room with explosive collars; one is the silent trigger holder."),
    ("PROTO-2026-039", "Underground Casino Cheating (千局地下城)", "Hub_Asymmetric_Social_Play", "Underground Casino and Cheating Mechanics", "RPG where honest play guarantees defeat; mechanics center on sleight-of-hand and bluffing."),
    ("PROTO-2026-040", "Scene Jumping in the Book (書界折躍)", "Hub_Asymmetric_Social_Play", "Scene Jumping and Book Object Extraction", "Pulling physical props out of literary chapters to resolve obstacles in the real room."),
    ("PROTO-2026-041", "Deceptive Military Chess (虛妄沙盤)", "Hub_Asymmetric_Social_Play", "Deceptive Military Chess - Spying, DDoS, Shelling", "Cyberwarfare chess featuring radar spoofing, fake troop signals, and communications jamming."),
    ("PROTO-2026-042", "Poison Potion Roulette (毒蠱合劑)", "Hub_Asymmetric_Social_Play", "Potion Brewing Poison Roulette", "Cooperative alchemy where brewing powerful elixirs has an escalating chance to blind your ally."),
    ("PROTO-2026-043", "Systemic Doubt Sabotage (質疑之錘)", "Hub_Asymmetric_Social_Play", "Institutional Doubt System Sabotage", "Verbally expressing distrust in a machine mechanic actively weakens its physics integrity."),
    ("PROTO-2026-044", "Virtual Room Sheep Voting (困獸強製票選)", "Hub_Asymmetric_Social_Play", "Virtual Room Interactive Items and Social Chaos", "Social toy where players deploy force pads and forced-vote sheep to derail peer meetings."),
    ("PROTO-2026-045", "Inverted Group Vision (聚散視野)", "Hub_Asymmetric_Social_Play", "Group Vision and Tactical Range", "Team visibility radius shrinks as players cluster; separating grants omniscient vision."),
    ("PROTO-2026-046", "The Asymmetric Outlier (背叛者契約)", "Hub_Asymmetric_Social_Play", "Asymmetric Outlier Challenge", "A cooperative dungeon crawl where one player can secretly accept an outlier pact to turn 1-vs-All."),
    ("PROTO-2026-047", "Timed Document Laser Evasion (檔案掃描陣)", "Hub_Asymmetric_Social_Play", "Timed Document Laser and Ping-Pong Ghost Escape", "Stealth puzzle dodging sweeping red legal lasers while stamping identity papers."),
    ("PROTO-2026-048", "Democracy Bingo (多數決陷阱)", "Hub_Asymmetric_Social_Play", "Democracy Bingo and Systemic Game Rules", "Social board game where majority votes trigger chaotic, mutually assured destruction rules."),
    ("PROTO-2026-049", "Knife Block & Disarm (雙刃脫手)", "Hub_Asymmetric_Social_Play", "Knife Combat Duel - Block and Disarm", "High-stakes duel where perfectly timed blocks fling both players' weapons across the arena."),
    ("PROTO-2026-050", "Beneficial Detection (被捕的紅利)", "Hub_Asymmetric_Social_Play", "Asymmetric Outlier Challenge", "Evasion game where deliberately letting specific enforcers catch you yields rare contraband."),

    # Hub 5: Wave Dynamics
    ("PROTO-2026-051", "Bora-Bora Spectrum Surfer (波拉波拉光譜衝浪)", "Hub_Wave_Dynamics_and_Momentum", "Bora-Bora Spectrum Surfer", "Pumping cadence along oceanic A-frame breaks while absorbing colored swell lines."),
    ("PROTO-2026-052", "Two-Surfer Wave Crash (同浪共墜)", "Hub_Wave_Dynamics_and_Momentum", "Two-Player Wave Crash Mechanics", "Competitive surfing where sharing the same reef break causes both players to plunge to the seabed."),
    ("PROTO-2026-053", "Seabed Topography Break (礁石、砂礫與斷層)", "Hub_Wave_Dynamics_and_Momentum", "Seabed Bottom Ecology - Reef, Stone, Sand", "Dynamic sea bottom topography (Reef, Stone, Sand) shifting wave steepness and wipeout damage."),
    ("PROTO-2026-054", "Card-Driven Wave Cadence (浪潮卡牌組)", "Hub_Wave_Dynamics_and_Momentum", "Card-Driven Wave Movement Combo", "Turn-based surf mechanics balancing paddle timing against unpredictable ocean swells."),
    ("PROTO-2026-055", "Momentum Storage Rebound (動能蓄積彈射)", "Hub_Wave_Dynamics_and_Momentum", "Momentum Storage and Kinetic Release", "Absorbing kinetic impacts into surfboard rails to slingshot into aerial combo rotations."),
    ("PROTO-2026-056", "Pins, Wires & Breaking Bonds (斷線針輪)", "Hub_Wave_Dynamics_and_Momentum", "Pins, Wires, and Bond-Breaking Mechanics", "Tactile pinball puzzle where stretching electrical wires past elastic tension snaps platforms."),
    ("PROTO-2026-057", "Dark Sky Celestial Navigation (暗夜引力星圖)", "Hub_Wave_Dynamics_and_Momentum", "Dark Sky Exploration and Pacing Rewards", "Pacing down in near pitch-black waters to reveal faint gravitational currents."),
    ("PROTO-2026-058", "Water Wiggle Jelly Physics (果凍水波)", "Hub_Wave_Dynamics_and_Momentum", "Water Wiggle Vertex Shader", "Vertex displacement jelly water where wave velocity bounces characters between crests."),
    ("PROTO-2026-059", "Surfboard Tailoring Ratio (板型力學)", "Hub_Wave_Dynamics_and_Momentum", "Surfboard Equipment and High Fashion Economy", "Customizing rocker and rail thickness to survive heavy hydraulic barrels."),
    ("PROTO-2026-060", "Seashell Repair Economy (貝殼修復工坊)", "Hub_Wave_Dynamics_and_Momentum", "Sustainable Non-Speculative Surfing Economy", "Purging currency speculation; board repairs require trading authentic ocean salvage."),
    ("PROTO-2026-061", "Aerial Drop Air Combos (凌空迴旋)", "Hub_Wave_Dynamics_and_Momentum", "Wave Dynamics and Aerial Combos", "Launching off vertical wave lips to input skateboard-style trick combinations."),
    ("PROTO-2026-062", "Acoustic Wave Topography (聲波海嘯)", "Hub_Wave_Dynamics_and_Momentum", "Acoustic Physics and 3D Wave Visualization", "Visualizing subterranean acoustics into physical wave barriers that push the player."),

    # Hub 6: Somatic Movement
    ("PROTO-2026-063", "Player-as-Flower Leaning (向日之軀)", "Hub_Somatic_Movement_and_Connection", "Kinetic Resonance: Bloom of the Unspoken", "Somatic camera tracking where leaning your torso guides the stem toward shifting light."),
    ("PROTO-2026-064", "Physical Reach Extension Tools (異化延伸具)", "Hub_Somatic_Movement_and_Connection", "Reach Extension Physical Tools", "Assistive control puzzle utilizing physical extenders and optical magnifying lenses."),
    ("PROTO-2026-065", "Limited Mobility Toothbrush Rhythm (生活微律動)", "Hub_Somatic_Movement_and_Connection", "Limited Mobility Motor Rhythm Imitation", "Translating domestic repetitive rhythms into expressive game controls."),
    ("PROTO-2026-066", "Night Museum Freeze Pose (凝像潛步)", "Hub_Somatic_Movement_and_Connection", "Night in the Museum - Freeze Pose Escape", "Motion camera stealth: freezing in twisted statue postures before security lasers sweep."),
    ("PROTO-2026-067", "Arm Tilt Pinball Flippers (雙臂彈珠臺)", "Hub_Somatic_Movement_and_Connection", "Motion Pinball Machine - Arm Tilt Flippers", "Using arm angles as physical flipper triggers to launch heavy steel balls."),
    ("PROTO-2026-068", "Marshmallow Soap Barrier (軟糖捏塑與皂液防線)", "Hub_Somatic_Movement_and_Connection", "Marshmallow Kingdom", "Deforming squashy enemies by hand while rubbing surfaces to generate protective soap foam."),
    ("PROTO-2026-069", "Clap-to-Switch Control (合掌移軸)", "Hub_Somatic_Movement_and_Connection", "Color Switch - 2-Player Directional Puzzle", "Two-player puzzle: P1 controls X, P2 controls Y; physical claps instantly swap axis ownership."),
    ("PROTO-2026-070", "Vertical Punching Leaping Fish (躍水咬拳)", "Hub_Somatic_Movement_and_Connection", "Vertical Punching Leaping Fish", "Aquatic creatures leaping from below that clamp onto player fists until physically shaken off."),
    ("PROTO-2026-071", "Inverted Minion Escapism (小卒的沉重)", "Hub_Somatic_Movement_and_Connection", "Inverted Role Play - Minion and Pest Escape", "Playing an ultra-sluggish tower defense creep trying to avoid the hero's blade."),
    ("PROTO-2026-072", "Graphite Line Friction (石墨刻痕)", "Hub_Somatic_Movement_and_Connection", "Painting in watercolour and graphite", "Pressing too hard creates brittle lines; light touches produce featherweight movement paths."),
    ("PROTO-2026-073", "Social Communication Gaps (未言的間隔)", "Hub_Somatic_Movement_and_Connection", "Distance, Insecurity, and Human Bonds", "Visualizing interpersonal awkwardness through dynamic, elastic watercolor boundary fields."),
    ("PROTO-2026-074", "Awkwardness as Mass (拘謹之重)", "Hub_Somatic_Movement_and_Connection", "People’s ignorance creates trouble for ppl", "Player character gains physical mass and slower turn rates when surrounded by staring NPCs."),

    # Hub 7: Urban Claustrophobia & HK Identity
    ("PROTO-2026-075", "28th Floor Balcony Vertigo (廿八樓的俯瞰)", "Hub_Urban_Alienation_and_Identity", "Public Housing Perspectives and MTR Fisheye", "Public housing platformer where wind shears and gravity pull from the side of the building."),
    ("PROTO-2026-076", "MTR Fisheye Rush (地鐵魚眼鏡)", "Hub_Urban_Alienation_and_Identity", "Public Housing Perspectives and MTR Fisheye", "Navigating crowded subway transfers under extreme barrel distortion and social panic meters."),
    ("PROTO-2026-077", "The Circle Approval Trap (圈子認同圈)", "Hub_Urban_Alienation_and_Identity", "In-Group Approval Circle Paradox", "Gaining social approval to leave an in-group, only to find departure voids your points."),
    ("PROTO-2026-078", "Cantonese Nine Tones Voice Path (九聲階梯)", "Hub_Urban_Alienation_and_Identity", "Proximity Social Hangout Scaling", "Voice-controlled platformer where pitch elevation across Cantonese tones sculpts staircases."),
    ("PROTO-2026-079", "Nails on the Keyboard-Screen (釘於鍵盤之掌)", "Hub_Urban_Alienation_and_Identity", "nails to my hands on the keyboard-screen", "Rhythm survival: typing urgent rent checks to prevent the eviction bar from dropping."),
    ("PROTO-2026-080", "Subdivided Flat Grid (膛房空間格)", "Hub_Urban_Alienation_and_Identity", "Public Housing Perspectives and MTR Fisheye", "Puzzle packing oversized furniture into tiny Hong Kong rooms with zero wasted square inches."),
    ("PROTO-2026-081", "Delly Cyrus: Relentless Run (穿樓暴走)", "Hub_Urban_Alienation_and_Identity", "Delly Cyrus - Bullying and Running Narrative Seed", "Channeling school bullying trauma into infinite sprint acceleration through stairwells."),
    ("PROTO-2026-082", "The Giving Concrete Pillar (給予之柱)", "Hub_Urban_Alienation_and_Identity", "The Giving Tree Resource Motif", "Chipping away at the structural pillar of your own flat to sell building materials for food."),
    ("PROTO-2026-083", "Chimp Department Store (猩猩百貨)", "Hub_Urban_Alienation_and_Identity", "Chimp Department Store - Mini-Employee Cards", "Melancholic shopping sim where placing consolation cards spawns miniature running clerks."),
    ("PROTO-2026-084", "Tibetan Bell & I Ching Roots (古鐘尋根)", "Hub_Urban_Alienation_and_Identity", "尋根", "Striking resonant singing bowls to clear spiritual noise in noisy high-density flats."),
    ("PROTO-2026-085", "Aristotle’s Hong Kong Telos (城中幸福論)", "Hub_Urban_Alienation_and_Identity", "Aristotle Eudaimonia and Ultimate Telos", "Measuring the intrinsic eudaimonia of daily chores against soul-draining corporate commute hours."),
    ("PROTO-2026-086", "Public Housing Laundry Swell (晾衣竿之陣)", "Hub_Urban_Alienation_and_Identity", "Public Housing Perspectives and MTR Fisheye", "Acrobatics swinging across bamboo laundry poles suspended over public housing atriums."),
    ("PROTO-2026-087", "Pretense of Pure Form (扮得純粹)", "Hub_Urban_Alienation_and_Identity", "扮得純粹", "Social stealth: matching pedestrian walk cadence and expressions to blend into crowds."),
    ("PROTO-2026-088", "Overheated V8 Engine Commute (人肉八缸引擎)", "Hub_Urban_Alienation_and_Identity", "Human V8 Engine and Highway School Metaphor", "Managing human engine temperature along a highway school commute where stopping is forbidden."),

    # Hub 8: Modular Toy Logic
    ("PROTO-2026-089", "Dual-Joint Stick Slinger (雙關節搖桿彈射)", "Hub_Modular_Toy_Mechanics", "Dual-Joint Direction Controller", "Input paradigm using nested dual-joint analog circles to aim and release kinetic projectiles."),
    ("PROTO-2026-090", "Hexagonal Floor Carpet (六角地毯控制器)", "Hub_Modular_Toy_Mechanics", "Hexagonal Carpet Input Controller", "Stepping between 6 tactile floor zones to command tactical skirmishes."),
    ("PROTO-2026-091", "Emergency Item Series (非常事態封印物)", "Hub_Modular_Toy_Mechanics", "Emergency Use Only Item Series", "Sealed absurdist equipment that breaks physics rules only during existential crises."),
    ("PROTO-2026-092", "Robo Marching Circus (機械行進樂隊)", "Hub_Modular_Toy_Mechanics", "Robo Marching Band Circus", "Automated brass automatons marching in synchronized formations, deflecting obstacles."),
    ("PROTO-2026-093", "Geometric Snap & Adhesive Glue (幾何卡榫與黏著物)", "Hub_Modular_Toy_Mechanics", "Geometric Surface Snapping and Adhesive Shapes", "Snapping polygon faces together at fixed rotational angles to build rolling physics contraptions."),
    ("PROTO-2026-094", "Mememe Mosquito Evasion (蚊鳴微閃)", "Hub_Modular_Toy_Mechanics", "Mememe Mosquito Audio-Visual Motif", "High-frequency mosquito hums indicating microsecond windows to execute perfect dodges."),
    ("PROTO-2026-095", "Reactive Gas Chambers (氣體連鎖化學室)", "Hub_Modular_Toy_Mechanics", "Player shoots gases to each other", "Shooting distinct pressurized gases at enemies to trigger combustions, freezing, or toxic levitation."),
    ("PROTO-2026-096", "Supply Chain Reverse Disassembly (逆向拆解堡壘)", "Hub_Modular_Toy_Mechanics", "Supply Chain Component Disassembly Game", "Dismantling complex defense turrets in exact reverse sequence under heavy enemy siege."),
    ("PROTO-2026-097", "Scrambled Health Bar UI (破碎血槽格鬥)", "Hub_Modular_Toy_Mechanics", "Scrambled Health Bar Combat", "Attacks physically shatter your UI health bar across the screen; damage halts in UI gaps."),
    ("PROTO-2026-098", "Mini Heavy 8-Ball Pool (超重八球論)", "Hub_Modular_Toy_Mechanics", "Mini Heavy Pool - 8-Ball Role Mechanics", "Billiards on high-friction felt where every numbered ball acts as an RPG class with special mass."),
    ("PROTO-2026-099", "9-Numpad Stat Synthesizer (九宮格數值熔爐)", "Hub_Modular_Toy_Mechanics", "9-Numpad Directional Stat Control", "Micro-strategy game using the numpad to merge lower character stats into elite tiers."),
    ("PROTO-2026-100", "Hype Meter & Release the Hound (激鬥村莊：放狗之掣)", "Hub_Modular_Toy_Mechanics", "Hype Meter and Release the Hound Button", "Balancing a village excitement gauge with an emergency button that releases wild guard beasts.")
]

TEMPLATE = """---
id: {id}
title: "{title}"
status: "Pitch"
folder: "07_Factory"
primary_hub: "[[00_MOCs/{hub}]]"
source_anchor: "[[01_Game_Design/{source}]]"
created: "2026-09-18"
tags: ["factory/prototype", "shattered-mind", "{id}"]
---

# Concept Brief: {title}

### 1. Creative Hook
{hook}

### 2. Core Interactive Loop
- **Input Model:** One-Touch / Mouse Gesture / Modular Stick
- **Juice Standard:** Dynamic camera kick, hit-stop on action triggers, procedural SFX.
- **Aesthetic Law:** Strict prohibition of `#000000` and `#FFFFFF`; dual-tint polarized shadows.

### 3. Component Assembly Manifest
- `{id}_CoreController.gd`
- `{id}_JuiceFeedback.gd`
- `{id}_ShaderPass.gdshader`

---
**Executive Action:**
- [ ] **[ GREENLIGHT TO PRODUCTION ]**
- [ ] **[ MUTATE / RE-ROLL ]**
- [ ] **[ REJECT TO ARCHIVE ]**
"""

for card_id, title, hub, source, hook in CARDS:
    file_path = FACTORY_DIR / f"{card_id}.md"
    content = TEMPLATE.format(
        id=card_id,
        title=title,
        hub=hub,
        source=source,
        hook=hook
    )
    file_path.write_text(content, encoding="utf-8")

print(f"Successfully populated {len(CARDS)} prototype cards into 07_Factory/!")