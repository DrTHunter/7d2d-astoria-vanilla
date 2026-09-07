# Astoria 8K — vanilla edition

The same Astoria 8K world as [my modded version](https://github.com/DrTHunter/7d2d-astoria-my-world),
but **no POI mods required**. Every building is still there — every Compopack POI, every Zeebark
house, all eight starter bases. They have just been rewritten to use only blocks that ship with the
game.

📍 **[Browse every POI on the interactive map →](https://drthunter.github.io/astoria-8k-poi-map/)**

| | |
|---|--:|
| POIs in the world | **13,095** |
| POI mods you need to install | **zero** |
| Starter bases, no zombies inside | **8** |

---

# Setup

Three steps. Nothing to manage, nothing to keep in sync with anyone else.

## 1. Install the base map

**[Astoria 8K — Full World Map](https://www.nexusmods.com/7daystodie/mods/7017)** (Nexus 7017,
**version 1.5.1**). Extract it so the files land here:

```
%APPDATA%\7DaysToDie\GeneratedWorlds\Astoria 8K\
```

Paste `%APPDATA%\7DaysToDie` into Explorer's address bar to get there. The folder must be named
exactly **Astoria 8K**.

## 2. Download this repo

Green **Code** button at the top of this page → **Download ZIP** → unzip it anywhere you like.

*(Or, if you have git: `git clone https://github.com/DrTHunter/7d2d-astoria-vanilla.git`)*

## 3. Run the installer

Open the unzipped folder and run:

```
python tools/install.py
```

It finds your game by itself, checks your Astoria files are the right version, **backs them up**,
patches the map, and installs the POI pack. If anything looks wrong it stops and changes nothing.

*(No Python? [python.org](https://www.python.org/downloads/) — tick **"Add Python to PATH"** during
install.)*

Then start a **new** game and pick **Astoria 8K**. You spawn in the prison yard.

> **An existing save won't show any of this.** The game bakes buildings into the ground the first
> time you visit an area. Start fresh.

### Undo

```
python tools/install.py --undo
```

Puts the original map back from the backups. To remove the POI pack, delete
`%APPDATA%\7DaysToDie\Mods\Astoria-Vanilla-POIs`.

Using Vortex? Drag `vortex/Astoria-Vanilla-POIs.zip` onto it instead and you get an on/off switch.

---

# How the conversion works

The map places **1,794** distinct prefabs. 813 are vanilla and the game already has them; the other
**981** came from nine mods and are bundled here, converted.

A prefab is three files that matter: `.tts` holds the block **geometry** as numeric ids,
`.blocks.nim` maps those ids to block **names**, and `.xml` holds the metadata. Because the geometry
only stores ids, **swapping a material is a change to the name table alone** — so the `.tts` is
never touched and every building keeps its exact shape, size and layout. Only what it is made of
changes.

Of the 981, only **89** used a non-vanilla block at all — between them, **603** distinct blocks.
The Compopack's 820 POIs, the bulk of the map, were already vanilla-only and needed nothing.

## How each of the 603 was mapped

| Method | Blocks |
|---|--:|
| Followed the block's own `Extends` chain to a vanilla block | 194 |
| Curated family rule — pictures, rugs, furniture, appliances… | 284 |
| Deliberately removed — vanilla has no equivalent | 119 |
| No rule matched → removed | 6 |

**1. The `Extends` chain.** Most modded blocks are declared as variations of a vanilla one, so the
author has already told you what it is. Following that chain gives exact answers:

```
MPL_SalmonBathtubClawFoot        -> decoClawFootBathTub
DesktopPCVLD                     -> decoComputerDeskTopPC
MPL_BookShelfDubBotFull01_Poof   -> cntBookShelfDoubleBottomFull01
ZBK_GoreBlockHumanCorpse1_Gurney -> goreBlockHumanCorpse1
```

**2. Family rules,** for blocks whose chain bottoms out at a custom model. Zeebark's 100 `ZBK_PP_*`
blocks all descend from `ZBK_PP_Picture01` — they are wall pictures, so they become
`pictureFrame_01a`. Around 41 wall-mounted weapon props become an empty gun rack. Rugs become
`rugBear`, couches `couchModernArm`, bicycles `bicycleStatic`.

**3. Removal, on purpose.** 125 blocks become air, and that is the honest answer for them: 65 are
wall stains, cracks, cutouts and torn wallpaper, 10 are graffiti, 14 are particle effects, 6 are
fallen trees. Vanilla has nothing that fills those roles.

### The rule that matters

**A decoration is never allowed to become something with gameplay behaviour.**

The obvious approach — match on the block's shape and material — produces
`ArcadeMachine01VLD → dartTrap` and `AreaRug10_1x4_Offset → cobweb`. That is a trap that shoots you
in an arcade, and a rug that slows you every time you walk over it. Both look right in a diff and
are wrong in the game.

So substitution targets are filtered against a blocklist of traps, spikes, cobwebs, barbed wire,
blades and the like, and anything that fails falls through to air. A missing rug beats a hidden
trap. The only exceptions are faithful ones: a modded blade trap does become `bladeTrap`, because
that is what it already was.

Every one of the 603 decisions is in [`docs/block-mapping.json`](docs/block-mapping.json).

## Sleeper volumes

Three Compopack sleeper groups had no vanilla equivalent and were renamed to the vanilla group they
were modelled on — `S_Zom_Janitor_Only → ZomJanitorOnly`, `S_Zom_HazMat_Only → ZomHazMatOnly`,
`ZomSnow → GroupGenericZombie`. Seven POIs affected.

Worth noting, since it cost me an hour: sleeper volume groups resolve against **`gamestages.xml`**,
not `entitygroups.xml`, and the gamestage number is part of the declared name — `1GroupGenericZombie`
is a real vanilla group, not a broken reference.

## Verification

The converted set was checked block by block:

- **0** block names outside vanilla `blocks.xml`, across all 981 prefabs
- **0** sleeper groups outside vanilla `gamestages.xml`
- **0** decorations mapped onto anything harmful

---

# What's in this repo

```
vortex/Astoria-Vanilla-POIs.zip   the 981 converted POIs, 13.9 MB
world-patch/                      the map changes: dtm.patch, prefabs.xml, spawnpoints.xml
tools/install.py                  applies them; --undo puts the stock map back
docs/                             the full write-up, and every block decision as JSON
```

453 MB of prefabs compress to 13.9 MB, because a `.tts` is mostly long runs of the same block id.

## Traders

**38 traders, and every town has one within a short walk.** Astoria shipped 24, but they were
distributed by the world generator rather than by town, so several towns had none at all and the
spawn city had two on opposite corners.

Astoria's own traders sit a median 66 m *outside* the town edge, on the approach road, and that is
the shape this follows — for each town without one, a clear, flat 60x60 patch 25–140 m beyond the
edge was scored on distance to the nearest road, how much cut and fill it needs, and whether it
faces the next town along. Every site chosen is on or beside a road; all but two need under a
metre of levelling. An existing town lot was the fallback, and never won.

Three traders that were already in the right place kept their spot and just got a better building.
All **14 distinct trader buildings** are now in use — the five vanilla ones, six of MPLogue's,
Zeebark's, and both of xcpv's settlements — so no two neighbouring towns look alike. Three have
deep basements (MPLogue's Wight bunker goes 31 blocks down), so those went to the sites with the
most ground under them; the shallowest trader still stands on 5 m of rock.

The spawn city gets a third, `trader_xcpv_Settlement_02_Viper7`, 266 m from where you wake up,
because the first walk was otherwise the better part of a kilometre.

Turn on the **Traders** layer on the [interactive map](https://drthunter.github.io/astoria-8k-poi-map/)
to see where they all are.

The full list, with teleport commands: [`docs/TRADERS.md`](docs/TRADERS.md).

## The eight starter bases

Cut out of existing POIs, with every sleeper volume stripped — nothing spawns inside, so they are
safe to move into on day one.

| Cut from | Name | Size |
|---|---|--:|
| `prison_01` | **StarterBase_Prison_Cellblock** — the map spawn is in its yard | 113×109 |
| `farm_17` | **StarterBase_UFO_Farm** | 69×75 |
| `ranger_station_07` | **StarterBase_Ranger_Station** | 70×79 |
| `hotel_03` | **StarterBase_Hotel_Tower** | 127×124 |
| `house_modern_18` | **StarterBase_Modern_House** — compound | 111×105 |
| `house_modern_31` | **StarterBase_Bunker_House** — compound | 69×75 |
| `Ayesoar_Mansion_by_MPLogue` | **StarterBase_Ayesoar_Mansion** — compound | 60×54 |
| `Modern_House_Zeebark` | **StarterBase_Zeebark_Modern_House** — own plot | 60×60 |

Two of them, the Ayesoar Mansion and the Zeebark house, were built with modded decoration, so they
lose some detail in the conversion. The structures are unchanged.

They sit in two walled plots — a **146×202 compound** and a **74×74 plot** 14 m east — behind a wall
copied block-for-block from the Modern House's own front wall, with seven working roll-up gates and
a paved ring road joined to the real road network.

## Credit

The POIs in this pack are other people's work. The buildings were designed by the authors of the
[Compopack](https://www.nexusmods.com/7daystodie/mods/5438),
[Zeebark](https://www.nexusmods.com/7daystodie/mods/6577),
[Voltralux](https://www.nexusmods.com/7daystodie/mods/4916),
[MPLogue](https://www.nexusmods.com/7daystodie/mods/3436),
[Svarii](https://www.nexusmods.com/7daystodie/mods/9899),
[Cog](https://www.nexusmods.com/7daystodie/mods/10928),
[WinterDawn](https://www.nexusmods.com/7daystodie/mods/9420),
[Caleseche](https://www.nexusmods.com/7daystodie/mods/10496) and
[ShadowModernHouse](https://www.nexusmods.com/7daystodie/mods/10509) packs, and the map itself by the
author of [Astoria 8K](https://www.nexusmods.com/7daystodie/mods/7017). All that was done here is a
material swap so they run without their mods. Go give them endorsements.
