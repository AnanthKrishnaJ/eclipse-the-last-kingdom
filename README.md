# Eclipse: The Last Kingdom

A pixel-art action RPG in a single HTML file. Open `eclipse.html` in a browser to play; there is nothing to install or build. On Vercel, `vercel.json` serves the game at the site root.

## Story

It is 7:30 on a monsoon evening in Kakkanad, Kochi, and the office cab has just left Infopark without you. You can explore the street outside the Infopark gate in the rain. Drink chai at Chandran's stall, chat with the juice-shop owner and the security guard, haggle with an auto driver, and take a short lesson at the kalari. Then cross at the zebra crossing to the bus stop by Hotel Annapoorna. A gust tears a little girl's umbrella away, she runs into the road after it, and a private bus is coming. Whether you move in time is up to you.

You wake in a divine space before Aurelia, goddess of the dawn. What you say to her matters, and she offers you gifts: you choose your own powers from more than a hundred. Then you are reborn in the grass of Dawnmeadow with plain clothes and nothing else: no weapon, no armor, not a coin. Gather stones, branches, reeds and berries; fight with your fists or your powers; craft primitive tools. When you are ready, a merchant's cart carries you to Solmere, the city of the guilds. Register at the Adventurers' Guild, and the guildmaster sends you east to Eldoria, the last lit village, where the war against the eclipse begins.

## Features

- Six difficulty levels chosen before a new game: Easy, Normal, Hard, Extreme, Hell and Impossible. They change enemy health, damage and attack speed, experience and gold, healing, and Dawn's Grace. Impossible gives you one life: no revives, and dying erases the save.
- A playable Kerala opening in Kakkanad, outside Infopark: a monsoon evening with left-hand traffic that honks and brakes for you, metro construction on the median, a tea stall, a kalari, and ten people to talk to.
- Full outfit design before you start: design what you wear in Kochi and what you wake up in. Choose tops, sleeves, bottoms (including mundu, folded mundu and saree), shoes, outer layers, belts, headwear, accessories, patterns, and any colour. Start from 11 presets, undo and redo, save up to 12 designs to a library, and share designs as codes. Height and facial hair are new creation options, and the Wardrobe's Design studio lets you redesign in game.
- 112 divine powers in five categories (Elemental, Physical, Magical, Summoning, Special), across five rarities from Common to Divine. Each has its own cost, cooldown and limitation, and evolves at level 5. Choose three with seven soul points. Four hidden powers are earned through what you do in the opening. The selection screen has filters, search, side-by-side comparison and confirmation, and works on phones.
- Powers are real mechanics: bolts, beams, waves, meteors, gravity wells, time stop, teleports, barriers, buffs, healing, eleven kinds of summoned allies, copied techniques, and 45 passives that change stats, regeneration, evasion, loot, crafting and more. They level up with use and are saved with the game. Power slots use Z, X, C and V, or the round buttons on touch screens.
- A weaponless start: gather materials, craft a flint knife, club, staff, grass vest or food, and throw stones with bare hands. The first quest accepts either gathering or fighting.
- Solmere, the main city, where every building has its own architecture: the Adventurers' Guild hall is the largest and tallest, with a domed marble temple, a three-storey timber inn, a stone tavern, an apothecary tower, a clock-tower town hall, crenellated barracks, a brick bakery, a boutique with dress displays, an open-forge smithy and more. There is also an inn, a tavern, a grocer, a bakery, a clothier, a smithy and armory, an apothecary, a general store, a temple, a town hall, guard barracks, homes and a market plaza. Carts connect Dawnmeadow, Solmere and Eldoria.
- Real-time combat: three-hit combos, heavy attacks (hold attack) that differ per weapon, dodge rolls with perfect-dodge slow motion, parries that open a counter-attack, four skills, and ultimates with a cut-in, dimmed screen, slow-motion finish and damage summary.
- Adventurers' Guild: registration in Solmere, an adventurer card with ranks F to S and perks, bounties, named elite hunts with rewards, and a rank-gated Guild Shop.
- Dawnmeadow starting grassland with gathering spots, Meadow Puffs and Horn Beetles.
- Living village: NPCs keep daily routines and gather in the plaza in the evening.
- Three classes, Warden, Ranger and Arcanist, each with its own gear on the character.
- Armor shows on the character: tunic, leather, chainmail, wolfhide or full plate. Portraits change to match.
- Bag page laid out as an equipment screen (paper doll) with attributes, a 24-slot inventory, filters, sorting, hover tooltips and item comparison.
- Full character creation in tabs: name, gender, skin, eye colour and shape; 16 hairstyles, hair colour and headband; war paint, scars, glasses and earrings; outfit and coat dyes; and class. Live portrait, a turnable walking sprite and a randomizer.
- Classic JRPG interface: blue windows with silver edges, a pointing-hand cursor, a pause menu with icons and a hero status panel, a dialogue window with portrait, and a hero medallion on the HUD.
- The protagonist: messy black hair over dark eyes, a white shirt under a gold-trimmed black coat with red lining and long coat-tails, crossing leather straps, a red sash, a blue-gem pendant and tall gold-cuffed boots. Character creation can swap the coat for class gear.
- 16 hairstyles, from Messy and Wolf cut to Hime cut, Braid and Twin buns, each drawn for portraits and in-game sprites. Restyle any time at the Wardrobe's barber.
- Wardrobe: five cosmetic outfits (Protagonist Coat with coat, lining and trim dyes, Class Gear, Kerala Festival Wear, Royal Regalia, Nightstalker Cloak) and a show or hide armor toggle. Open it from the pause menu or your cottage.
- Lantern network: fast travel between any lanterns you have lit.
- Bestiary tab recording every monster you meet, with stats, tips and drops.
- Fully rebindable keyboard and mouse controls, up to three inputs per action.
- Companions Mimi, Lyra, Serah and Noelle, with Relationships 2.0: ten stages from Stranger to Married life, eight date locations with choices and consequences, first-kiss and anniversary scenes, gifts and personal quests.
- Married life: spouses keep daily routines, share meals and evenings at the cottage, say goodnight and leave small gifts.
- Companions greet you each day, react to rain, nightfall and danger, banter with each other and point out treasure.
- Adventurers' Guild bounties, a cottage with cooking, decorating and a garden, plus a day–night cycle, weather and seasons.
- Cinematic boss fights: letterboxed intros with roar shockwaves, glowing wind-ups, after-image trails on charges, leaps and blinks, impact craters, slow-motion phase changes with banners and phase pips, a shaking boss bar on hits, and a victory finisher with light pillars and shattering.
- Six areas, three bosses, side quests, a hidden quest, crafting, and New Game+.
- Three save slots kept in the browser with automatic backups and recovery, gamepad support and touch controls.
- Settings for music, effects and ambience volume, and a Reduced screen-effects mode.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the game is built and the phased improvement plan.

## Controls

All controls can be changed under Pause → Controls or Settings → Customize controls.

| Action | Default |
| --- | --- |
| Move / run | WASD or arrow keys, hold Shift to run |
| Attack, talk | Left click (toward the cursor), J or Space |
| Dodge / block | K / L or hold right click |
| Skills | 1–4 |
| Powers | Z, X, C, V |
| Burst | R |
| Potion | Q |
| Bag, skills, journal, map | I, T, O, M (powers and crafting are tabs in the same menu) |
| Pause | Esc |
