# Eclipse: The Last Kingdom — technical assessment

This document describes how the game is built, where new systems plug in, and the plan for the "Ultimate JRPG Enhancement" work, with the status of each phase.

## 1. Architecture

The whole game is one static file, `eclipse.html`: CSS, markup and a single classic `<script>`. There is no build step, no dependencies and no asset files; every sprite, tile, portrait, background and sound is generated at runtime. Vercel serves it as a static site (`vercel.json` rewrites `/` to `/eclipse.html`).

The script is organised in layers, top to bottom:

| Layer | What lives there | Key names |
| --- | --- | --- |
| Core | maths, noise, colour helpers, `Store` (localStorage with try/catch), settings | `mulberry32`, `fbm`, `shade`, `Store`, `settings` |
| Audio | Web Audio synth for effects and generative music | `AudioSys.play`, `Music.play`, `TRACKS` |
| Input | keyboard, mouse, gamepad, touch; actions with rebindable bindings | `Input`, `ACTIONS`, `DEF_BIND` |
| Art | procedural tiles, trees, icons, houses; humanoid sprite builder; portrait painter | `genTiles`, `buildSprite`, `drawHumanoid`, `paintPortrait`, `getPortrait` |
| Data | items, enemies, classes, skills, quests, NPCs, heroines, outfits | `ITEMS`, `ENEMY`, `CLASSES`, `QUESTS`, `NPCDEF`, `HEROINES`, `OUTFITS` |
| Maps | tile maps built from noise plus hand placement | `buildVillage`, `buildForest`, `buildCaverns`, `buildMeadow`, `newMap` |
| Entities | `Player`, `Enemy` and boss subclasses, `NPC`, `Companion` | `Player.prototype.update/draw`, `Boss`, `Grukk`, `Sentinel`, `Sovereign` |
| State | the global `G` object: map, entities, particles, flags, quests, relationships, guild | `G` |
| Loop | fixed 60 Hz `update`, then `render`, `hudUpdate`, `Music.update` | `frame`, `update`, `render` |
| UI | HUD, codex tabs, shop, dialogue/visual-novel layer, menus, creation, wardrobe | `hudUpdate`, `renderCodex`, `Dlg`, `Scene`, `openGen` |
| Persistence | `serialize` / `startFrom` / `saveGame`, three slots plus `.bak` backups | `eclipse.slot.N` |

### The extension pattern

Later features are added as **wrapper layers** appended before `boot()`. Each layer keeps a reference to the previous function and calls it:

```js
const _update10 = update;
update = function (dt) { /* before */ _update10(dt); /* after */ };
```

Because the original code calls these functions by their global names, every caller picks up the newest layer. This is how the game has grown without rewriting working code, and it is the rule for future work: **extend, never replace**.

## 2. Integration points

| Need | Hook |
| --- | --- |
| Clothing, armor and hair on sprites | `gearPass(P, S, layer, k)` runs inside `buildSprite` at four layers: `back`, `legs`, `body`, `top` |
| Portrait clothing and hair | `portraitBack`, `portraitFront`, `hairBackX`, `hairFrontX`, `portraitBangs` inside `paintPortrait` |
| Look → sprite palette / portrait spec | `lookPal(cls, look)` and `lookFace(cls, look)` |
| Overlay effects in world space | `fx2(...)` list drawn by the `render` layer above lighting |
| Slow motion, letterbox, banners | `G.slowT`, `cinematic(ms)`, `banner(main, sub)` |
| New maps | wrap `buildWorld`; maps join `G.maps` and are saved automatically (explored masks) |
| New enemies | add to `ENEMY`, draw via `NEWDRAW` in the `Enemy.prototype.draw` layer, list in `BEASTS` |
| Quests | `QUESTS` entry, `qStart` / `qSet` / `qDone`, progress through `qProg` and `onKill` layers |
| Saving new state | add to the `serialize` layer, read it back in the `startFrom` layer with defaults |

## 3. Risks and constraints

- **Single file size.** The file is about 470 KB. It loads instantly as static content, but each layer must stay compact.
- **Wrapper order matters.** A layer only sees layers defined before it. New layers go at the end, just before `boot()`.
- **Sprite caching.** Sprites are cached by palette identity (`palId`). Anything that changes a look must produce a new palette object (`applyLook()` clears the player's cache).
- **Save compatibility.** Every new field needs a default in the `startFrom` layer. Saves carry `v` and a `.bak` copy.
- **Background tabs.** Browsers pause `requestAnimationFrame` in hidden tabs; the game simply pauses there.

## 4. Phase plan and status

### Phase 1 — Core polish
Done in this pass:
- Smooth acceleration and deceleration, running lean, running dust (earlier pass).
- Idle look-around, low-health exhaustion breath, victory pose after a boss falls.
- Heavy attacks by holding attack, different for each weapon: sword ground slam, knife dash strike, staff arcane burst.
- Weapon identity on light attacks: knives swing faster; a staff's third hit fires an arcane bolt.
- Perfect dodge (slow motion, burst gain) and perfect parry → counter-attack.
- Ultimates: screen dimming, letterbox, class-coloured shockwaves and beams, slow-motion finish and a damage summary.
- Moving cloud shadows on outdoor maps.

Next: dedicated bow draw and release, more idle variations (stretch, weapon adjust), sitting and sleeping poses, animated grass and water reflections.

### Phase 2 — Living world
Done: NPC daily routines (morning at home, working hours at their posts, evenings together in the plaza, indoors at night and in heavy rain).
Next: NPCs talking to each other, benches and eating, festival crowds and mini-games, seasonal effects, more exploration and secret areas.

### Phase 3 — Relationships
Done: ten display stages derived from the saved seven-step status, so no migration is needed; a progress track in the Bonds tab; five new date places (flower garden, lakeside, picnic, stargazing, evening walk) with three choices each; a first-kiss scene; seasonal anniversaries; married routines, shared meals, evenings, goodnights and gifts; companion greetings, reactions, banter and treasure-spotting.
Next: more group scenes, family events, companion idle animations.

### Phase 4 — Story and content
Done: a new opening map, Dawnmeadow, with a starter quest that leads to Eldoria; Guild elite hunts and rank progression from F to S.
Next: story cinematics for key beats, optional dungeons, secret bosses, weekly challenges.

### Phase 5 — Technical polish
Done: save version field, automatic `.bak` backup on every save, graceful recovery from a damaged save, a Screen effects setting (Full / Reduced, defaulting to Reduced when the system asks for reduced motion), a separate ambience volume.
Next: particle pooling and a full mobile layout pass.
